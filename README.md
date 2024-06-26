# Virtual Control

## 介绍
想要开发一个通过捕捉手部关键点，以此来实现远程控制鼠标/键盘等功能的程序。

## 效果展示
1.58 W@z.tr RKW:/ 03/22 我想当网红 # 人工智能  https://v.douyin.com/ij6uPDme/ 复制此链接，打开Dou音搜索，直接观看视频！

## 环境（现阶段）
- python 
- opencv 
- mediapipe 
- pyautogui
- PyQt5
- pygetwindow

## 关键点捕捉
目前使用[mediapipe](https://github.com/google/mediapipe)内置的功能来实现手部追踪，以及关键点获取。后续将采用自训练的keypoint网络来代替此部分内容，以提升帧率及精度。

## 功能（to do list）
- 页面上下滚动 ✅
- 实时展示手部关键点 ✅
- 鼠标点击
- 移动平滑

## 运行
```
python main.py --window Edge --reset 2 --fps 30 --quit 2
```
参数介绍：
- window：指定控制窗口名称，默认Edge
- reset：指定重置标准位置时间，默认2秒
- fps：指定帧率，默认30
- quit: 指定退出时间，默认2秒

## 功能实现简述

- **阈值设定**：根据当前显示器分辨率进行调整，考虑手部细微抖动对于轨迹的影响，因此犹如阈值进行控制。
- **标准坐标位置**：食指在某个点以及阈值范围区域内停留2秒以上的坐标。会将此点的y轴坐标显示在窗口最右侧。
- **退出**：由于切换了控制窗口，因此qt窗口不再接受键盘等输入的内容。因此改为，将食指放置在右侧退出区域内一定时间后退出。
- **页面上下滚动**：根据当前食指运动后坐标与标准坐标对比，超过预设的阈值则判定为手指滑动。并设置判断参数，在没有回到标准坐标或重置标准坐标前，只会朝同一方向进行一次滑动。