# -*- coding:utf-8 -*-

__author__ = 'Ace'
__email__ = '394452216@qq.com'

"""
Test1
自动模拟点击UI窗口
解决需求：
1.模拟人工点击操作进行自动化。

这个开发项目的针对一款windows的桌面软件。此桌面软件是用一个webkit写的浏览器。外部无法获取控件hwnd等任何信息。
所以只能根据UI反馈的颜色信息进行每步自动化的操作。

步骤器：
1.点击器
2.输入器
3.颜色检查器

Machine为一个管理器
加入所需的步骤器即可
然后start

如何取消？
鼠标动一下就可以。每次步骤前会检查上一次的步骤坐标。如果用户干预了鼠标。就会终止所有步骤的执行

"""

from ctypes import *
import win32api
import win32con
import time
import win32gui
import win32clipboard as w


class POINT(Structure):
    _fields_ = [("x", c_ulong), ("y", c_ulong)]


class ColorCheck(object):
    def __init__(self, source_color, cursour_color=None, c_pos=None):
        self.source_color = source_color
        self.cursour_color = cursour_color
        self.c_pos = c_pos

    @staticmethod
    def get_mouse_point():
        po = POINT()
        windll.user32.GetCursorPos(byref(po))
        return int(po.x), int(po.y)

    @staticmethod
    def get_desktop_color():
        hwnd = win32gui.GetDesktopWindow()
        dc = win32gui.GetWindowDC(hwnd)
        long_colour = win32gui.GetPixel(dc, *ColorCheck.get_mouse_point())
        i_colour = int(long_colour)
        return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

    def check(self):
        # 如果未设置目标颜色 直接返回True
        if self.source_color == None:
            return True

        if self.source_color == ColorCheck.get_desktop_color():
            return True
        else:
            return False


class MouseObject(object):
    def __init__(self, x, y, hwnd):
        self.x = x
        self.y = y
        self.hwnd = hwnd

    def offset(self):
        window_pos = win32gui.GetWindowPlacement(self.hwnd)
        w_x, w_y = window_pos[-1][0], window_pos[-1][1]
        return (w_x + self.x, w_y + self.y)

    def __click(self):
        self.mouse_move(*self.offset())
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)

    def click(self):
        self.__click()

    def doubclick(self):
        self.__click()
        self.__click()

    def mouse_move(self, x, y):
        windll.user32.SetCursorPos(x, y)
        time.sleep(0.05)


class ClickBox(MouseObject):
    def __init__(self, x, y, double=False, hwnd=0):
        super(ClickBox, self).__init__(x, y, hwnd)

        self.check_color = None
        self.sleep = 0
        if double:
            self.click = self.doubclick

    def set_color(self, color):
        self.check_color = color

    def set_sleep(self, value):
        self.sleep = value

    def start(self):
        # 循环检查点击后的颜色是否正确
        while True:
            self.click()
            if ColorCheck(source_color=self.check_color).check():
                time.sleep(self.sleep)
                return True


class InputBox(object):
    def __init__(self, text):
        super(InputBox, self).__init__()
        self.text = text

    @staticmethod
    def setText(string):
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, string)
        w.CloseClipboard()

    @staticmethod
    def paset():
        win32api.keybd_event(17, 0, 0, 0)
        win32api.keybd_event(86, 0, 0, 0)
        win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)


    def start(self):
        # 循环检查点击后的颜色是否正确

        InputBox.setText(self.text)
        InputBox.paset()


class ChcekColorBox(MouseObject):
    def __init__(self, x, y, colors, hwnd, isbreak):
        super(ChcekColorBox, self).__init__(x, y, hwnd=hwnd)
        self.tager_color = colors
        self.last_pos = None
        self.isbreak = isbreak
        self.fail = False

    def set_tager_color(self, value):
        self.tager_color = value

    def start(self):
        # 循环检查点击后的颜色是否正确

        while True:

            self.mouse_move(*self.offset())
            current_color = ColorCheck.get_desktop_color()
            print current_color, self.tager_color
            if current_color in self.tager_color:
                self.fail = False
                return True
            else:
                if self.isbreak:
                    self.fail = True
                    return
                time.sleep(0.5)


class Machine(object):
    def __init__(self):
        self.task = []
        self.is_break_lst = []
        self.input_lst = []

        self.round = 2

        self.last_pos = None
        self.sleep_time = 0.35

    def set_round(self, value):
        self.round = value

    def add_input(self, text=""):
        item = InputBox(text=text)
        self.task.append(item)
        self.input_lst.append(item)

    def add_color_check(self, x, y, colors, hwnd, isbreak=False):
        item = ChcekColorBox(x, y, colors=colors, hwnd=hwnd, isbreak=isbreak)
        self.task.append(item)
        self.is_break_lst.append(item)

    def add_click(self, x, y, colors=None, double=False, hwnd=0, sleep=0):
        item = ClickBox(x=x, y=y, double=double, hwnd=hwnd)
        item.set_color(colors)
        item.set_sleep(sleep)
        self.task.append(item)

    def run(self):
        for a in xrange(self.round):
            for i in self.task:
                # 如果上次点击完的坐标和现在获取的坐标不一样。就中断
                time.sleep(self.sleep_time)
                if self.last_pos and self.last_pos != ColorCheck.get_mouse_point():
                    return

                if i in self.input_lst:
                    i.text = str(10002 + a)

                i.start()
                self.last_pos = ColorCheck.get_mouse_point()
                if i in self.is_break_lst:
                    if i.fail:
                        break


if __name__ == '__main__':

    machine = Machine()
    down_h = win32gui.FindWindow(None, u'下载列表')
    main_h = win32gui.FindWindow(None, u'Smart+设计平台')

    # 取消上次的标签
    machine.add_click(x=524, y=143, hwnd=main_h, sleep=0.5)

    # 双击输入框
    machine.add_click(x=116, y=195, hwnd=main_h, double=True)

    # 输入ID
    machine.add_input(text=str(10003))

    # 点击搜索
    machine.add_click(x=217, y=195, hwnd=main_h)

    # 检查是否正在加载... (背景颜色)，出现230则代表搜索成功
    machine.add_color_check(x=320, y=275, hwnd=main_h, colors=((230, 230, 230),))

    #  检查是否有资源（下载按钮颜色）没有资源则中断后续步骤
    machine.add_color_check(x=576, y=350, hwnd=main_h, colors=((22, 128, 157), (9, 144, 181)), isbreak=True)

    # 点击下载按钮
    machine.add_click(x=555, y=350, hwnd=main_h)

    #  检查下载进度，(文件夹按钮的颜色)
    machine.add_color_check(x=805, y=136, hwnd=down_h, colors=((149, 149, 149), (201, 201, 201)))

    # 删除任务
    machine.add_click(x=747, y=136, hwnd=down_h)

    # 确定
    machine.add_click(x=416, y=397, hwnd=down_h)

    machine.set_round(15)

    machine.run()
