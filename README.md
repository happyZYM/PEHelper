# PEHeler
仅需输入原始数据和几个公式，PEHelper便可自动为您计算物理量的值、不确定度、灵敏系数

支持的特性有：
- [x] 将工作区保存为文件
- [x] 指定数值运算的精度
- [x] 自动追踪不确定度
- [ ] 多因变量
- [ ] 常见的数据拟合

# 使用方法
![pic](https://cloud.zymsite.ink/f/mB4cK/example.gif)
## 下载
### Windows端
在<https://github.com/happyZYM/PEHelper/releases/>页面下载对应版本的`PEHelper.zip`，解压后即可使用
### 其他平台
在<https://github.com/happyZYM/PEHelper/releases/>页面下载对应版本的源码，安装`PyQt6`、`SymPy`、`Scipy`、`mpmath`等依赖项即可使用

## 文件操作
- 打开：菜单栏 File->Open，或Ctrl+O
- 保存：菜单栏 File->Save，或Ctrl+S
- 另存为：菜单栏 File->Save As，或Ctrl+Shift+S

## 原始数据编辑
进入Raw Variables标签页
- 增加变量：点击左下角Add Raw Variable
- 删除变量：右击变量->Delete
- 修改变量名：双击变量 或 右击变量->Edit Name
- 变量类型：在右侧面板下拉框中选择。Full类型表示这个变量无序预处理，直接录入它的值和不确定度；Single类型表示这个变量为单次采样，可输入它的读书、允差、数量级、读数系统误值，实际值=(度数-系统误差)\*数量级，实际系统误差=读数系统误值\*数量级；Multiple类型标识这个变量为多次采用，需要输入一个读数列表，其他值的意义通Single类型。**注意：修改变量类型会清空已输入的数据**
- Multiple类型读数列表的编辑：点击AddData或按Ctrl+A添加数据，右击数据可删除或编辑；左击后按住不放拖动可调换位置。

## 中间变量编辑
有时算式很庞大，一次性写出可读性较差，此时可以引入中间变量，进入Intermediate Variables标签页可编辑中间变量
- 增加变量：点击下方Add Intermediate
- 删除变量：右击->Delete
- 调整顺序保证依赖正确：左击，按住不放，拖动

## 数据分析
### 操作
进入Analysis标签页，可设置因变量名称，表达式，置信度，数值运算的有效位数，然后点击按钮Start Analysis即可获取分析报告。
### 报告解读
- `Value`：数值
- `Uncertainty`：不确定度
- `Derivative`：灵敏系数

## 公式语法
计算模块采用SymPy，因此常见符号均可直接使用，如圆周率直接输入`pi`，根号直接输入`sqrt(...)`，乘方输入`**`