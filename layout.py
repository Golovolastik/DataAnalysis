import tkinter as tk
import pandas as pd
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from venn_lib import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Мое приложение")
        
        # Размещение виджетов
        self.create_widgets()
        
    def create_widgets(self):
        # Создание первой вертикальной части (комбобокс и набор виджетов)
        self.combobox_frame = ttk.Frame(self.root, width=200, height=200)
        self.combobox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Создание контейнера Frame для кнопки и комбо-бокса
        self.container_frame = ttk.Frame(self.combobox_frame)
        self.container_frame.pack(side=tk.TOP, padx=5, pady=5)

        # Создание комбобокса
        self.combobox = ttk.Combobox(self.container_frame, width=12)
        self.combobox.state(['readonly'])
        self.combobox.grid(padx=5, pady=5, row=1, column=0)
        self.parameter_dict = {} # Cписок параметров
        self.add_button = ttk.Button(self.container_frame, text="Добавить", command=self.add_selection_block, width=10)
        self.add_button.grid(padx=5, pady=5, row=2)

        # Cоздание области для выбранных параметров
        self.parameter_frame = ttk.Frame(self.combobox_frame)
        self.parameter_frame.pack(padx=5, pady=5, side='top')

        # Чтение данных из CSV-файла
        def choose_file():
            path = filedialog.askopenfilename()
            try:
                df = pd.read_csv(path, sep=';')
            except:
                return
            # Получение списка названий колонок
            self.column_names = df.columns.tolist()
            # Установка значений комбобокса как названия колонок
            self.combobox['values'] = self.column_names
            # Очистка старого фрейма
            for widget in self.parameter_frame.winfo_children():
                widget.destroy()
            self.parameter_dict.clear()
            self.combobox.set('')
            return df
        
        self.df = choose_file()

        # Создание кнопки выбора файла
        self.open_file_button = ttk.Button(self.container_frame, text='Выбрать файл', command=choose_file)
        self.open_file_button.grid(padx=5, pady=5, row=0, column=0)

        # Создание второй вертикальной части (график)
        self.plot_frame = ttk.Frame(self.root, width=400, height=400)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #self.plot_frame.pack_propagate(False)
        self.draw_diagram()
        
        # Создание третьей вертикальной части (таблица)
        self.table_frame = ttk.Frame(self.root, width=200, height=200)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # # Создание заголовков столбцов для таблицы
        columns = self.df.columns.to_list()
        
        # Создание таблицы
        table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        # # Установка заголовков столбцов
        for column in columns:
            table.heading(column, text=column)
        
        # # Чтение данных из CSV-файла и добавление их в таблицу
        for row in self.df[columns].itertuples(index=False):
            table.insert("", "end", values=row)
        
        table.pack(padx=10, pady=10)

    def draw_diagram(self):
        # Создание графика
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal')

        # Ваш код для создания диаграммы Венна
        venn_data = (set([1, 2, 3, 4]), set([3, 4, 5, 6]))
        venn2(ax, venn_data)
        #ax.set_title("Venn Diagram")
        # Устанавливаем пределы осей
        ax.set_xlim(0, 2)
        ax.set_ylim(0, 2)
        ax.axis('off')

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        # Создание панели инструментов навигации для приближения и перемещения
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()
        fig.tight_layout()

    def add_selection_block(self):
        if self.combobox.get() == '':
            return
        # Создание блока с виджетами
        if not self.parameter_dict:
            self.accept_button = ttk.Button(self.parameter_frame, text="Применить", command=self.accept_button_command)
            self.accept_button.pack(padx=5, pady=10, side=tk.TOP)
        name = self.combobox.get()
        self.combobox.set('')
        if name in self.parameter_dict:
            return
        else:
            self.parameter_dict[name] = None
        # Создание виджетов в блоке
        selected_value_label = tk.LabelFrame(self.parameter_frame, text=f"{name}")
        selected_value_label.pack()

        selected_value_entry = ttk.Entry(selected_value_label, width=10)
        selected_value_entry.pack(pady=5, padx=5)

        def delete_selection_block():
            selected_value_label.destroy()
            self.parameter_dict.pop(name)
            if not self.parameter_dict:
                self.accept_button.destroy()

        delete_button = ttk.Button(selected_value_label, text="Удалить", command=delete_selection_block)
        delete_button.pack()

    def accept_button_command(self):
        print("hello!")
        # value1 = 
        # self.df[self.df[self.parameter_dict[0]] == ]


def init_program():
    # Создание экземпляра приложения
    root = tk.Tk()
    app = MyApp(root)
    # Запуск главного цикла Tkinter
    root.mainloop()

init_program()