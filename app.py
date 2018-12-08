import random

import tkinter
import pyautogui


class Mouse:

    speed = 20

    screen_width = None
    screen_height = None
    not_move = None

    def start(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.center_pointer(pyautogui)
        next_move = self.move(self.move_down)
        while 1:
            self.reverse_direction(pyautogui)
            next_move = self.move(next_move)
            next_move(pyautogui)
            self.change_speed()

    def center_pointer(self, pyautogui):
        pyautogui.moveTo(self.screen_width / 2, self.screen_height / 2)

    def move(self, current_move):
        moves = [
            self.move_up,
            self.move_down,
            self.move_left,
            self.move_right,
        ]
        if self.not_move:
            moves.remove(self.not_move)

        if random.choice(range(10)) == 1:
            next_move = random.choice(moves)
            return next_move

        if self.not_move == current_move:
            return self.get_opposite_direction(current_move)

        return current_move

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
        if random.choice(range(5)) == 1:
            self.speed = random.choice(range(20, 50))

    def reverse_direction(self, pyautogui):
        x, y = pyautogui.position()

        if y < 50:
            self.not_move = self.get_opposite_direction(self.move_down)
            self.move_down(pyautogui)

        elif y > (self.screen_height - 50):
            self.not_move = self.get_opposite_direction(self.move_up)
            self.move_up(pyautogui)

        elif x < 50:
            self.not_move = self.get_opposite_direction(self.move_right)
            self.move_right(pyautogui)

        elif x > (self.screen_width - 50):
            self.not_move = self.get_opposite_direction(self.move_left)
            self.move_left(pyautogui)


class App:

    window_title = "Welcome to CazMouse\u2122"
    help_text = "To end program move mouse pointer \nto the top left corner of your screen"
    start_button_text = "Start moving the mouse pointer?"
    window_background_colour = "#4f4e4e"
    window_size = "300x75"
    label_foreground_colour = "#ffffff"

    mouse_program = Mouse()

    def run(self):
        window = self.create_window()
        window.mainloop()

    def create_window(self):
        window = tkinter.Tk()
        self.center_window(window)
        window.title(self.window_title)
        window.configure(background=self.window_background_colour)
        window.geometry(self.window_size)

        label = self.create_label(window, self.help_text)
        label.pack()

        start_button = self.create_button(
            window, self.start_button_text, self.mouse_program.start)
        start_button.pack()

        return window

    def center_window(self, window):
        window.eval(
            'tk::PlaceWindow {} center'.format(
                window.winfo_pathname(window.winfo_id())))

    def create_label(self, window, text):
        label = tkinter.Label(window, text=text)
        label.configure(
            background=self.window_background_colour,
            foreground=self.label_foreground_colour,
        )
        return label

    def create_button(self, window, name, command):
        button = tkinter.Button(
            window,
            text=name,
            highlightbackground=self.window_background_colour,
            width=25,
            command=command
        )
        return button


if __name__ == "__main__":
    App().run()
