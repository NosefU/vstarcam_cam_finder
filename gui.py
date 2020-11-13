from copy import deepcopy

from scanner import *
import tkinter as tk


class CameraWidget:
    def __init__(self, root_widget, camera):
        self.camera = camera
        self.root = root_widget
        self.frame = tk.LabelFrame(self.root, text=self.camera.name)
        self.ip_label = tk.Label(self.frame, text='IP')
        self.ip_entry = tk.Entry(self.frame, width=20)
        self.ip_entry.insert(0, f'{self.camera.ip}:{self.camera.port}')


        self.ip_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.ip_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)


response = open('raw_cam_rasponse.bin', 'rb').read()
root = tk.Tk()
camera = Camera(response)
camera2 = deepcopy(camera)
camera2.name = 'Cam2 Name'
cam_widget = CameraWidget(root, camera)
cam_widget2 = CameraWidget(root, camera2)
cam_widget.pack(pady=5)
cam_widget2.pack(pady=5)


root.mainloop()
