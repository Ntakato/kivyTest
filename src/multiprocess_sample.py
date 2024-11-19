import multiprocessing
import os
import time

from kivy.app import App
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView


def factorial(n):
    if n < 0:
        raise
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)


def background_task(queue, n):
    print(f"processID: {os.getpid()}; calculate {n}!")
    time.sleep(0.8)
    result1 = factorial(n)
    queue.put(f"{n}!: {result1}\n{n + 10}!: ")
    print(f"processID: {os.getpid()}; result = {result1}")
    print(f"processID: {os.getpid()}; calculate {n + 10}!")
    time.sleep(0.8)
    result2 = factorial(n + 10)
    queue.put(f"{n}!: {result1}\n{n + 10}!: {result2}")
    print(f"processID: {os.getpid()}; result = {result2}")


def image_processing(x):
    print('start image processing')
    time.sleep(2)
    print('end image processing')
    return x


def processing():
    print("start calculate processing")
    time.sleep(2)
    print("end calculate processing")
    return "success"


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
    Label:
        id: label
        status: 'Reading'
        text: 'Press Button!'
'''


class SampleApp(App):

    images = []

    def build(self):
        print(f"processID: {os.getpid()}; this is main process")
        self.queue = multiprocessing.Queue()
        Clock.schedule_interval(self.check_queue, 0.5)
        return Builder.load_string(kv)

    def button_pressed(self, n):
        self.processing_percentage = 0
        self.process_text = f"Processing\n{self.processing_percentage}%"

        # 操作可能な部分がないフルスクリーンのモーダルを出すことでユーザー操作を制限します
        self.modal = ModalView(size_hint=(.8, .8), auto_dismiss=False)
        self.modal_label = Label(text=self.process_text)
        self.modal.add_widget(self.modal_label)
        self.modal.open()

        self.process = multiprocessing.Process(target=background_task, args=(self.queue, n))
        self.process.start()
        # print(self.process.is_alive())

    def check_queue(self, dt):
        if not self.queue.empty():
            result = self.queue.get()
            self.processing_percentage += 50
            self.process_text = f"Processing\n{self.processing_percentage}%"
            self.modal_label.text = self.process_text
            self.images.append(image_processing(result))
            print(self.images)
            if (len(self.images) == 2):
                final_result = processing()
                self.root.ids.label.text = f"{result}\n{final_result}"
                self.images = []
                self.modal.dismiss()
            # print(self.process.is_alive())


if __name__ == '__main__':
    SampleApp().run()
