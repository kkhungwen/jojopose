import pygame
import sys
from level_manager import LevelManager  # 管理關卡
from pose_recognition import PoseRecognition  # 姿態辨識
from sound_manager import SoundManager
from ui_manager import UIManager  # 使用者介面
import game_resource as gr
import states

# 初始化Pygame
pygame.init()

class PoseGame:
    def __init__(self):
        # 初始化游戏窗口和模块
        self.screen = pygame.display.set_mode((gr.SCREEN_WIDTH, gr.SCREEN_HEIGHT - 50))
        pygame.display.set_caption('Pose Recognition Game')

        self.clock = pygame.time.Clock()  # 添加 clock 对象
        self.level_manager = LevelManager()
        self.pose_recognition = PoseRecognition()
        self.ui_manager = UIManager(self.screen)
        self.sound_manager = SoundManager()

        # 初始化游戏状态
        self.state = states.MainMenuState()
        self.state.enter_state(self)  # 调用 enter_state

    def change_state(self, new_state):
        self.state.exit_state(self)  # 调用 exit_state
        self.state = new_state
        self.state.enter_state(self)  # 调用 enter_state

    def run(self):
        while True:
            self.clock.tick(60)  # 设置帧率为 60 FPS
            self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.state.handle_events(self, event)

    def update(self):
        self.state.update(self)

    def render(self):
        self.state.render(self)

if __name__ == "__main__":
    game = PoseGame()
    game.run()
