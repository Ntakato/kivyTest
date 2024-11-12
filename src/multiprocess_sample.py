import multiprocessing
import os
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder

multiprocessing.set_start_method("spawn", force=True)


# サブプロセスで実行する関数
def factorial(n):
    if n < 0:
        raise
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def background_task(queue, n):
    print(f"processID: {os.getpid()}; calculate {n}!")
    time.sleep(1)
    result1 = factorial(n)
    queue.put(f"{n}!: {result1}\n{n + 10}!: ")
    print(f"processID: {os.getpid()}; result = {result1}")
    print(f"processID: {os.getpid()}; calculate {n + 10}!")
    time.sleep(1)
    result2 = factorial(n + 10)
    queue.put(f"{n}!: {result1}\n{n + 10}!: {result2}")
    print(f"processID: {os.getpid()}; result = {result2}")


kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        ToggleButton:
            id: btn1
            group: 'a'
            text: '5, 15'
            on_press: app.button_pressed(5)
        ToggleButton:
            id: btn2
            group: 'a'
            text: '10, 20'
            on_press: app.button_pressed(10)
        ToggleButton:
            id: btn3
            group: 'a'
            text: '20, 30'
            on_press: app.button_pressed(20)
        ToggleButton:
            id: btn4
            group: 'a'
            text: '30, 40'
            on_press: app.button_pressed(30)
    Label:
        id: label
        status: 'Reading'
        text: 'Press Button!'
'''


class SampleApp(App):

    def build(self):
        print(f"processID: {os.getpid()}; this is main process")
        self.queue = multiprocessing.Queue()
        Clock.schedule_interval(self.check_queue, 1)
        return Builder.load_string(kv)

    def button_pressed(self, language):
        self.process = multiprocessing.Process(target=background_task, args=(self.queue, language))
        self.process.start()
        self.root.ids.label.text = "Processing..."
        print(self.process.is_alive())

    def check_queue(self, dt):
        if not self.queue.empty():
            result = self.queue.get()
            self.root.ids.label.text = f"{result}"


if __name__ == '__main__':
    SampleApp().run()
