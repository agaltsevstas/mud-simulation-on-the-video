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
        self.video_name = None
        self.image_name = None
        self.data = None
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
        self.master.bind('<v>', self.add_video)
        self.master.bind('<i>', self.add_image)
        self.master.bind('<o>', self.open_file)
        self.master.bind('<Delete>', self.delete_file)
        self.master.bind('<Escape>', self.exit)

    # Загрузка видео файла
    def add_video(self, event=None):
        video_path = filedialog.askopenfilename(initialdir=dir, title="Select VIDEO",
                                                filetypes=[("ALL files", ' '
                                                            .join('*.' + ext for ext in ("avi", "mp4", "mkv", "flv", "wmv"))),
                                                           ("AVI files", "*.avi"),
                                                           ("MP4 files", "*.mp4"),
                                                           ("MKV files", "*.mkv"),
                                                           ("FLV files", "*.flv"),
                                                           ("WMV files", "*.wmv")])

        # Проверка пути к видеофайлу на пустоту
        if len(video_path):
            # Проверка на совпадение ранее загруженного видеофайла файла с таким же именем
            if self.video_path:
                self.list_box.delete(0)
            self.list_box.insert(0, video_path)
            self.video_path = video_path
            self.video_name = os.path.basename(self.video_path)
            print(video_path + " loaded")

    # Загрузка изображения
    def add_image(self, event=None):
        image_path = filedialog.askopenfilename(initialdir=dir, title="Select IMAGE",
                                                filetypes=[("ALL files", ' '
                                                            .join('*.' + ext for ext in ("png", "jpg", "jpeg", "bmp", "gif"))),
                                                           ("PNG files", "*.png"),
                                                           ("JPG files", "*.jpg"),
                                                           ("JPEG files", "*.jpeg"),
                                                           ("BMP files", "*.bmp"),
                                                           ("GIF files", "*.gif")])
        # Проверка пути к изображению
        if len(image_path):
            # Проверка на совпадение ранее загруженного изображения с таким же именем
            if self.image_path:
                self.list_box.delete(tk.END)
            self.list_box.insert(tk.END, image_path)
            self.image_path = image_path
            self.image_name = os.path.basename(self.image_path)
            print(image_path + " loaded")

    # Открытие файла
    def open_file(self, event=None):
        try:
            selection = self.list_box.curselection()
            if self.list_box.get(selection) == self.video_path:
                print(self.video_path + " opening")
                cap = cv2.VideoCapture(self.video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                success, frame = cap.read()
                while success:
                    key = cv2.waitKey(int(1 / fps * 1000))
                    if key == 27:
                        break
                    success, frame = cap.read()
                    cv2.imshow(self.video_name, frame)
                cap.release()
                cv2.destroyAllWindows()
            if self.list_box.get(selection) == self.image_path:
                print(self.image_path + " opening")
                image = cv2.imread(self.image_path)
                cv2.imshow(self.image_name, image)
                key = cv2.waitKey(0)
                if key == 27:
                    cv2.destroyAllWindows()
        except:
            messagebox.showerror("No file selected", "Select a file from the list")
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
            print(filepath + " deleted")

    def read_data(self, data_file):
        self.data = np.uint8([])
        try:
            file = open(data_file, "r")
            # Чтение данных
            if os.stat(data_file).st_size:
                for line in file:
                    if not line == "\n":
                        self.data = np.append(self.data, np.array([int(s) for s in line.split() if s.isdigit()]))
                file.close()
            else:
                print("File is empty!")
        except IOError:
            print("Could not open file!")

    # Симуляция грязи на видеофайле в режиме оннлайн
    def simulation(self, event=None):
        # Путь к видеофайлу
        path = os.path.dirname(self.video_path)
        # Путь к новому видео
        mud_video_path = path + "/" + "mud_" + self.video_name
        # Название нового видео
        mud_video_name = "mud_" + self.video_name
        # Текстовый файл, в котором будут храниться данные
        data_file = path + "/" + "data" + ".txt"
        self.read_data(data_file)
        step = 5
        video_brightness = 128
        mud_brightness = 64
        do_mud_masking = False
        can_video_recording = False
        do_hide_text = False
        record_counter = 0
        cap = cv2.VideoCapture(self.video_path)
        # Чтение кадра из видеофайла
        is_frame, frame = cap.read()
        # Ширина и высота кадра
        frame_width, frame_height = frame.shape[:2]
        # Подготовка изображения к наложению на видеофайл
        image_overlay = cv2.imread(self.image_path)
        image_overlay = cv2.resize(image_overlay, (frame_height, frame_width))
        # Размытие наложенного изображения по Гауссиану
        image_overlay = cv2.GaussianBlur(image_overlay, (0, 0), 1.8)
        image_overlay_copy = image_overlay.copy()
        # Минимальное значение пикселя на кадре
        min_pixel = np.min(image_overlay)
        # Максимальное значение пикселя на кадре
        max_pixel = np.max(image_overlay)
        threshold = max_pixel
        # Кодек видео
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video = cv2.VideoWriter(mud_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_height, frame_width))
        # Размер окна и расположение
        cv2.namedWindow(mud_video_name, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(mud_video_name, 0, 0)
        # Проверка на открытие видеофайла
        if not is_frame:
            print("Video not found")
        dt = int(1 / cap.get(cv2.CAP_PROP_FPS) * 1000)
        while True:
            modify = False
            key = cv2.waitKey(dt)
            # Загрузка данных из текстового файла
            if key == 13:
                threshold = self.data[record_counter]
                mud_brightness = self.data[1 + record_counter]
                video_brightness = self.data[2 + record_counter]
                print("Pressed ENTER, Read from {}, threshold = {}, "
                      "c = {}, d = {}"
                      .format(data_file, threshold, mud_brightness, video_brightness))
                record_counter += 3
                if record_counter >= len(self.data):
                    record_counter = 0
                modify = True
            # Спрятать / показать надпись на видео
            if key == ord('h'):
                do_hide_text ^= 1
                if do_hide_text:
                    print("Pressed H, the text is hidden")
                else:
                    print("Pressed H, the text is visible")
            # Наложение / удаление грязи
            if key == ord('x'):
                do_mud_masking ^= 1
                if do_mud_masking:
                    print("Pressed X, mud")
                else:
                    print("Pressed X, clean")
            # Выход
            if key == 27:
                print("Pressed ESC")
                break
            # Пауза
            if key == 32:
                print("Pressed pause")
                key = cv2.waitKey(0)
            # Увеличение порога яркости
            if key == ord('w') and threshold <= 255 - step:
                threshold += step
                print("Pressed W, threshold = ", threshold)
            # Уменьшение порога яркости
            if key == ord('s') and threshold >= 0 + step:
                threshold -= step
                print("Pressed S, threshold =", threshold)
            # Увеличение яркости видео
            if key == ord('d') and video_brightness <= 255 - step:
                video_brightness += step
                modify = True
                print("Pressed D, video brightness =", video_brightness)
            # Уменьшение яркости видео
            if key == ord('a') and video_brightness - step > mud_brightness:
                video_brightness -= step
                modify = True
                print("Pressed A, video brightness = ", video_brightness)
            # Увеличение яркости грязи
            if key == ord('g') and mud_brightness + step < video_brightness:
                mud_brightness += step
                modify = True
                print("Pressed G, mud brightness = ", mud_brightness)
            # Уменьшение яркости грязи
            if key == ord('f') and mud_brightness >= 0 + step:
                mud_brightness -= step
                modify = True
                print("Pressed F, mud brightness = ", mud_brightness)
            # Изменение кадра
            if modify:
                image_overlay = ((video_brightness - mud_brightness) / (max_pixel - min_pixel)) * \
                                (image_overlay_copy - min_pixel) + mud_brightness
                image_overlay = image_overlay.astype(np.uint8)
            # Наложение маски на изображение
            if do_mud_masking:
                # Вычисление маски изображения
                ret, mask = cv2.threshold(image_overlay, threshold, threshold, cv2.THRESH_TRUNC)
                mask = threshold - mask
                image = cv2.subtract(frame, mask)
            else:
                image = frame
            # Запись видео
            if can_video_recording:
                video.write(image)
                image = cv2.circle(image, (30, 30), 10, (0, 0, 255), -1)
            # Надпись на видео
            if not do_hide_text:
                text = ["key H-hide text", "key ESC-exit", "key SPACE-pause",
                        "key R-recording/stop recording video",
                        "key ENTER-write/read data",
			"key X-add/delete mud",
                        "keys W/S-increase/decrease in brightness threshold",
                        "keys D/A-increase/decrease video brightness",
                        "keys G/F-increase/decrease mud brightness"]
                # Расположение
                x = frame_width - 420
                y = frame_height - 500
                # Вывод текста на изображение
                for i in text:
                    image = cv2.putText(image, i, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (66, 170, 255), 2, cv2.LINE_4)
                    y += 25
            cv2.imshow(mud_video_name, image)
            # Запись / остановка записи видео
            if key == ord('r'):
                can_video_recording ^= 1
                if can_video_recording:
                    video.write(image)
                    print("Pressed R, video recording to {}".format(mud_video_path))
                else:
                    video.release()
                    data = np.uint8([threshold, mud_brightness, video_brightness])
                    file = open(data_file, "a")
                    file.write(' '.join(["{}".format(item) for item in data]))
                    file.write("\n")
                    file.close()
                    self.read_data(data_file)
                    print("Pressed R, video stop recorded; data recorded to {}, parameters: threshold = {data[0]}, "
                          "c = {data[1]}, d = {data[2]}".format(data_file, data=data))
            is_frame, frame = cap.read()
            # Остановка видео
            if not is_frame:
                cap.release()
                cap.open(self.video_path)
                is_frame, frame = cap.read()
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

        if self.list_box.size() >= 1:
            self.button_open_file.config(state=tk.ACTIVE, bg="#c0c0c0")
            self.master.bind('<o>', self.open_file)
        else:
            self.button_open_file.config(state=tk.DISABLED, bg="white")
            self.master.unbind('<o>')

        if self.list_box.size() == 2:
            self.button_simulation.config(state=tk.ACTIVE, bg="#ffb841")
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
    root.title("Choose files")
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



