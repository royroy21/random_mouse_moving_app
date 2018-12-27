import time
import random
from threading import Thread

import tkinter
import pyautogui


class Mouse:

    speed = 20
    screen_width = None
    screen_height = None
    limit_move = None
    start_time = None
    click_mouse_interval = 3
    last_position = None

    number_of_clicks = 0
    number_of_turns = 0
    number_of_pixels_moved = 0

    def start(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.center_pointer(pyautogui)

        self.last_position = pyautogui.position()
        self.number_of_pixels_moved = sum(self.last_position)

        is_new_move, next_move = self.move(self.move_down)
        while 1:
            self.reverse_direction(pyautogui)
            is_new_move, next_move = self.move(next_move)
            if is_new_move:
                self.change_speed()
            next_move(pyautogui)

            if self.get_click_mouse_required():
                pyautogui.click()

            self.get_number_of_pixels_moved()

    def get_number_of_pixels_moved(self):
        last_x, last_y = self.last_position
        new_x, new_y = pyautogui.position()

        moved = None
        if last_x != new_x:
            moved = abs(last_x - new_x)
        elif last_y != new_y:
            moved = abs(last_y - new_y)

        if moved:
            self.number_of_pixels_moved += moved

    def start_with_clicks(self):
        self.start_time = time.time()
        self.start()

    def get_click_mouse_required(self):
        if not self.start_time:
            return False

        time_since_start = time.time()
        if (time_since_start - self.start_time) > self.click_mouse_interval:
            self.start_time = time.time()
            self.number_of_clicks += 1
            return True
        else:
            return False

    def center_pointer(self, pyautogui):
        pyautogui.moveTo(self.screen_width / 2, self.screen_height / 2)

    def move(self, current_move):
        moves = [
            self.move_up,
            self.move_down,
            self.move_left,
            self.move_right,
        ]
        if self.limit_move:
            moves.remove(self.limit_move)

        if random.choice(range(10)) == 1:
            next_move = random.choice(moves)
            if next_move != current_move:
                self.number_of_turns += 1
            return True, next_move

        if self.limit_move == current_move:
            self.number_of_turns += 1
            return True, self.get_opposite_direction(current_move)

        return False, current_move

    def get_opposite_direction(self, direction):
        opposite_move_map = {
            self.move_up: self.move_down,
            self.move_down: self.move_up,
            self.move_left: self.move_right,
            self.move_right: self.move_left,
        }
        return opposite_move_map[direction]

    def move_up(self, pyautogui):
        pyautogui.moveRel(None, -self.speed)

    def move_down(self, pyautogui):
        pyautogui.moveRel(None, self.speed)

    def move_left(self, pyautogui):
        pyautogui.moveRel(-self.speed, None)

    def move_right(self, pyautogui):
        pyautogui.moveRel(self.speed, None)

    def change_speed(self):
        self.speed = random.choice([20, 30, 40, 50, 60])

    def reverse_direction(self, pyautogui):
        x, y = pyautogui.position()

        if y < 50:
            self.limit_move = self.get_opposite_direction(self.move_down)
            self.move_down(pyautogui)

        elif y > (self.screen_height - 50):
            self.limit_move = self.get_opposite_direction(self.move_up)
            self.move_up(pyautogui)

        elif x < 50:
            self.limit_move = self.get_opposite_direction(self.move_right)
            self.move_right(pyautogui)

        elif x > (self.screen_width - 50):
            self.limit_move = self.get_opposite_direction(self.move_left)
            self.move_left(pyautogui)


class App:

    window_title = "CazMouse"
    help_text = "To end program move mouse pointer \nto the top left corner of your screen"
    start_button_text = "Start (moving mouse pointer)?"
    start_with_clicks_button_text = "Start (with mouse clicks)?"
    window_background_colour = "#4f4e4e"
    window_size = "300x150"
    label_foreground_colour = "#ffffff"
    stats_background_colour = '#000000'

    mouse_program = Mouse()

    def __init__(self):
        self.window = tkinter.Tk()
        self.mouse_stats = tkinter.StringVar()
        self.mouse_stats.set('')
        self.mouse_pointer_stats = None

    def run(self):
        self.create_window()
        while 1:
            self.window.after(1, self.update_stats)
            self.window.update_idletasks()
            self.window.attributes('-topmost', True)
            self.window.update()
            self.window.attributes('-topmost', False)

    def create_window(self):
        self.center_window()
        self.window.title(self.window_title)
        self.window.configure(background=self.window_background_colour)
        self.window.geometry(self.window_size)

        label = self.create_label(self.help_text)
        label.pack()

        self.mouse_pointer_stats = self.create_stats(self.mouse_stats)
        self.mouse_pointer_stats.pack()

        start_button = self.create_button(
            self.start_button_text,
            self.create_move_mouse_thread,
        )
        start_button.pack()

        start_button_with_clicks = self.create_button(
            self.start_with_clicks_button_text,
            self.create_move_mouse_with_clicks_thread,
        )
        start_button_with_clicks.pack()

    def create_move_mouse_thread(self):
        thread = Thread(target=self.mouse_program.start)
        thread.start()

    def create_move_mouse_with_clicks_thread(self):
        thread = Thread(target=self.mouse_program.start_with_clicks)
        thread.start()

    def update_stats(self):
        self.mouse_stats.set(
            'distance covered: {}\n number of clicks: {}\nnumber of turns: {}'.format(
                self.mouse_program.number_of_pixels_moved,
                self.mouse_program.number_of_clicks,
                self.mouse_program.number_of_turns,
                )
            )
        self.mouse_pointer_stats.update_idletasks()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_label(self, text):
        label = tkinter.Label(self.window, text=text)
        label.configure(
            background=self.window_background_colour,
            foreground=self.label_foreground_colour,
        )
        return label

    def create_stats(self, text):
        label = tkinter.Label(self.window, textvariable=text)
        label.configure(
            padx=100,
            background=self.stats_background_colour,
            foreground=self.label_foreground_colour,
        )
        return label

    def create_button(self, name, command):
        button = tkinter.Button(
            self.window,
            text=name,
            highlightbackground=self.window_background_colour,
            width=25,
            command=command
        )
        return button


if __name__ == "__main__":
    App().run()
