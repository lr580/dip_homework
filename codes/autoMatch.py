import cv2
from preRotate import *
from graphCut import *
from stringMatch import *



def toString(res):
    '''给定一个字符数组,转换为字符串形式'''
    s = ''
    for i in res:
        s += i
    return s


def reshape(img, mw=1000, mh=1000):
    '''给定图片,等比例裁剪使长宽不超mw,mh'''
    h, w = img.shape[:2]
    sh, sw = mh/h, mw/w
    s = min(sw, sh, 1)  # 与1比较,防止放大
    res = cv2.resize(img, (0, 0), fx=s, fy=s)
    return res


def preDeal(img0):
    '''给定一张图片,将其裁剪大小和自动旋转'''
    img = autoRotateC(img0)
    img = reshape(img)
    return img


def filtRes(m):
    '''输入匹配结果，对结果进行筛除和修正并返回'''
    r = []
    hasB = False  # 是否出现过B
    for i in m:
        # 首次出现B
        if i == 'B' and not hasB:
            hasB = True
            continue
        # 再次出现B,根据实践经验,结果应修改为0
        if i == 'B' and hasB:
            i = '0'
        # 只保留数字
        if i not in 'ISBN-':
            r.append(i)
    return r


def getChecksum(m):
    '''输入ISBN码序列,返回校验码'''
    s = 0
    if len(m) == 10:
        w = [i for i in range(10, 1, -1)]
        for i in range(9):
            s += w[i]*int(m[i])
        s %= 11
        if s == 10:
            return 'X'
        return chr(ord('0')+s)
    else:
        for i in range(12):
            # 权重奇数位是1,偶数位是3
            w = 3 if i % 2 else 1
            s += w*int(m[i])
        s = (10-(s % 10)) % 10
        return chr(ord('0')+s)


def checkISBN(m):
    '''输入初筛后的校验码序列,校验它是否正确'''
    if m[:-1].count('X'):
        return False  # 只有最后位可能是X
    if len(m) not in (10, 13):
        return False  # 长度不对
    return m[-1] == getChecksum(m)

# 测试
# checkISBN([i for i in '9787222070370'])


def adjudgeByChecksum(m):
    '''给定ISBN码序列,若不合校验码将其根据校验码校正并返回'''
    if len(m) not in (10, 13):
        return m  # 改不了没救了
    if m[:-1].count('X'):
        return m  # 改不了没救了
    if not checkISBN(m):
        m[-1] = getChecksum(m)
    return m


def average(m):
    '''返回校验码序列的平均值'''
    a = [int(i) for i in m if i != 'X']
    return sum(a)/max(1, len(a))


def betterMatch(m1, m2):
    '''给定两个匹配结果，选择最优的'''
    d1, d2 = filtRes(m1), filtRes(m2)
    r1, r2 = checkISBN(d1), checkISBN(d2)
    # 如果r1,r2都对,取平均数最接近4.5的
    if r1 and r2:
        a1, a2 = average(d1), average(d2)
        if abs(a1-4.5) < abs(a2-4.5):
            return d1
        return d2
    if r1:
        return d1
    if r2:
        return d2
    l1, l2 = len(d1), len(d2)
    # 一个都不对的话,优先选长度接近的
    if l1 == 13:
        return d1
    if l2 == 13:
        return d2
    if l1 == 10:  # 选10的优先级低一些
        return d1
    if l2 == 10:
        return d2
    return d1  # 否则,优先选先找到的


def matchFlip(img):
    '''给定一张图片,将其正反都匹配一次取最优返回'''
    img1 = img.copy()
    img2 = rotateImg(img1, 180)
    res1 = getMatch(img1)
    res2 = getMatch(img2)
    return betterMatch(res1, res2)
    # 下面调试用：
    # plotSumAnalyse(img1)
    # plotSumAnalyse(img2)
    # plotSplit(img1)
    # plotSplit(img2)


def iterMatch(img0):
    '''给定一张图片,枚举二值化阈值取最好结果\n
    输出其ISBN字符串结果'''
    img = preDeal(img0)
    ans = []  # 当前最优结果
    for thr in range(5, 255, 10):
        img1 = autoCut(img, thr)
        res = matchFlip(img1)
        ans = betterMatch(ans, res)
        # print(thr, toString(res),toString(ans))
    ans = adjudgeByChecksum(ans)
    return toString(ans)


def autoMatch(img0):
    '''给定一张图片,按Otsu算法选取二值化阈值\n
    输出其ISBN字符串结果(以列表形式)'''
    img = preDeal(img0)
    thr = getThrestHold(toGrey(img))
    img = autoCut(img, thr)
    res = matchFlip(img)
    res = adjudgeByChecksum(res)
    return toString(res)


def Match(img0, thr):
    '''给定一张图片和二值化阈值thr\n
    输出其ISBN字符串结果(以列表形式)'''
    img = preDeal(img0)
    img = autoCut(img, thr)
    res = matchFlip(img)
    res = adjudgeByChecksum(res)
    return toString(res)


# 效果展示
'''
# img = cv2.imread('../imgs/12.jpg')
# print(img.shape)
# prints(autoMatch(img))
# print(iterMatch(img))
# prints(Match(img, 125))
'''
