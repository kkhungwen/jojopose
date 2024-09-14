import time
import game_resource as gr

class Level:
    def __init__(self, background_image, target_pose, action_name):
        self.action_name = action_name
        self.background_image = background_image
        self.target_pose = target_pose
        self.start_time = time.time()
        self.time_limit = 200  # 每個關卡的時間限制（秒）

    def is_time_up(self):
        return time.time() - self.start_time > self.time_limit

class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level_index = 0
        self.load_levels()

    def load_levels(self):
        # 載入關卡，可以從文件或其他來源獲取數據
        self.levels.append(Level(gr.BG0, gr.JO1, "JO1"))
        self.levels.append(Level(gr.BG1, gr.JO2, "JO2"))
        self.levels.append(Level(gr.BG4, gr.JO3, "JO3"))
        self.levels.append(Level(gr.BG7, gr.JO4, "JO4"))
        self.levels.append(Level(gr.BG6, gr.JO5, "JO5"))
        # 可以繼續添加更多關卡

    def update(self):
        # 更新當前關卡的狀態
        current_level = self.get_current_level()
        if current_level.is_time_up():
            print("Time's up for the current level.")

    def get_current_level(self):
        return self.levels[self.current_level_index]

    def check_pose(self, action):
        current_level = self.get_current_level()
        if action == current_level.action_name:
            return True
        return False

    def is_last_level(self):
        return self.current_level_index == len(self.levels) - 1

    def load_next_level(self):
        if not self.is_last_level():
            self.current_level_index += 1
            print(f"Loading level {self.current_level_index + 1}")
        else:
            print("All levels completed.")

    def is_time_up(self):
        return self.get_current_level().is_time_up()