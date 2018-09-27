import os
import random
import time

from PIL import Image, ImageDraw, ImageFont

# font = ImageFont.truetype(font="C:\WINDOWS\Fonts\Arial.ttf", size=100)
font = ImageFont.truetype(font="/Library/Fonts/Arial.ttf", size=48)


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


# 将10位时间戳转换为时间字符串，默认为2017-10-01 13:37:04格式
def timestamp_to_date(time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.localtime(time_stamp)
    str_date = time.strftime(format_string, time_array)
    return str_date


# image: 图片  text：要添加的文本 font：字体
def add_text_to_image(image, text, font=font):
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    # 设置文本文字位置
    text_xy = (rgba_image.size[0] - text_size_x - 10, rgba_image.size[1] - text_size_y - 10)
    # 设置文本颜色和透明度
    image_draw.text(text_xy, text, font=font, fill=(200, 200, 200, 200))
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_text


if __name__ == '__main__':

    choose_path = "/Users/demon/Desktop/imgs"
    list = os.listdir(choose_path)
    for i in range(0, len(list)):
        if list[i] == ".DS_Store":
            continue
        start_time = date_to_timestamp("2018-09-09 00:00:00")
        end_time = date_to_timestamp("2018-09-19 00:00:00")
        result_time = random.randint(start_time, end_time)
        re_time = timestamp_to_date(result_time)
        print(re_time)
        path = os.path.join(choose_path, list[i])
        print(path)
        im_before = Image.open(path)
        im_after = add_text_to_image(im_before, re_time)
        im = im_after.convert("RGB")
        after_url = choose_path + "/watermask" + list[i] + ".jpg"
        print(after_url)
        im.save(after_url)
