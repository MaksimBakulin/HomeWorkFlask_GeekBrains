import os
import sys
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class App:
    def __init__(self, master):
        self.master = master
        master.title("Speech Recognition App")

        # создаем виджеты
        self.label = tk.Label(master, text="Выберите аудиофайл")
        self.label.pack()

        self.button = tk.Button(master, text="Выбрать файл", command=self.choose_file)
        self.button.pack()

        self.textbox = scrolledtext.ScrolledText(master, width=60, height=20)
        self.textbox.pack()

    def choose_file(self):
        # открываем диалог выбора файла
        audio_file = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav;*.mp3")])

        if audio_file:
            # создаем объект Recognizer
            r = sr.Recognizer()

            # открываем аудиофайл и записываем данные в объект AudioFile
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)

            # используем метод recognize_google для распознавания речи
            try:
                result = r.recognize_google(audio_data, show_all=True, language="ru-RU")
            except sr.UnknownValueError:
                messagebox.showerror("Ошибка", "Не удалось распознать речь в файле")
                return
            except sr.RequestError:
                messagebox.showerror("Ошибка", "Ошибка соединения с сервером распознавания речи")
                return

            # получаем имя выходного файла из имени входного файла
            output_file = os.path.splitext(audio_file)[0] + ".txt"

            # сохраняем результат в отдельный файл с полным содержанием аудиофайла и распознанными словами
            with open(output_file, "w") as f:
                for alternative in result["alternative"]:
                    transcript = alternative["transcript"]
                    f.write(f"{transcript}\n")

            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, f"Результат сохранен в файл: {output_file}")
            messagebox.showinfo("Готово", "Распознавание речи завершено и результат сохранен в файл")

root = tk.Tk()
app = App(root)
root.mainloop()