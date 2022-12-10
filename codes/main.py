# 窗口化程序部分,核心逻辑代码全部在其他代码文件
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk, Image
import os
import cv2
from autoMatch import iterMatch
import threading
import numpy as np

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
        # 读取带中文路径的图片，不能直接imread
        img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # 为了不让窗口特别大，缩放一下
        img0 = Image.open(path)
        h, w = img0.size
        sh, sw = 400/h, 600/w
        s = min(sw, sh, 1)
        img0 = img0.resize((int(h*s), int(w*s)), Image.Resampling.BICUBIC)
        imgShow = ImageTk.PhotoImage(img0)
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
    root.clipboard_clear()
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
