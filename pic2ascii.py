#!/usr/bin/env python
# -*- coding: utf-8 -*-
from StringIO import StringIO

from PIL import Image  # 图像处理模块
import requests

ASCII_CHARS = [' ', '#', '?', '%', '.', '+', '.', '*', ':', ',', '@']


# 压缩图片
def scale_image(image, new_width=60):
    (original_width, original_height) = image.size  # 获取原图尺寸
    aspect_ratio = original_height / float(original_width) * 0.5  # 计算高宽比，因为输出文本有2倍行距，所以乘0.5维持高宽比
    new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image


# 灰度模式
def convert_to_grayscale(image):
    return image.convert('L')  # 调用image对象自己的.convert()方法


def map_pixels_to_ascii_chars(image, range_width=25):
    # 将每个像素根据其灰度值映射为一个字符，每个字符对应25个灰度值
    pixels_in_image = list(image.getdata())  # 获取原图灰度值列表
    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    # 对于每个像素点，将其灰度值转换为列表ASCII_CHARS的索引
    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, new_width=60):
    image = scale_image(image, new_width)  # 调用scale_image()函数，压缩图片
    image = convert_to_grayscale(image)  # convert_to_grayscale()函数，转换为灰度图

    pixels_to_chars = map_pixels_to_ascii_chars(image)  # 映射至字符集
    len_pixels_to_chars = len(pixels_to_chars)  # 获取字符集长度

    image_ascii = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def handle_image_conversion(image_filepath, new_width=60):
    image = Image.open(image_filepath)  # Image.open()打开源图片
    image_ascii = convert_image_to_ascii(image, new_width)  # 调用上面的convert_image_to_ascii()函数
    print(image_ascii)  # 输出字符画


response = requests.get("http://img4.duitang.com/uploads/blog/201309/27/20130927160338_z4z8i.jpeg")
img = Image.open(StringIO(response.content))
print convert_image_to_ascii(img, 200)
