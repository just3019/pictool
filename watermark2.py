# -*- coding: utf-8 -*-
import os
import random
import threading
import time
import tkinter
from tkinter import *
from tkinter.filedialog import askdirectory

from PIL import Image, ImageDraw, ImageFont

LOCK = threading.Lock()

# 指定要使用的字体和大小；/Library/Fonts/是macOS字体目录；Linux的字体目录是/usr/share/fonts/
# font = ImageFont.truetype(font="/Library/Fonts/Arial.ttf", size=24)
font = ImageFont.truetype(font="C:\WINDOWS\Fonts\Arial.ttf", size=48)


# image: 图片  text：要添加的文本 font：字体
def add_text_to_image(image, text, font=font):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = (rgba_image.size[0] - text_size_x - 10, rgba_image.size[1] - text_size_y - 10)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(255, 255, 255, 100))
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text


def openfile():
    path_ = askdirectory()
    log(path_)
    global choose_path
    choose_path = path_


def ui():
    root = tkinter.Tk()
    root.title('打水印工具')
    root.geometry('600x600')
    global btn_file
    btn_file = Button(root, text='选择路径', command=openfile)
    btn_file.pack()
    fm1 = Frame(root)
    fm1.pack(fill=X)
    label1 = Label(fm1, text='开始时间：')
    global entry1
    entry1 = Entry(fm1, width=15)
    label2 = Label(fm1, text='结束时间：')
    global entry2
    entry2 = Entry(fm1, width=15)
    label1.pack(side=LEFT)
    entry1.pack(side=LEFT)
    label2.pack(side=LEFT)
    entry2.pack(side=LEFT)

    global s1
    s1 = Scrollbar(root)
    s1.pack(side=RIGHT, fill=Y)
    global textView
    textView = Text(root, width=400, height=30, yscrollcommand=s1.set)
    label3 = Label(root, text='日志输出')
    label3.pack()
    textView.pack(expand=YES, fill=X)
    s1.config(command=textView.yview)
    btn = Button(root, text='开始', command=submit)
    btn.pack(expand=YES, fill=X)
    root.mainloop()


def submit():
    LOCK.acquire()
    if choose_path is None or entry1 is None or entry2 is None or choose_path == "" or entry1 == "" or entry2 == "":
        log("先填写参数")
        raise RuntimeError("先填写参数")
    en1 = entry1.get()
    en2 = entry2.get()
    print(en1 + " " + en2)
    list = os.listdir(choose_path)
    for i in range(0, len(list)):
        if list[i] == ".DS_Store":
            continue
        start_time = date_to_timestamp(en1)
        end_time = date_to_timestamp(en2)
        result_time = random.randint(start_time, end_time)
        re_time = timestamp_to_date(result_time)
        path = os.path.join(choose_path, list[i])
        log(path)
        im_before = Image.open(path)
        im_after = add_text_to_image(im_before, re_time)
        im = im_after.convert("RGB")
        after_url = choose_path + "/watermask" + list[i] + ".jpg"
        log(after_url)
        im.save(after_url)
    LOCK.release()


def log(s):
    print(s)
    textView.insert(END, '%s\n' % s)
    textView.update()
    textView.see(END)


# 将时间字符串转换为10位时间戳，时间字符串默认为2017-10-01 13:37:04格式
def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


# 将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


if __name__ == '__main__':
    ui()
