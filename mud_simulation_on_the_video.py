import sys

if sys.version_info[0] < 3:
    sys.stderr.write("You need Python 3 or later to run this script!\n")
    sys.exit(1)

import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

# GUI приложение
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.video_path = None
        self.image_path = None
        self.label_first = tk.Label(text="missing file", fg="red")
        self.label_first.grid(row=0, column=1, sticky="nsew")
        self.label_second = tk.Label(text="missing file", fg="red")
        self.label_second.grid(row=1, column=1, sticky="nsew")
        self.list_box = tk.Listbox(selectmode=tk.EXTENDED, height=2)
        self.list_box.grid(row=2, columnspan=4, sticky="nsew")
        self.button_file_first = tk.Button(text="Load video", activeforeground="blue", bg="#4e9a06",
                                           command=lambda: self.add_video())
        self.button_file_first.grid(row=0, column=0, sticky="nsew")
        self.button_file_second = tk.Button(text="Load image", activeforeground="blue", bg="#ffff00",
                                            command=lambda: self.add_image())
        self.button_file_second.grid(row=1, column=0, sticky="nsew")
        self.button_open_file = tk.Button(text="Open file", activeforeground="blue", bg="#ffb841",
                                          command=lambda: self.open_file())
        self.button_open_file.grid(row=3, column=0, sticky="nsew")
        self.button_delete = tk.Button(text="Delete", activeforeground="blue", bg="#ff496c",
                                       command=lambda: self.delete_file())
        self.button_delete.grid(row=3, column=1, sticky="nsew")
        self.button_simulation = tk.Button(text="Simulation", activeforeground="blue", bg="#c0c0c0",
                                           command=lambda: self.simulation())
        self.button_simulation.grid(row=3, column=2, sticky="nsew")
        self.button_exit = tk.Button(text="Exit", activeforeground="blue", bg="#42aaff",
                                     command=lambda: self.exit())
        self.button_exit.grid(row=3, column=3, sticky="nsew")
        self.update_clock()
        self.master.bind('<Delete>', self.delete_file)
        self.master.bind('<Escape>', self.exit)

    # Загрузка видео файла
    def add_video(self):
        video_path = filedialog.askopenfilename(initialdir=dir, title="Select VIDEO",
                                                filetypes=[("ALL files", ' '
                                                            .join('*.' + ext for ext in ("avi", "mp4", "mkv", "flv", "wmv"))),
                                                           ("AVI files", "*.avi"),
                                                           ("MP4 files", "*.mp4"),
                                                           ("MKV files", "*.mkv"),
                                                           ("FLV files", "*.flv"),
                                                           ("WMV files", "*.wmv")])

        # Проверка пути к xml файла на пустоту и на совпадение ранее загруженного xml файла с таким же именем
        if len(video_path):
            """
            Если загружается xml labeled файл, то он добавляется в начало списка и удаляется ранее добавленный
            файл.
            Если загружается xml neuronet файл, то он добавляется в конец списка и удаляется ранее добавленный
            файл.
            """
            if self.video_path:
                self.list_box.delete(0)
            self.list_box.insert(0, video_path)
            self.video_path = video_path
            print(video_path + " LOADED")

    # Загрузка видео файла
    def add_image(self):
        image_path = filedialog.askopenfilename(initialdir=dir, title="Select IMAGE",
                                                filetypes=[("ALL files", ' '
                                                            .join('*.' + ext for ext in ("png", "jpg", "jpeg", "bmp", "gif"))),
                                                           ("PNG files", "*.png"),
                                                           ("JPG files", "*.jpg"),
                                                           ("JPEG files", "*.jpeg"),
                                                           ("BMP files", "*.bmp"),
                                                           ("GIF files", "*.gif")])
        # Проверка пути к xml файла на пустоту и на совпадение ранее загруженного xml файла с таким же именем
        if len(image_path):
            # Проверка на
            if self.image_path:
                self.list_box.delete(tk.END)
            self.list_box.insert(tk.END, image_path)
            self.image_path = image_path
            print(image_path + " LOADED")

    # Открытие файла
    def open_file(self, event=None):
        try:
            selection = self.list_box.curselection()
            if self.list_box.get(selection) == self.video_path:
                print(self.video_path + " OPEN")
                cap = cv2.VideoCapture(self.video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                success, frame = cap.read()
                while success:
                    key = cv2.waitKey(int(1 / fps * 1000))
                    if key == 27:
                        break
                    success, frame = cap.read()
                    cv2.imshow(os.path.basename(self.video_path), frame)
                cap.release()
                cv2.destroyAllWindows()
            if self.list_box.get(selection) == self.image_path:
                print(self.image_path + " OPEN")
                image = cv2.imread(self.image_path)
                cv2.imshow(os.path.basename(self.image_path), image)
                key = cv2.waitKey(0)
                if key == 27:
                    cv2.destroyAllWindows()
        except:
            print("File cannot be opened!")

    # Удаление файла(ов) при нажатии или выделении через shift
    def delete_file(self, event=None):
        select = list(self.list_box.curselection())
        select.reverse()
        for i in select:
            filepath = self.list_box.get(i)
            if filepath == self.video_path:
                self.video_path = None
            elif filepath == self.image_path:
                self.image_path = None
            self.list_box.delete(i)
            print(filepath + " DELETED")

    # Удаление файла(ов) при нажатии или выделении через shift
    def simulation(self, event=None):
        path = os.path.dirname(self.video_path)
        name = os.path.splitext(os.path.basename(self.video_path))[0]
        ext = os.path.splitext(os.path.basename(self.video_path))[1]
        file_video = path + "/" + name + "_new" + ext
        file_data = path + "/" + "data" + ".txt"
        c = 64
        d = 128
        increase = 5
        dirt_masking = False
        record = False
        click = True
        count_click = 0
        cap = cv2.VideoCapture(self.video_path)
        is_frame, image = cap.read()
        width, height = image.shape[:2]
        overlay = cv2.imread(self.image_path)
        overlay = cv2.resize(overlay, (height, width))
        overlay = cv2.GaussianBlur(overlay, (0, 0), 1.8)
        overlay_copy = overlay.copy()
        a = np.min(overlay)
        b = np.max(overlay)
        threshold = b
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(file_video, fourcc, cap.get(cv2.CAP_PROP_FPS), (height, width))
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(name, 0, 0)
        if not is_frame:
            print("video not found")
        dt = int(1/cap.get(cv2.CAP_PROP_FPS)*1000)
        while True:
            modify = False
            key = cv2.waitKey(dt)
            if key == ord('r'):
                ~click
                if click:
                    try:
                        count = 0
                        data_from_file = np.uint8([])
                        file = open(file_data, "r")
                        if os.stat(file_data).st_size:
                            for line in file:
                                if not line == "\n":
                                    data_from_file = np.append(data_from_file, np.array([int(s) for s in line.split()
                                                                                         if s.isdigit()]))
                                    print("pressed R, Read from {}, threshold = {data[0]}, c = {data[1]}, d = {data[2]}"
                                          .format(file_data, data=data_from_file))
                                    count += 3
                            file.close()
                            click = False
                        else:
                            print("FILE is EMPTY!")
                    except IOError:
                        print("Could not OPEN FILE!")
                else:
                    threshold = data_from_file[count_click]
                    c = data_from_file[1+count_click]
                    d = data_from_file[2+count_click]
                    print("pressed double R, read from DATA, threshold = {}, c = {}, d = {}".format(threshold, c, d))
                    count_click += 3
                    if count_click >= len(data_from_file):
                        count_click = 0
            if key == ord('x'):
                dirt_masking ^= 1
                if dirt_masking:
                    print("pressed x, DIRTY")
                else:
                    print("pressed x, CLEAN")
            if key == 27:
                print("pressed BREAK")
                break
            if key == 32:
                print("pressed PAUSE")
                key = cv2.waitKey(0)
            if key == ord('w') and threshold <= 255-increase:
                threshold += increase
                print("pressed w, threshold = ", threshold)
            if key == ord('s') and threshold >= 0+increase:
                threshold -= increase
                print("pressed s, threshold =", threshold)
            if key == ord('d') and d <= 255 - increase:
                modify = True
                d += increase
                print("pressed d, d =", d)
            if key == ord('a') and d - increase > c:
                modify = True
                d -= increase
                print("pressed a, d = ", d)
            if key == ord('g') and c + increase < d:
                modify = True
                c += increase
                print("pressed g, c =", c)
            if key == ord('f') and c >= 0 + increase:
                modify = True
                c -= increase
                print("pressed f, c = ", c)
            if modify:
                overlay = ((d - c) / (b - a)) * (overlay_copy - a) + c
                overlay = overlay.astype(np.uint8)
            if dirt_masking:
                # image32 = image.astype(np.float32)
                #rows,cols,channels = overlay.shape
                # roi = output[0:rows, 0:cols ]
                # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(overlay, threshold, threshold, cv2.THRESH_TRUNC)
                # mask = np.array(mask, dtype=np.float32)
                mask = threshold - mask
                # mask = np.array(mask, dtype=np.uint8)
                # cv2.imshow("0" , roi)
                # cv2.waitKey(0)
                # mask_inv = cv2.bitwise_not(mask)
                # roi = np.array(roi, dtype=np.float32)
                # overlay = np.array(overlay, dtype=np.float32)
                # img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
                # img2_fg = cv2.bitwise_and(overlay,overlay,mask = mask)
                # img2_fg -= threshold
                dst = cv2.subtract(image, mask)
                # dst = image - mask
                # np.clip(dst, 0,255, out=dst)
                # dst = dst.astype('uint8')
                # dst = np.array(dst, dtype=np.uint8)
                # output[0:rows, 0:cols ] = dst
                # cv2.addWeighted(output, 0.5, image, 0.5, 0, image)
            else:
                dst = image
            if record:
                video.write(dst)
            cv2.imshow("0", dst)
            if key == 13:
                record ^= 1
                if record:
                    video.write(dst)
                    print("pressed ENTER, video recording to {}".format(file_video))
                else:
                    video.release()
                    data_to_file = np.uint8([threshold, c, d])
                    file = open(file_data, "a")
                    file.write(' '.join(["{}".format(item) for item in data_to_file]))
                    file.write("\n")
                    file.close()
                    print("pressed ENTER, video stop recorded; data recorded to {}, parameters: threshold = {data[0]}, "
                          "c = {data[1]}, d = {data[2]}".format(file_data, data=data_to_file))
                    click = True
            is_frame, image = cap.read()
            if not is_frame:
                cap.release()
                cap.open(self.video_path)
                is_frame, image = cap.read()
                if not is_frame:
                    break

    # Выход из программы
    def exit(self, event=None):
        ask = messagebox.askquestion(title="Exit", message="Are you sure to quit?")
        if ask == "yes":
            self.master.destroy()
            self.master.quit()

    def update_clock(self):
        """
        Таймер, который проверяет через каждые (несколько) миллисекунд на наличие двух загруженных xml файлов.
        Если оба xml файла не загружены, то кнопка button_open_file недоступна.
        """
        if self.video_path:
            self.label_first.config(text=os.path.basename(self.video_path) + " LOADED", fg="blue")
        else:
            self.label_first.config(text="missing file", fg="red")

        if self.image_path:
            self.label_second.config(text=os.path.basename(self.image_path) + " LOADED", fg="blue")
        else:
            self.label_second.config(text="missing file", fg="red")

        if self.list_box.size() == 2:
            self.button_simulation.config(state=tk.ACTIVE, bg="#c0c0c0")
            self.master.bind('<s>', self.simulation)
        else:
            self.button_simulation.config(state=tk.DISABLED, bg="white")
            self.master.unbind('<s>')
        self.after(100, self.update_clock)

def main():
    root = tk.Tk()
    # Ширина экрана
    width = root.winfo_screenwidth()
    # Высота экрана
    height = root.winfo_screenheight()
    # Середина экрана
    width = width // 2
    height = height // 2
    # Смещение от середины
    width = width - 200
    height = height - 200
    root.title("Choose FILES")
    # Размеры GUI приложения
    root.geometry("400x200+{}+{}".format(width, height))
    # Масштабирование
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)
    Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()



