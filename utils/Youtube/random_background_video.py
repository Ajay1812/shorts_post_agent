import random
import os

class RandomVideo:
    def __init__(self):
        self.path = "Data/processed_clips/"
    def select_random_video(self) -> str:
        parts_list = os.listdir(self.path)
        return random.choices(parts_list)[0]
        