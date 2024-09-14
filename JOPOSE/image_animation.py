import pygame
import time
import random

# 定义基本的 Image_Animation 类
class Image_Animation:
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.original_image = self.image.copy()  # 保存原始图像以便缩放
        self.animations = []

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def add_animation(self, animation):
        self.animations.append(animation)

    def update(self, surface):
        for animation in self.animations:
            animation.update(self)
        
        self.draw(surface)


# 定义动画基类
class Animation:
    def update(self, image_animation):
        raise NotImplementedError("Subclasses should implement this method")

# 淡出动画
class FadeOutAnimation(Animation):
    def __init__(self, fade_speed):
        self.fade_speed = fade_speed
        self.alpha = 255

    def update(self, image_animation):
        self.alpha -= self.fade_speed
        if self.alpha < 0:
            self.alpha = 0
        image_animation.image.set_alpha(self.alpha)

# 缩放动画
class ScaleAnimation(Animation):
    def __init__(self, scale_time, scale_start, scale_end):
        self.scale_speed = (float(scale_end) - float(scale_start))/scale_time
        self.scale_factor = scale_start
        self.scale_start = scale_start
        self.scale_end = scale_end

    def update(self, image_animation):
        self.scale_factor += self.scale_speed
        if((self.scale_start<self.scale_end and self.scale_factor> self.scale_end)or (self.scale_start>self.scale_end and self.scale_factor< self.scale_end)):
            self.scale_factor = self.scale_end

        if self.scale_factor < 0.1:
            self.scale_factor = 0.1
        new_size = (int(image_animation.original_image.get_width() * self.scale_factor), 
                    int(image_animation.original_image.get_height() * self.scale_factor))
        image_animation.image = pygame.transform.scale(image_animation.original_image, new_size)

# 平移动画
class MoveToAnimation(Animation):
    def __init__(self, target_position, duration):
        self.target_position = target_position
        self.duration = duration
        self.start_time = time.time()

    def update(self, image_animation):
        elapsed_time = time.time() - self.start_time
        progress = min(elapsed_time / self.duration, 1.0)
        new_x = image_animation.position[0] + (self.target_position[0] - image_animation.position[0]) * progress
        new_y = image_animation.position[1] + (self.target_position[1] - image_animation.position[1]) * progress
        image_animation.position = (new_x, new_y)


class ShakeAnimation(Animation):
    def __init__(self, intensity, duration):
        self.intensity = intensity  # 抖动的强度（像素范围）
        self.duration = duration  # 抖动的持续时间
        self.start_time = time.time()

    def update(self, image_animation):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.duration:
            # 随机生成一个偏移量
            offset_x = random.randint(-self.intensity, self.intensity)
            offset_y = random.randint(-self.intensity, self.intensity)
            # 更新图像的位置
            image_animation.position = (
                image_animation.position[0] + offset_x,
                image_animation.position[1] + offset_y
            )
        else:
            # 动画结束后，将图像恢复到初始位置
            self.start_time = time.time()  # 重置时间以便可以重复使用

class ImageCycleAnimation(Animation):
    def __init__(self, images, cycle_time):
        self.images = images  # 图像列表
        self.cycle_time = cycle_time  # 每张图像显示的时间
        self.current_image_index = 0
        self.last_update_time = time.time()

    def update(self, image_animation):
        current_time = time.time()
        if current_time - self.last_update_time > self.cycle_time:
            # 更新到下一个图像
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            image_animation.image = self.images[self.current_image_index]
            self.last_update_time = current_time
