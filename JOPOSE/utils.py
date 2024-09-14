import numpy as np
import pygame as pg
import cv2

def make_surface_rgba(array):
    """返回一个由 [w, h, 4] numpy 数组构成的表面，支持每像素透明度"""
    shape = array.shape
    if len(shape) != 3 or shape[2] != 4:
        raise ValueError("Array must be RGBA format")

    # 创建一个与数组宽高相同且支持每像素 alpha 的表面
    surface = pg.Surface(shape[0:2], pg.SRCALPHA, 32)

    # 将 RGB 部分拷贝到表面上
    pg.pixelcopy.array_to_surface(surface, array[:, :, 0:3])

    # 将 alpha 部分拷贝到表面上
    surface_alpha = np.array(surface.get_view('A'), copy=False)
    surface_alpha[:, :] = array[:, :, 3]

    return surface

def scale_image(image, target_height):
    # 将 Pygame Surface 转换为 numpy 数组
    image_np = pg.surfarray.array3d(image)
    
    # 调整图像的通道顺序
    image_np = np.transpose(image_np, (1, 0, 2))
    
    # 计算新的宽度，保持宽高比
    height, width, _ = image_np.shape
    new_width = int((target_height * width) / height)
    
    # 调整图像大小
    resized_image_np = cv2.resize(image_np, (new_width, target_height))
    
    # 将 numpy 数组转换回 Pygame Surface
    resized_image = pg.surfarray.make_surface(np.transpose(resized_image_np, (1, 0, 2)))
    
    return resized_image