from postScrolling import postScrolling
import argparse
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
def args():
    parser = argparse.ArgumentParser(description='Personal information')
    parser.add_argument('--window', dest='window', type=str, default="Edge", help='需要进行控制的窗口名称')
    parser.add_argument('--reset', dest='reset', type=int, default=2, help='重置标准位置时间')
    parser.add_argument('--fps', dest='fps', type=int, default=30, help='刷新频率')
    parser.add_argument('--quit', dest='quit', type=int, default=2, help='悬停退出时间')
    args = parser.parse_args()
    return args

def main(args):
    app = QApplication(sys.argv)
    window = postScrolling(args.window, args.reset, args.fps, args.quit)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    args = args()
    main(args)