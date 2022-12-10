# 窗口化程序部分,核心逻辑代码全部在mods\下
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk
import os
import cv2
from autoMatch import iterMatch
import threading

root = Tk()
root.title('图书ISBN号字符识别')

# 按钮逻辑部分
img = None  # 打开的图片
imgLabel = None  # 防warning
runButton = None
resLabel = None


def openImage():
    global img
    path = askopenfilename()
    if os.path.exists(path):
        img = cv2.imread(path)
        imgShow = ImageTk.PhotoImage(file=path)
        imgLabel.config(image=imgShow)
        # 防止临时变量消亡
        imgLabel.image = imgShow


def matchThr():
    '''为了防止前端卡死，多线程处理'''
    res = iterMatch(img)
    resLabel.config(text='识别结果：'+res)
    runButton.config(state='normal')


def matchImage():
    if type(img) == type(None):
        showinfo('提示', '未打开图片')
        return
    runButton.config(state='disabled')
    thr = threading.Thread(target=matchThr)
    thr.start()


def clipRes():
    # 去掉"识别结果:"五个字符
    res = resLabel['text'][5:]
    root.clipboard_append(res)


# 控件布局部分
ftop = Frame(root)
imgLabel = Label(root)
fbottom = Frame(root)
openButton = Button(ftop, text='打开图片', command=openImage)
runButton = Button(ftop, text='进行识别', command=matchImage)
resLabel = Label(fbottom, text='识别结果:')
copyButton = Button(fbottom, text='复制到剪贴板', command=clipRes)
ftop.grid(row=0)
imgLabel.grid(row=1)
fbottom.grid(row=2)
openButton.grid(row=0, column=0, padx=5, pady=5)
runButton.grid(row=0, column=1, padx=5, pady=5)
resLabel.grid(row=0, column=1, padx=5, pady=5)
copyButton.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
