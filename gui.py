from copy import deepcopy

from scanner import *
import tkinter as tk


def make_textmenu(root):
    global the_menu
    the_menu = tk.Menu(root, tearoff=0)
    the_menu.add_command(label="Cut")
    the_menu.add_command(label="Copy")
    the_menu.add_command(label="Paste")
    the_menu.add_separator()
    the_menu.add_command(label="Select all")

def callback_select_all(event):
    # select text after 50ms
    root.after(50, lambda: event.widget.select_range(0, 'end'))

def show_textmenu(event):
    e_widget = event.widget
    the_menu.entryconfigure("Cut", command=lambda: e_widget.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Copy", command=lambda: e_widget.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Paste", command=lambda: e_widget.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Select all", command=lambda: e_widget.select_range(0, 'end'))
    the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)


class CameraWidget:
    def __init__(self, root_widget, camera):
        self.camera = camera
        self.root = root_widget
        self.main_frame = tk.LabelFrame(self.root, text=self.camera.name)

        self.ip_frame = tk.Frame(self.main_frame)
        self.ip_label = tk.Label(self.ip_frame, text='IP')
        self.ip_entry = tk.Entry(self.ip_frame, width=20)
        self.ip_entry.insert(0, f'{self.camera.ip}:{self.camera.port}')
        self.ip_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.ip_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.cloud_frame = tk.Frame(self.main_frame)
        self.cloud_label = tk.Label(self.cloud_frame, text='Cloud ID')
        self.cloud_entry = tk.Entry(self.cloud_frame, width=20)
        self.cloud_entry.insert(0, f'{self.camera.cloud_id}')
        self.cloud_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.cloud_entry.pack(side=tk.LEFT, padx=5, pady=5)

        self.ip_frame.pack()
        self.cloud_frame.pack()

    def pack(self, *args, **kwargs):
        self.main_frame.pack(*args, **kwargs)


response = open('raw_cam_rasponse.bin', 'rb').read()
root = tk.Tk()
make_textmenu(root)
root.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
root.bind_class("Entry", "<Control-a>", callback_select_all)

camera = Camera(response)
camera2 = deepcopy(camera)
camera3 = deepcopy(camera)
camera4 = deepcopy(camera)

camera2.name = 'Cam2 Name'
camera3.name = 'Cam3 Name'
camera4.name = 'Cam4 Name'
cam_widget = CameraWidget(root, camera)
cam_widget2 = CameraWidget(root, camera2)
cam_widget3 = CameraWidget(root, camera3)
cam_widget4 = CameraWidget(root, camera4)
cam_widget.pack(pady=5)
cam_widget2.pack(pady=5)
cam_widget3.pack(pady=5)
cam_widget4.pack(pady=5)


root.mainloop()
