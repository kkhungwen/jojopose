import pygame
from game_resource import resource_path

class SoundManager:
    def __init__(self):
        # 初始化 Pygame 的聲音系統
        pygame.mixer.init()
        self.sounds = {}  # 保存音效及其對應的音量
        self.musics = {}  # 保存音樂及其對應的音量
        self.load_sound("yesyesyes",resource_path("sound\\YES YES YES.mp3"),0.8)
        self.load_music("moriohchoradio",resource_path("sound\\Morioh Cho Radio.mp3"),0.3)
        self.load_music("torture",resource_path("sound\\canzoni preferite.mp3"),0.3)
        self.load_music("awaken",resource_path("sound\\Awaken.mp3"),0.3)

    def load_sound(self, name, file_path, volume=1.0):
        """加載聲音文件到管理器中，並設置初始音量"""
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(volume)  # 設置初始音量
            self.sounds[name] = {
                'sound': sound,
                'volume': volume  # 保存音量
            }
        except pygame.error as e:
            print(f"無法加載聲音 {file_path}: {e}")

    def play_sound(self, name, loops=0, maxtime=0, fade_ms=0):
        """播放聲音並設置音量"""
        if name in self.sounds:
            sound_data = self.sounds[name]
            sound = sound_data['sound']
            volume = sound_data['volume']
            sound.set_volume(volume)  # 確保播放時使用設置的音量
            sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        else:
            print(f"聲音 {name} 不存在")

    def stop_sound(self, name):
        """停止指定的聲音"""
        if name in self.sounds:
            sound = self.sounds[name]['sound']
            sound.stop()
        else:
            print(f"聲音 {name} 不存在")

    def set_volume(self, name, volume, is_music=False):
        """設置指定聲音或音樂的音量"""
        target = self.musics if is_music else self.sounds
        if name in target:
            if 0.0 <= volume <= 1.0:
                item = target[name]
                if is_music:
                    pygame.mixer.music.set_volume(volume)
                else:
                    item['sound'].set_volume(volume)
                item['volume'] = volume  # 更新保存的音量
            else:
                print("音量必須在 0.0 到 1.0 之間")
        else:
            print(f"{'音樂' if is_music else '聲音'} {name} 不存在")

    def stop_all_sounds(self):
        """停止所有播放中的聲音"""
        pygame.mixer.stop()

    def get_sound(self, name):
        """獲取指定聲音的 Sound 對象"""
        return self.sounds.get(name)

    def load_music(self, name, file_path, volume=0.5):
        """加載音樂文件到管理器中，並設置初始音量"""
        try:
            self.musics[name] = {
                'file_path': file_path,
                'volume': volume  # 保存音量
            }
        except pygame.error as e:
            print(f"無法加載音樂 {file_path}: {e}")

    def play_music(self, name, loops=-1):
        """播放背景音樂"""
        if name in self.musics:
            music_data = self.musics[name]
            file_path = music_data['file_path']
            volume = music_data['volume']
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(loops=loops)
        else:
            print(f"音樂 {name} 不存在")

    def stop_music(self):
        """停止背景音樂"""
        pygame.mixer.music.stop()

    def pause_music(self):
        """暫停背景音樂"""
        pygame.mixer.music.pause()

    def unpause_music(self):
        """恢復播放背景音樂"""
        pygame.mixer.music.unpause()
