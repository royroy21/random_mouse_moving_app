import time
import random
from threading import Thread

import tkinter
import pyautogui


class Mouse:

    pointer_speeds = [5, 10, 20, 30, 40, 50, 60]
    click_mouse_intervals = [1, 2, 3, 4, 5]

    is_active = False
    speed = 20
    screen_width = None
    screen_height = None
    limit_move = None
    mouse_click_timer = None
    last_position = None
    number_of_clicks = 0
    number_of_turns = 0
    number_of_pixels_moved = 0
    time = None

    def _start(self):
        self.is_active = True

        self.screen_width, self.screen_height = pyautogui.size()
        self.center_pointer(pyautogui)

        self.last_position = pyautogui.position()
        self.number_of_pixels_moved = sum(self.last_position)

        is_new_move, next_move = self.move(self.move_down)

        while self.is_active:
            try:
                self.reverse_direction(pyautogui)
                is_new_move, next_move = self.move(next_move)
                if is_new_move:
                    self.change_speed()
                next_move(pyautogui)

                if self.get_click_mouse_required():
                    pyautogui.click()

                self.add_number_of_pixels_moved()
            except pyautogui.FailSafeException:
                self.is_active = False

    def start(self):
        self.mouse_click_timer = None
        self._start()

    def start_with_clicks(self):
        self.mouse_click_timer = time.time()
        self._start()

    def get_click_mouse_required(self):
        if not self.mouse_click_timer:
            return False

        time_since_start = time.time()
        click_mouse_interval = random.choice(self.click_mouse_intervals)
        if (time_since_start - self.mouse_click_timer) > click_mouse_interval:
            self.mouse_click_timer = time.time()
            self.number_of_clicks += 1
            return True
        else:
            return False

    def add_number_of_pixels_moved(self):
        old_x, old_y = self.last_position
        new_x, new_y = pyautogui.position()

        moved = None
        if old_x > new_x:
            moved = old_x - new_x
        elif new_x > old_x:
            moved = new_x - old_x
        elif old_y > new_y:
            moved = old_y - new_y
        elif new_y > old_y:
            moved = new_y - old_y

        if moved:
            self.number_of_pixels_moved += moved
            self.last_position = (new_x, new_y)

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
        self.speed = random.choice(self.pointer_speeds)

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

    root = tkinter.Tk()
    mouse_program = Mouse()
    mouse_pointer_stats = None

    title = "CazMouse"
    help_text = "To end program move mouse pointer \nto the top left corner of your screen"
    start_button_text = "Start (moving mouse pointer)"
    start_with_clicks_button_text = "Start (**with mouse clicks)"

    size = "305x180"
    font = 'Helvetica 16 bold'

    background_colour = "#4f4e4e"
    label_foreground_colour = "#000000"
    stats_foreground_colour = "#b7ffb5"
    stats_background_colour = '#000000'

    start_button = None
    start_button_with_clicks = None

    def __init__(self):
        self.mouse_stats = tkinter.StringVar()
        self.mouse_stats.set('')

    def run(self):
        self.create_window()
        while 1:
            self.root.after(1, self.update_stats)
            self.root.update_idletasks()
            self.root.attributes('-topmost', True)
            self.root.update()
            self.root.attributes('-topmost', False)
            if not self.mouse_program.is_active:
                self.enable_buttons()

    def create_window(self):
        self.center_window()
        self.root.title(self.title)
        self.root.configure(background=self.background_colour)
        self.root.geometry(self.size)

        label = self.create_label(self.help_text)
        label.pack()

        self.mouse_pointer_stats = self.create_stats(self.mouse_stats)
        self.mouse_pointer_stats.pack()

        self.start_button = self.create_button(
            self.start_button_text,
            self.create_move_mouse_thread,
        )
        self.start_button.pack()

        self.start_button_with_clicks = self.create_button(
            self.start_with_clicks_button_text,
            self.create_move_mouse_with_clicks_thread,
        )
        self.start_button_with_clicks.pack()

    def create_move_mouse_thread(self):
        thread = Thread(target=self.mouse_program.start)
        thread.start()
        self.disable_buttons()

    def create_move_mouse_with_clicks_thread(self):
        thread = Thread(target=self.mouse_program.start_with_clicks)
        thread.start()
        self.disable_buttons()

    def _change_buttons_state(self, new_state):
        self.start_button['state'] = new_state
        self.start_button_with_clicks['state'] = new_state
        self.start_button.update_idletasks()
        self.start_button_with_clicks.update_idletasks()

    def disable_buttons(self):
        self._change_buttons_state(tkinter.DISABLED)

    def enable_buttons(self):
        self._change_buttons_state(tkinter.NORMAL)

    def update_stats(self):
        number_of_pixels_moved = \
            f'pixels covered: {self.mouse_program.number_of_pixels_moved}'
        number_of_clicks = \
            f'number of clicks: {self.mouse_program.number_of_clicks}'
        number_of_turns = \
            f'number of turns: {self.mouse_program.number_of_turns}'
        self.mouse_stats.set(
            '{}\n{}\n{}'.format(
                number_of_pixels_moved,
                number_of_clicks,
                number_of_turns,
                )
            )
        self.mouse_pointer_stats.update_idletasks()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_label(self, text):
        label = tkinter.Label(self.root, text=text)
        label.configure(
            background=self.background_colour,
            foreground=self.label_foreground_colour,
            font=self.font,
        )
        return label

    def create_stats(self, text):
        label = tkinter.Label(self.root, textvariable=text)
        label.configure(
            padx=50,
            background=self.stats_background_colour,
            foreground=self.stats_foreground_colour,
            font=self.font,
            borderwidth=10,
            relief=tkinter.SUNKEN,
        )
        return label

    def create_button(self, name, command):
        button = tkinter.Button(
            self.root,
            text=name,
            highlightbackground=self.background_colour,
            width=30,
            command=command,
            font=self.font,
        )
        return button


if __name__ == "__main__":
    App().run()
