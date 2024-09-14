import pygame
import game_resource as gr
import time
from flash_text import FlashingText
import image_animation

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.flashing_text = FlashingText(self.font)
        self.snaps = {}
        self.victory_start_time = 0
        self.victory_display_duration = 1  # 每张图片显示的时间（秒）
        self.victory_images = []
        self.current_image_index = 0

    def show_main_menu(self):
        self.screen.blit(gr.WP, (0, 0))
        self.flashing_text.update(self.screen,"Press SPACE to start", (gr.SCREEN_WIDTH / 2, 700), (255, 30, 210), (255, 120, 190))  # Update the flash state

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (300, 250))
        retry_text = self.font.render("Press SPACE to retry", True, (255, 255, 255))
        self.screen.blit(retry_text, (150, 350))

    def start_render_victory(self):
        self.victory_start_time = time.time()
        self.victory_images = list(self.snaps.values())
        self.current_image_index = 0
        self.animations = []
        self.effect_animations = []

        self.dondondon_image = gr.DONDONDON
        self.dondondon_shake = image_animation.ShakeAnimation(20,3)
        self.dondondon_animation_0 = image_animation.Image_Animation(self.dondondon_image,(900,150))
        self.dondondon_animation_0.add_animation(self.dondondon_shake)
        self.dondondon_shake = image_animation.ShakeAnimation(20,3)
        self.dondondon_animation_1 = image_animation.Image_Animation(self.dondondon_image,(100,200))
        self.dondondon_animation_1.add_animation(self.dondondon_shake)
        self.dondondon_shake = image_animation.ShakeAnimation(20,3)
        self.dondondon_animation_2 = image_animation.Image_Animation(self.dondondon_image,(500,100))
        self.dondondon_animation_2.add_animation(self.dondondon_shake)

        self.effect_animations.extend([self.dondondon_animation_0,self.dondondon_animation_1,self.dondondon_animation_2])

    def render_victory(self):
        self.screen.fill((0, 0, 0))

        # 显示当前图片
        elapsed_time = time.time() - self.victory_start_time
        if self.current_image_index < len(self.victory_images):
            if elapsed_time >= self.victory_display_duration * (self.current_image_index + 1):
                image = self.victory_images[self.current_image_index]
                x_position = -300 + self.current_image_index * 250
                self.screen.blit(image, (x_position, 0))
                self.current_image_index += 1

                self.snap_image= image
                self.snap_fadein = image_animation.ScaleAnimation(5,0,1)
                self.snap_animation = image_animation.Image_Animation(self.snap_image,(x_position, 0))
                self.snap_animation.add_animation(self.snap_fadein)
                
                self.animations.append(self.snap_animation)
        
        # play animation
        for animation in self.animations:
            animation.update(self.screen)

        for animation in self.effect_animations:
            animation.update(self.screen)

        continue_text = self.font.render("Press SPACE to continue", True, (255, 255, 255))
        self.screen.blit(continue_text, (gr.SCREEN_WIDTH / 2, 700))
        

    def start_render_level(self,level,):
        # Target pose animation
        self.target_pose_image = level.target_pose
        self.target_pose_fadein = image_animation.ScaleAnimation(5,0,1)
        self.target_pose_image_animation = image_animation.Image_Animation(self.target_pose_image,(150,150))
        self.target_pose_image_animation.add_animation(self.target_pose_fadein)
        
        self.level_animations = []
        self.level_animations.append(self.target_pose_image_animation)


    def render_level(self, level, player_image):
        background = level.background_image
        
        self.screen.blit(background, (0, 0))
        self.screen.blit(player_image, (gr.SCREEN_WIDTH / 4 * 3 - gr.SCREEN_WIDTH / 2, 10))  # 显示在右侧

        # play animation
        for animation in self.level_animations:
            animation.update(self.screen)

    def start_render_leveltransition(self, player_image,level_index):
        self.snaps[level_index] = player_image

        self.dondondon_image = gr.DONDONDON
        self.dondondon_shake = image_animation.ShakeAnimation(20,3)
        self.dondondon_animation = image_animation.Image_Animation(self.dondondon_image,(900,150))
        self.dondondon_animation.add_animation(self.dondondon_shake)

        self.line_effect_images = [gr.LINE_EFFECT_0,gr.LINE_EFFECT_1]
        self.line_effect_cycle = image_animation.ImageCycleAnimation(self.line_effect_images,0.1)
        self.line_effect_animation = image_animation.Image_Animation(gr.LINE_EFFECT_0,(0,0))
        self.line_effect_animation.add_animation(self.line_effect_cycle)

        self.player_snap_image = player_image


    def render_leveltransition(self, level):
        background = level.background_image
        target_pose = level.target_pose

        self.screen.blit(background, (0, 0))
        self.screen.blit(self.player_snap_image, (gr.SCREEN_WIDTH / 4 * 3 - gr.SCREEN_WIDTH / 2, 10))  # 显示在右侧
        self.screen.blit(target_pose, (150, 150))  # 显示在左侧

        self.line_effect_animation.update(self.screen)
        self.dondondon_animation.update(self.screen)


 
 
        
