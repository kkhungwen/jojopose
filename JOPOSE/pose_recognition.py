import cv2
import numpy as np
from mediapipe import solutions
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import pygame as pg
import utils
import game_resource as gr
from game_resource import resource_path

class PoseRecognition:
    def __init__(self):
        pg.init()  # 初始化 Pygame
        self.cap = cv2.VideoCapture(0)
        self.human_cut_img = None
        self.current_action = ""
        self.sequence = []
        self.threshold = 0.9

        # 初始化 MediaPipe 的 Pose 模型（无 model_path 参数）
        self.mp_pose = solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            enable_segmentation=True,
            min_tracking_confidence=0.5
        )

        self.actions = np.array(["JO1", "JO2", "JO3", "JO4", "JO5", "DEFAULT"])

        # 建立模型
        self.model = Sequential()
        self.model .add(LSTM(64, return_sequences=True, activation="relu", input_shape=(30, 132)))
        self.model .add(LSTM(128, return_sequences=True, activation="relu"))
        self.model .add(LSTM(64, return_sequences=False, activation="relu"))
        self.model .add(Dense(64, activation="relu"))
        self.model .add(Dense(32, activation="relu"))
        self.model .add(Dense(self.actions.shape[0], activation="softmax"))

        self.model .compile(optimizer="Adam", loss="categorical_crossentropy", metrics=["categorical_accuracy"])
        #model.load_weights(resource_path("jojopose_0.h5"))
        self.model .load_weights(resource_path('jojopose_0.h5'))


    def __del__(self):
        self.cap.release()
        pg.quit()  # 退出 Pygame

    def get_player_image(self):
        return self.human_cut_img

    def update(self):
        # 读取视频流
        ret, image = self.cap.read()
        if not ret:
            print("无法读取视频流")
            return
        
        image,results = mediapipe_detection(image,self.pose)

        keypoints = extract_keypoints(results)
        self.sequence.append(keypoints)
        self.sequence = self.sequence[-10:]

        if len(self.sequence) == 10:
            res = self.model.predict(np.expand_dims(self.sequence,axis=0))[0]

            if res[np.argmax(res)]>self.threshold:
                self.current_action = self.actions[np.argmax(res)]


        """ 剪切人类影像 """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 计算 segmentation mask
        if results.segmentation_mask is not None and results.pose_landmarks is not None:
            # 创建一个透明度通道
            alpha_channel = (results.segmentation_mask > 0.1).astype(np.uint8) * 255  # 生成透明度通道
            fg_img = np.dstack((img_rgb, alpha_channel))  # 将RGB图像和透明度通道堆叠在一起
            # 确保图像的维度正确
            fg_img = fg_img.swapaxes(0, 1)  # 交换轴，使其符合 Pygame 的要求
            # 计算新的高度，保持宽高比
            new_height = int((gr.SCREEN_HEIGHT-20) * fg_img.shape[0] / fg_img.shape[1])
            # 调整图像大小
            resized_image = cv2.resize(fg_img, (gr.SCREEN_HEIGHT-20, new_height))
            flipped_image = cv2.flip(resized_image, 0)
            self.human_cut_img = utils.make_surface_rgba(flipped_image)
        else:
            # 创建全透明的背景图像
            transparent_img = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
            transparent_img = transparent_img.swapaxes(0, 1)  # 交换轴
            self.human_cut_img = utils.make_surface_rgba(transparent_img)


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results


def extract_keypoints(result):
    pose = np.array([[res.x,res.y,res.z,res.visibility] for res in result.pose_landmarks.landmark]).flatten() if result.pose_landmarks else np.zeros(33*4)
    return pose