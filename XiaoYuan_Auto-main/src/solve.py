import cv2
import numpy as np
import pytesseract
from PIL import Image
import pyautogui
import time
import config


class Solve:
    def __init__(self):
        self.left_num_last = 0
        self.right_num_last = 0
        self.error_count = 0
        self.isContinue = False
        self.operation_save = ["<", ">", "="]

    def solve(self, left_number_img, right_number_img, window):
        # 确保输入图像是 uint8 类型
        left_number_img = self.preprocess_image(left_number_img)
        right_number_img = self.preprocess_image(right_number_img)

        # OCR 识别
        left_num = self.recognize_number(left_number_img)
        right_num = self.recognize_number(right_number_img)

        # string to int
        try:
            left_num = int(left_num)
            right_num = int(right_num)
        except ValueError:
            left_num = 0
            right_num = 0

        operation = self.calculate(left_num, right_num)

        if left_num != self.left_num_last or right_num != self.right_num_last:
            self.error_count = 0
            self.draw_flag(operation, window)
            print(f"operation: {operation}")
            if operation == "break":
                self.isContinue = True

        if left_num == self.left_num_last and right_num == self.right_num_last and (left_num != 0 or right_num != 0):
            self.error_count += 1

        if self.error_count > 5:
            for oper in self.operation_save:
                self.draw_flag(oper, window)
                time.sleep(1)

        if left_num == 0 and right_num == 0 and self.isContinue:
            time.sleep(5)
            self.auto_continue(window)
            print("没有找到数字，可能游戏已结束，自动点击继续")
            self.isContinue = False

        self.left_num_last = left_num
        self.right_num_last = right_num

    def preprocess_image(self, img):
        if img.dtype != np.uint8:
            img = (255 * (img - np.min(img)) / np.ptp(img)).astype(np.uint8)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, bin_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
        return bin_img

    def recognize_number(self, img):
        img_pil = Image.fromarray(img)
        num_str = pytesseract.image_to_string(
            img_pil, config="--oem 3 --psm 6 outputbase digits"
        )
        return num_str.strip()

    def calculate(self, left_num, right_num):
        if left_num < right_num:
            return "<"
        elif left_num > right_num:
            return ">"
        elif left_num == right_num and left_num != 0 and right_num != 0:
            return "="
        else:
            return "break"

    def draw_flag(self, operation, window):
        win_box = [window.left, window.top, window.width, window.height]
        win_x, win_y, win_w, win_h = win_box
        scale_x = win_w / config.WINDOW_DEFAULT_WIDTH
        scale_y = win_h / config.WINDOW_DEFAULT_HEIGHT

        if operation == "<":
            self.draw_less_than(win_x, win_y, scale_x, scale_y)
        elif operation == ">":
            self.draw_great_than(win_x, win_y, scale_x, scale_y)
        elif operation == "=":
            self.draw_equal(win_x, win_y, scale_x, scale_y)

    def draw_great_than(self, win_x, win_y, scale_x, scale_y):
        start_x1, start_y1 = win_x + int(300 * scale_x), win_y + int(450 * scale_y)
        end_x1, end_y1 = win_x + int(500 * scale_x), win_y + int(550 * scale_y)
        start_x2, start_y2 = win_x + int(500 * scale_x), win_y + int(550 * scale_y)
        end_x2, end_y2 = win_x + int(300 * scale_x), win_y + int(650 * scale_y)

        pyautogui.moveTo(start_x1, start_y1)
        pyautogui.dragTo(end_x1, end_y1, duration=0.1)  # 加快绘制速度
        pyautogui.moveTo(start_x2, start_y2)
        pyautogui.dragTo(end_x2, end_y2, duration=0.1)

    def draw_less_than(self, win_x, win_y, scale_x, scale_y):
        start_x1, start_y1 = win_x + int(500 * scale_x), win_y + int(450 * scale_y)
        end_x1, end_y1 = win_x + int(300 * scale_x), win_y + int(550 * scale_y)
        start_x2, start_y2 = win_x + int(300 * scale_x), win_y + int(550 * scale_y)
        end_x2, end_y2 = win_x + int(500 * scale_x), win_y + int(650 * scale_y)

        pyautogui.moveTo(start_x1, start_y1)
        pyautogui.dragTo(end_x1, end_y1, duration=0.1)  # 加快绘制速度
        pyautogui.moveTo(start_x2, start_y2)
        pyautogui.dragTo(end_x2, end_y2, duration=0.1)

    def draw_equal(self, win_x, win_y, scale_x, scale_y):
        start_x1, start_y1 = win_x + int(300 * scale_x), win_y + int(650 * scale_y)
        end_x1 = win_x + int(500 * scale_x)

        start_x2, start_y2 = win_x + int(300 * scale_x), win_y + int(700 * scale_y)
        end_x2 = win_x + int(500 * scale_x)

        pyautogui.moveTo(start_x1, start_y1)
        pyautogui.dragTo(end_x1, start_y1, duration=0.1)
        pyautogui.moveTo(start_x2, start_y2)
        pyautogui.dragTo(end_x2, start_y2, duration=0.1)

    def auto_continue(self, window):
        win_box = [window.left, window.top, window.width, window.height]
        win_x, win_y, win_w, win_h = win_box
        scale_x = win_w / config.WINDOW_DEFAULT_WIDTH
        scale_y = win_h / config.WINDOW_DEFAULT_HEIGHT

        pyautogui.click(win_x + int(350 * scale_x), win_y + int(680 * scale_y), duration=0.2)
        pyautogui.click(win_x + int(600 * scale_x), win_y + int(1300 * scale_y), duration=0.2)
        pyautogui.click(win_x + int(400 * scale_x), win_y + int(1170 * scale_y), duration=0.2)
