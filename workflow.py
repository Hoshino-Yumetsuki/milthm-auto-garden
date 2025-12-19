"""Workflow engine for game automation.

This module provides a YAML-based workflow orchestration system that supports:
- Loading workflows from YAML files
- Composing workflows (workflows can reference other workflows)
- Event loops for continuous monitoring
- Parameterized workflows
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Optional, Any, Dict, List
from dataclasses import dataclass
import yaml


class WorkflowEngine:
    """Main workflow engine that loads and executes YAML-based workflows."""

    def __init__(self, workflows_dir: str = "workflows"):
        self.workflows_dir = Path(workflows_dir)
        self.loaded_workflows: Dict[str, Dict] = {}
        self.function_registry: Dict[str, Callable] = {}
        self.workflow_stack: List[Path] = (
            []
        )  # Track current workflow path for relative imports

    def register_function(self, name: str, func: Callable) -> None:
        """Register a function that can be called from workflows."""
        self.function_registry[name] = func

    def register_functions(self, functions: Dict[str, Callable]) -> None:
        """Register multiple functions at once."""
        self.function_registry.update(functions)

    def load_workflow(
        self, workflow_name: str, current_workflow_dir: Optional[Path] = None
    ) -> tuple[Dict, Path]:
        """Load a workflow from YAML file.

        Args:
            workflow_name: Workflow name or relative path (e.g., "./common/navigate" or "auto_garden")
            current_workflow_dir: Directory of the current workflow (for relative imports)

        Returns:
            Tuple of (workflow_data, workflow_file_path)
        """
        # Check if it's a relative path
        if workflow_name.startswith("./") or workflow_name.startswith("../"):
            if current_workflow_dir is None:
                current_workflow_dir = self.workflows_dir
            workflow_file = (current_workflow_dir / workflow_name).with_suffix(".yml")
        else:
            # Absolute path from workflows root
            workflow_file = self.workflows_dir / f"{workflow_name}.yml"

        # Normalize the path
        workflow_file = workflow_file.resolve()

        # Use normalized path as cache key
        cache_key = str(workflow_file)
        if cache_key in self.loaded_workflows:
            return self.loaded_workflows[cache_key], workflow_file

        if not workflow_file.exists():
            raise FileNotFoundError(f"Workflow file not found: {workflow_file}")

        with open(workflow_file, "r", encoding="utf-8") as f:
            workflow_data = yaml.safe_load(f)

        self.loaded_workflows[cache_key] = workflow_data
        return workflow_data, workflow_file

    def execute_workflow(
        self, workflow_name: str, params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Execute a workflow by name with optional parameters."""
        print(f"\n{'='*60}")
        print(f"Executing workflow: {workflow_name}")
        if params:
            print(f"Parameters: {params}")
        print(f"{'='*60}")

        # Get current workflow directory from stack (for relative imports)
        current_dir = self.workflow_stack[-1].parent if self.workflow_stack else None
        workflow, workflow_file = self.load_workflow(workflow_name, current_dir)
        params = params or {}

        if "steps" not in workflow:
            print(f"[Error] No steps found in workflow '{workflow_name}'")
            return False

        # Push current workflow to stack
        self.workflow_stack.append(workflow_file)
        try:
            return self._execute_steps(workflow["steps"], params)
        finally:
            # Pop from stack when done
            self.workflow_stack.pop()

    def _execute_steps(self, steps: list, params: Dict[str, Any]) -> bool:
        """Execute a list of workflow steps."""
        for step_data in steps:
            if not self._execute_step(step_data, params):
                return False
        return True

    def _execute_step(self, step_data: Dict, params: Dict[str, Any]) -> bool:
        """Execute a single workflow step."""
        step_type = step_data.get("type", "action")

        if step_type == "action":
            return self._execute_action(step_data, params)
        elif step_type == "workflow":
            return self._execute_sub_workflow(step_data, params)
        elif step_type == "condition":
            return self._execute_condition(step_data, params)
        elif step_type == "event_loop":
            return self._execute_event_loop(step_data, params)
        else:
            print(f"[Error] Unknown step type: {step_type}")
            return False

    def _execute_action(self, action_data: Dict, params: Dict[str, Any]) -> bool:
        """Execute a single action."""
        action_name = action_data.get("action")
        description = action_data.get("description", action_name)
        wait_after = action_data.get("wait_after", 0.5)
        retry = action_data.get("retry", 1)
        optional = action_data.get("optional", False)

        if action_name not in self.function_registry:
            print(f"[Error] Function '{action_name}' not registered")
            return not optional

        func = self.function_registry[action_name]

        # Handle dynamic parameters
        func_params = []
        if "param" in action_data:
            param_name = action_data["param"]
            if param_name in params:
                func_params.append(params[param_name])

        print(f"\n[Action] {description}")

        for attempt in range(retry):
            try:
                result = func(*func_params) if func_params else func()
                if result:
                    print(f"[Action] ✓ {description} succeeded")
                    if wait_after > 0:
                        time.sleep(wait_after)
                    return True
                else:
                    if attempt < retry - 1:
                        print(f"[Action] ⟳ Retrying ({attempt + 1}/{retry})...")
                        time.sleep(1.0)
            except Exception as e:
                print(f"[Action] ✗ Error: {e}")
                if attempt < retry - 1:
                    time.sleep(1.0)

        if optional:
            print(f"[Action] ⊘ Failed but optional, continuing...")
            return True

        print(f"[Action] ✗ {description} failed")
        return False

    def _execute_sub_workflow(
        self, workflow_data: Dict, params: Dict[str, Any]
    ) -> bool:
        """Execute a sub-workflow (workflow reference)."""
        workflow_name = workflow_data.get("workflow")
        if not workflow_name or not isinstance(workflow_name, str):
            print(f"[Error] No workflow name specified in sub-workflow")
            return False

        description = workflow_data.get("description", f"Sub-workflow: {workflow_name}")
        workflow_params = workflow_data.get("params", {})

        # Merge parent params with workflow-specific params
        merged_params = {**params, **workflow_params}

        print(f"\n[Sub-Workflow] {description}")
        # execute_workflow will handle relative paths using the workflow_stack
        return self.execute_workflow(workflow_name, merged_params)

    def _execute_condition(self, condition_data: Dict, params: Dict[str, Any]) -> bool:
        """Execute a conditional branch."""
        condition_name = condition_data.get("condition")
        description = condition_data.get("description", condition_name)
        on_true = condition_data.get("on_true", [])
        on_false = condition_data.get("on_false", [])

        if condition_name not in self.function_registry:
            print(f"[Error] Condition '{condition_name}' not registered")
            return False

        condition_func = self.function_registry[condition_name]

        print(f"\n[Condition] Checking: {description}")

        try:
            result = condition_func()
            if result:
                print(f"[Condition] ✓ True - executing true branch")
                return self._execute_steps(on_true, params)
            else:
                print(f"[Condition] ✗ False - executing false branch")
                return self._execute_steps(on_false, params)
        except Exception as e:
            print(f"[Condition] ✗ Error: {e}")
            return False

    def _execute_event_loop(self, loop_data: Dict, params: Dict[str, Any]) -> bool:
        """Execute an event loop."""
        name = loop_data.get("name", "Event Loop")
        interval = loop_data.get("interval", 10.0)
        handlers = loop_data.get("handlers", [])

        print(f"\n[EventLoop] Starting: {name} (interval: {interval}s)")
        print("[EventLoop] Press Ctrl+C to stop")

        try:
            while True:
                for handler in handlers:
                    handler_name = handler.get("name", "Handler")
                    condition = handler.get("condition")
                    actions = handler.get("actions", [])

                    if condition and condition in self.function_registry:
                        condition_func = self.function_registry[condition]
                        if condition_func():
                            print(f"\n[EventLoop] Trigger: {handler_name}")
                            self._execute_steps(actions, params)

                time.sleep(interval)
        except KeyboardInterrupt:
            print(f"\n[EventLoop] Stopped by user")
            return True

        return True


