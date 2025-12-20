# Milthm Auto Garden Milthm 自动种菜

## 项目结构

```
milthm-auto-garden/
├── main.py          # 示例脚本和演示
├── core.py          # 核心功能：图像识别、窗口捕获、鼠标点击
├── functions.py     # 每个图片对应的独立点击函数
├── assets/
│   ├── button/      # 按钮图片
│   │   ├── button_shouhuo.png
│   │   ├── button_zhongzhi.png
│   │   └── button_luxiaohuiting.png
│   ├── icon/        # 图标图片
│   │   └── icon_shouhuo.png
│   └── item/        # 物品图片
│       └── konghuapen.png
└── README.md        # 本文档
```

## 快速开始

### 安装依赖

```bash
uv pip install opencv-python numpy psutil pywin32 mss
```

### 使用

```bash
python main.py auto shuangbaomogu
```

```bash
python main.py auto 勿忘草
```

## 可用函数

### 按钮 (Button)

- `button_luxiaohuiting()` - 点击"录像回厅"按钮
- `button_shouhuo()` - 点击"收获"按钮
- `button_zhongzhi()` - 点击"种植"按钮

### 图标 (Icon)

- `icon_shouhuo()` - 点击"收获"图标

### 物品 (Item)

- `item_konghuapen()` - 点击"空花盆"物品

## 函数参数

所有函数都支持以下可选参数：

```python
def button_shouhuo(
    process_name: str = "milthm.exe",  # 目标进程名称
    threshold: float = 0.5,             # 匹配阈值 (0.0-1.0)
) -> bool:
    """返回 True 表示成功，False 表示失败"""
    ...
```

**示例：**

```python
# 使用默认设置
button_shouhuo()

# 自定义阈值（提高精确度）
button_shouhuo(threshold=0.7)

# 自定义进程名称
button_shouhuo(process_name="other_game.exe")

# 同时自定义多个参数
button_shouhuo(process_name="game.exe", threshold=0.6)
```

## 添加新图片

要为新图片添加点击函数：

1. 将图片放入相应的 `assets/` 子目录
2. 在 `functions.py` 中添加对应函数：

```python
def button_new_feature(
    process_name: str = PROCESS_NAME,
    threshold: float = MATCH_THRESHOLD,
) -> bool:
    """点击新功能按钮"""
    template_path = str(ASSETS_DIR / "button" / "button_new_feature.png")
    return locate_and_click(template_path, process_name, threshold)
```

3. 在其他脚本中导入使用：

```python
from functions import button_new_feature
button_new_feature()
```

## 高级用法

### 获取所有可用函数

```python
from functions import get_all_functions

all_funcs = get_all_functions()
for name, func in all_funcs.items():
    print(f"Available: {name}")
```

### 错误处理

```python
from functions import button_shouhuo

if button_shouhuo():
    print("成功点击！")
else:
    print("未找到按钮或点击失败")
```

### 循环重试

```python
import time
from functions import button_shouhuo

max_retries = 5
for i in range(max_retries):
    if button_shouhuo():
        print("成功！")
        break
    print(f"重试 {i+1}/{max_retries}...")
    time.sleep(1)
```

## 配置

可以在 `core.py` 中修改默认配置：

```python
PROCESS_NAME = "milthm.exe"  # 目标进程名称
MATCH_THRESHOLD = 0.5         # 默认匹配阈值
SCALES = [1.0, 0.95, 0.9, ...] # 模板匹配的缩放比例
```

## 调试

如果点击不准确或找不到图片：

1. **提高阈值**：`button_shouhuo(threshold=0.7)`
2. **检查进程名称**：确保游戏进程名正确
3. **检查图片质量**：确保模板图片清晰且与游戏界面匹配
4. **查看日志输出**：函数会打印匹配得分和坐标信息

## 📄 License

MIT License
