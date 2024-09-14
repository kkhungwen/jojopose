import pygame
from level_manager import LevelManager

class GameState:
    def enter_state(self, game):
        pass

    def exit_state(self, game):
        pass

    def handle_events(self, game, event):
        pass

    def update(self, game):
        pass

    def render(self, game):
        pass


class MainMenuState(GameState):
    def enter_state(self, game):
        # 可以在这里初始化一些与主菜单相关的资源
        # 播放音乐
        game.sound_manager.play_music("torture")

    def exit_state(self, game):
        print("Exiting Main Menu State")
        # 在这里释放或清理与主菜单相关的资源

    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.level_manager = LevelManager()
            game.sound_manager.play_music("moriohchoradio")
            game.change_state(PlayingState())

    def render(self, game):
        game.ui_manager.show_main_menu()


class PlayingState(GameState):
    def enter_state(self, game):
        # 初始化游戏中所需的资源或状态
        game.ui_manager.start_render_level(game.level_manager.get_current_level())

    def exit_state(self, game):
        print("Exiting Playing State")
        # 清理或保存游戏进行中的状态

    # Debug
    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:  
            if game.level_manager.is_last_level():
                game.change_state(LevelTransitionState())
 
            else:
                game.change_state(LevelTransitionState())

    def update(self, game):
        game.level_manager.update()
        game.pose_recognition.update()

        action = game.pose_recognition.current_action
        if game.level_manager.check_pose(action):
            game.change_state(LevelTransitionState())  # 切换到过渡动画状态

        elif game.level_manager.is_time_up():
            game.change_state(GameOverState())

    def render(self, game):
        game.ui_manager.render_level(game.level_manager.get_current_level(), game.pose_recognition.get_player_image())


class LevelTransitionState(GameState):
    def __init__(self):
        self.animation_time = 4.0  # 过渡动画的持续时间（秒）
        self.current_time = 0.0

    def enter_state(self, game):
        self.current_time = 0.0
        game.sound_manager.play_sound("yesyesyes")
        game.ui_manager.start_render_leveltransition(game.pose_recognition.get_player_image(),
                                                     game.level_manager.current_level_index)
        # 可以在这里初始化动画资源，例如加载动画图片或音效

    def exit_state(self, game):
        print("Exiting Level Transition State")
        # 清理动画资源

    def handle_events(self, game, event):
        pass  # 通常在动画过程中不会处理事件

    def update(self, game):
        self.current_time += game.clock.get_time() / 1000.0  # 将时间增量添加到当前时间
        if self.current_time >= self.animation_time:
            if game.level_manager.is_last_level():
                game.change_state(VictoryState())
                return
            game.level_manager.load_next_level()
            game.change_state(PlayingState())  # 动画结束后切换到游戏进行状态

    def render(self, game):
        # 在这里绘制动画
        game.ui_manager.render_leveltransition(game.level_manager.get_current_level())


class GameOverState(GameState):
    def enter_state(self, game):
        print("Entering Game Over State")

    def exit_state(self, game):
        print("Exiting Game Over State")

    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.change_state(MainMenuState())

    def render(self, game):
        game.ui_manager.show_game_over()


class VictoryState(GameState):
    def enter_state(self, game):
        game.sound_manager.play_music("awaken")
        game.ui_manager.start_render_victory()

    def exit_state(self, game):
        print("Exiting Victory State")

    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.change_state(MainMenuState())
            game.sound_manager.play_music("torture")

    def render(self, game):
        game.ui_manager.render_victory()

