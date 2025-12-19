# 工作流相对路径导入指南

## 概述

工作流引擎现在支持使用相对路径导入其他工作流，使得工作流组织更加灵活和模块化。

## 目录结构

```
workflows/
├── common/                    # 通用基础工作流
│   ├── navigate_to_garden.yml # 导航到花园
│   └── plant_crop.yml         # 种植作物
├── auto_garden.yml            # 主自动化工作流
├── shuangbaomuogu.yml        # 种植双孢蘑菇
├── harvest.yml                # 收获
└── monitor_harvest.yml        # 监控收获
```

## 导入语法

### 相对路径导入

使用 `./` 或 `../` 前缀表示相对路径：

```yaml
steps:
  # 从当前目录的 common 子目录导入
  - type: workflow
    workflow: ./common/navigate_to_garden
    description: "Navigate to garden"

  # 从父目录导入
  - type: workflow
    workflow: ../other_workflow
    description: "Import from parent"

  # 从当前目录导入
  - type: workflow
    workflow: ./common/monitor_harvest
    description: "Import from current dir"
```

### 绝对路径导入（从 workflows 根目录）

不使用 `./` 或 `../` 前缀：

```yaml
steps:
  # 从 workflows/ 根目录导入
  - type: workflow
    workflow: auto_garden
    description: "Import from root"

  # 从 workflows/common/ 导入
  - type: workflow
    workflow: common/navigate_to_garden
    description: "Import from subdirectory"
```

## 示例

### 示例 1: 顶层工作流导入基础工作流

**文件：** `workflows/shuangbaomuogu.yml`

```yaml
description: "Complete workflow to plant shuangbaomogu"

steps:
  # 使用相对路径从 common/ 导入
  - type: workflow
    workflow: ./common/navigate_to_garden
    description: "Navigate to garden interface"

  - type: workflow
    workflow: ./common/plant_crop
    description: "Plant shuangbaomogu"
    params:
      crop_name: "shuangbaomogu"
```

### 示例 2: 嵌套导入

**文件：** `workflows/common/navigate_to_garden.yml`

```yaml
description: "Navigate to garden from current location"

steps:
  # 如果需要，可以从这里导入同目录的其他工作流
  - type: workflow
    workflow: ./check_location
    description: "Check current location"

  # 或导入父目录的工作流
  - type: workflow
    workflow: ../helper_workflow
    description: "Use helper from parent"
```

### 示例 3: 混合使用相对路径和绝对路径

```yaml
steps:
  # 相对路径：从当前目录的子目录导入
  - type: workflow
    workflow: ./common/navigate_to_garden

  # 绝对路径：从 workflows 根目录导入
  - type: workflow
    workflow: harvest

  # 相对路径：从当前目录导入
  - type: workflow
    workflow: ./common/monitor_harvest
```

## 路径解析规则

1. **相对路径** (`./` 或 `../` 开头)
   - 相对于**当前执行的工作流文件所在目录**
   - 例如：如果 `workflows/shuangbaomuogu.yml` 导入 `./common/navigate_to_garden`
   - 解析为：`workflows/common/navigate_to_garden.yml`

2. **绝对路径**（无 `./` 或 `../` 前缀）
   - 相对于 `workflows/` 根目录
   - 例如：`common/navigate_to_garden` 解析为 `workflows/common/navigate_to_garden.yml`

3. **自动添加 `.yml` 扩展名**
   - 无需在工作流名称中包含 `.yml`
   - `./common/navigate_to_garden` 自动解析为 `./common/navigate_to_garden.yml`

## 优势

1. **模块化组织**
   - 可以将通用工作流放在 `common/` 目录
   - 将特定功能的工作流分组到子目录

2. **可重用性**
   - 基础工作流可以被多个高层工作流导入
   - 减少重复代码

3. **清晰的依赖关系**
   - 相对路径清楚地表明工作流之间的关系
   - 更容易理解工作流的层次结构

4. **灵活的重构**
   - 可以移动工作流到不同目录
   - 只需更新相对路径引用

## 注意事项

1. **循环依赖**
   - 避免 A 导入 B，B 又导入 A 的情况
   - 引擎会无限递归

2. **路径区分大小写**
   - 在某些系统上路径是区分大小写的
   - 建议使用小写和下划线命名

3. **工作流缓存**
   - 已加载的工作流会被缓存
   - 使用规范化的绝对路径作为缓存键

## Python API 使用

```python
from workflow import WorkflowEngine
from functions import get_all_functions

# 初始化引擎
engine = WorkflowEngine()
engine.register_functions(get_all_functions())

# 执行使用相对路径的工作流
engine.execute_workflow("shuangbaomuogu", params={"crop_name": "shuangbaomogu"})

# 也可以直接执行子目录中的工作流
engine.execute_workflow("common/navigate_to_garden")
```

## 命令行使用

```bash
# 执行顶层工作流（会自动使用相对路径导入）
python main.py auto shuangbaomogu

# 植物工作流（使用相对导入）
python main.py plant shuijinglan
```