# Legacy support classes (for backward compatibility)
@dataclass
class WorkflowStep:
    """Legacy workflow step class."""

    name: str
    action: Callable[[], bool]
    wait_after: float = 0.5
    retry_count: int = 3
    retry_delay: float = 1.0
    optional: bool = False

    def execute(self) -> bool:
        print(f"\n[Workflow] Executing: {self.name}")
        for attempt in range(self.retry_count):
            try:
                if self.action():
                    print(f"[Workflow] ✓ {self.name} succeeded")
                    if self.wait_after > 0:
                        time.sleep(self.wait_after)
                    return True
                else:
                    if attempt < self.retry_count - 1:
                        print(
                            f"[Workflow] ⟳ Retrying ({attempt + 1}/{self.retry_count})..."
                        )
                        time.sleep(self.retry_delay)
            except Exception as e:
                print(f"[Workflow] ✗ Error: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
        if self.optional:
            print(f"[Workflow] ⊘ Failed but optional, continuing...")
            return True
        print(f"[Workflow] ✗ {self.name} failed")
        return False


@dataclass
class ConditionalStep:
    """Legacy conditional step class."""

    name: str
    condition: Callable[[], bool]
    true_steps: list
    false_steps: Optional[list] = None

    def execute(self) -> bool:
        print(f"\n[Workflow] Checking condition: {self.name}")
        try:
            if self.condition():
                print(f"[Workflow] ✓ Condition True")
                for step in self.true_steps:
                    if not step.execute():
                        return False
            else:
                print(f"[Workflow] ✗ Condition False")
                if self.false_steps:
                    for step in self.false_steps:
                        if not step.execute():
                            return False
        except Exception as e:
            print(f"[Workflow] ✗ Error: {e}")
            return False
        return True


class Workflow:
    """Legacy workflow class."""

    def __init__(self, name: str):
        self.name = name
        self.steps = []

    def add_step(self, step: WorkflowStep | ConditionalStep) -> Workflow:
        """Add a step to the workflow.

        Args:
            step: WorkflowStep or ConditionalStep to add

        Returns:
            Self for method chaining
        """
        self.steps.append(step)
        return self

    def add_action(
        self,
        name: str,
        action: Callable[[], bool],
        wait_after: float = 0.5,
        retry_count: int = 3,
        retry_delay: float = 1.0,
        optional: bool = False,
    ) -> Workflow:
        """Convenience method to add an action step.

        Args:
            name: Step name
            action: Function to execute
            wait_after: Seconds to wait after successful execution
            retry_count: Number of retry attempts
            retry_delay: Seconds to wait between retries
            optional: If True, failure won't stop the workflow

        Returns:
            Self for method chaining
        """
        step = WorkflowStep(
            name=name,
            action=action,
            wait_after=wait_after,
            retry_count=retry_count,
            retry_delay=retry_delay,
            optional=optional,
        )
        return self.add_step(step)

    def add_condition(
        self,
        name: str,
        condition: Callable[[], bool],
        true_steps: List[WorkflowStep],
        false_steps: Optional[List[WorkflowStep]] = None,
    ) -> Workflow:
        """Convenience method to add a conditional branch.

        Args:
            name: Condition name
            condition: Function that returns True or False
            true_steps: Steps to execute if condition is True
            false_steps: Steps to execute if condition is False (optional)

        Returns:
            Self for method chaining
        """
        cond = ConditionalStep(
            name=name,
            condition=condition,
            true_steps=true_steps,
            false_steps=false_steps,
        )
        return self.add_step(cond)

    def execute(self) -> bool:
        """Execute all steps in the workflow.

        Returns:
            True if all steps succeed, False otherwise.
        """
        print(f"\n{'='*60}")
        print(f"Starting workflow: {self.name}")
        print(f"{'='*60}")

        for step in self.steps:
            if not step.execute():
                print(f"\n{'='*60}")
                print(f"Workflow '{self.name}' FAILED")
                print(f"{'='*60}")
                return False

        print(f"\n{'='*60}")
        print(f"Workflow '{self.name}' COMPLETED successfully")
        print(f"{'='*60}")
        return True


class EventLoop:
    """Event loop for continuous monitoring and automated responses."""

    def __init__(self, name: str, check_interval: float = 5.0):
        self.name = name
        self.check_interval = check_interval
        self.handlers: List[tuple[str, Callable[[], bool], Callable[[], bool]]] = []
        self.running = False

    def add_handler(
        self,
        name: str,
        condition: Callable[[], bool],
        action: Callable[[], bool],
    ) -> EventLoop:
        """Add an event handler.

        Args:
            name: Handler name
            condition: Function to check if event should trigger
            action: Function to execute when condition is True

        Returns:
            Self for method chaining
        """
        self.handlers.append((name, condition, action))
        return self

    def run(self, max_iterations: Optional[int] = None) -> None:
        """Run the event loop.

        Args:
            max_iterations: Maximum number of iterations (None for infinite)
        """
        print(f"\n{'='*60}")
        print(f"Starting event loop: {self.name}")
        print(f"Check interval: {self.check_interval}s")
        print(f"{'='*60}")

        self.running = True
        iteration = 0

        try:
            while self.running:
                if max_iterations is not None and iteration >= max_iterations:
                    print(f"\n[EventLoop] Reached max iterations ({max_iterations})")
                    break

                iteration += 1
                print(f"\n[EventLoop] Iteration {iteration}")

                for name, condition, action in self.handlers:
                    try:
                        if condition():
                            print(f"[EventLoop] ✓ Event triggered: {name}")
                            if action():
                                print(f"[EventLoop] ✓ Action succeeded: {name}")
                            else:
                                print(f"[EventLoop] ✗ Action failed: {name}")
                        else:
                            print(f"[EventLoop] ⊘ Event not triggered: {name}")
                    except Exception as e:
                        print(f"[EventLoop] ✗ Error in handler '{name}': {e}")

                print(
                    f"[EventLoop] Waiting {self.check_interval}s before next check..."
                )
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            print(f"\n[EventLoop] Interrupted by user")
        finally:
            self.running = False
            print(f"\n{'='*60}")
            print(f"Event loop '{self.name}' stopped")
            print(f"{'='*60}")

    def stop(self) -> None:
        """Stop the event loop."""
        self.running = False
