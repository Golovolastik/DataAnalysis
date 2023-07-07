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
        root.geometry('1024x576')
        root.resizable(False, False)
        
        # Размещение виджетов
        self.create_widgets()
        
    def create_widgets(self):
        # Создание первой вертикальной части (комбобокс и набор виджетов)
        self.combobox_frame = ttk.Frame(self.root, width=200, height=200)
        self.combobox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Создание контейнера Frame для кнопки и комбо-бокса
        self.container_frame = ttk.Frame(self.combobox_frame, width=200, height=200)
        self.container_frame.pack(side=tk.TOP, padx=5, pady=5, expand=False)

        # Создание комбобокса
        self.combobox = ttk.Combobox(self.container_frame, width=12)
        self.combobox.state(['readonly'])
        self.combobox.grid(padx=5, pady=5, row=1, column=0)
        self.parameter_dict = {} # Cписок параметров
        self.entry_list = [] # Список полей для ввода
        self.add_button = ttk.Button(self.container_frame, text="Добавить", command=self.add_selection_block, width=10)
        self.add_button.grid(padx=5, pady=5, row=2)

        # Cоздание области для выбранных параметров
        self.parameter_frame = ttk.Frame(self.combobox_frame)
        self.parameter_frame.pack(padx=5, pady=5, side='top', expand=False)

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
        self.df = self.df.astype(str)

        # Создание кнопки выбора файла
        self.open_file_button = ttk.Button(self.container_frame, text='Выбрать файл', command=choose_file)
        self.open_file_button.grid(padx=5, pady=5, row=0, column=0)

        # Создание второй вертикальной части (график)
        self.plot_frame = ttk.Frame(self.root, width=400, height=400)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #self.plot_frame.pack_propagate(False)
        #self.draw_diagram()
        
        # Создание третьей вертикальной части (таблица)
        self.table_frame = ttk.Frame(self.root, width=200, height=200)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
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

    def make_set(self):
        self.set_list = []
        for key in self.parameter_dict:
            result_set = set()
            value = self.parameter_dict[key]
            finded = self.df[self.df[key] == value]
            result_set.update(finded.index)
            self.set_list.append(result_set)
        return self.set_list
    
    def on_point_click(self, event):
        print("working")
        # if event.artist in point_value_dict:
        #     point = point_value_dict[event.artist]
        #     print(f"Нажата точка {point}")

    def place_dots(self):
        all_artists = self.ax.get_children()
        circles = []
        for artist in all_artists:
            if isinstance(artist, plt.Circle):
                # Получаем координаты и радиус окружности
                center = artist.center
                radius = artist.radius
                circles.append([center, radius])
        number_of_dots = {
                          0.5: 8,
                          0.35: 6,
                          0.25: 4,
                          0.15: 3
                         }
        # Создание нового списка множеств для уникальных значений
        self.unique_sets = [set() for _ in range(len(self.venn_data))]

        # Заполнение нового списка множеств уникальными значениями
        for i, current_set in enumerate(self.venn_data):
            for value in current_set:
                is_unique = True
                for j in range(len(self.venn_data)):
                    if j != i and value in self.venn_data[j]:
                        is_unique = False
                        break
                if is_unique:
                    self.unique_sets[i].add(value)
        print(circles)
        print(self.unique_sets)

        # self.unique_sets = []
        # for i, current_set in enumerate(self.venn_data):
        #     unique_values = set()
        #     for j in range(1, len(self.venn_data)):
        #         unique_values.update(current_set - self.venn_data[j])
        #     self.unique_sets.append(unique_values)

        for i, unique in enumerate(self.unique_sets):
            if len(unique) < number_of_dots.get(circles[i][1]):
                number = len(unique)
            else:
                number = number_of_dots.get(radius)
            random_set = random.sample(unique, number)
            for point in random_set:
                dist = random.random() * circles[i][1]*0.75
                theta = random.random() * 2 * np.pi
                x = circles[i][0][0] + dist * np.cos(theta) 
                y = circles[i][0][1] + dist * np.sin(theta)
                dot = self.ax.plot(x, y, 'ro')[0]
                dot.set_picker(5)  # Радиус "зоны попадания" для нажатия
                dot.set_pickradius(5)  # Радиус точки
        
        # intersections = []  # Множество для хранения уникальных точек пересечения

        # points = set()
        # for i, circle in enumerate(circles):
        #     for j in range(i + 1, len(circles)):
        #         if self.venn_data[i].intersection(self.venn_data[j]) in points:
        #             continue
        #         if self.venn_data[i].intersection(self.venn_data[j]):
        #             intersection_center = find_circle_intersection_center(
        #                 circles[i][0][0], circles[i][0][1], circles[i][1],
        #                 circles[j][0][0], circles[j][0][1], circles[j][1]
        #             )
        #             points.update(self.venn_data[i].intersection(self.venn_data[j]))
        #             #intersections.update(points)  # Добавляем точки пересечения в множество intersections
        #             print(points)
        # for point in points:
        #                 random_offset = -0.1 + random.random() * 0.2
        #                 dot = self.ax.plot(
        #                     intersection_center[0] + random_offset,
        #                     intersection_center[1] + random_offset,
        #                     'go'
        #                 )[0]
        #                 dot.set_picker(5)  # Радиус "зоны попадания" для нажатия
        #                 dot.set_pickradius(5)  # Радиус точки
        self.fig.canvas.mpl_connect('pick_event', self.on_point_click)

            

    def draw_diagram(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        # Создание графика
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_aspect('equal')
        self.venn_data = self.make_set()
        print(self.venn_data)
        print(self.parameter_dict)
        choose_venn(len(self.venn_data), self.ax, self.venn_data, self.parameter_dict)
        # Устанавливаем пределы осей
        self.ax.set_xlim(-2, 3)
        self.ax.set_ylim(-2, 3)
        self.ax.axis('off')

        self.place_dots()

        canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        canvas.draw()
        # Создание панели инструментов навигации для приближения и перемещения
        toolbar = NavigationToolbar2Tk(canvas, self.plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack()
        self.fig.tight_layout()

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
        self.entry_list.append(selected_value_entry)

        def delete_selection_block():
            selected_value_label.destroy()
            self.parameter_dict.pop(name)
            self.entry_list.remove(selected_value_entry)
            if not self.parameter_dict:
                self.accept_button.destroy()

        delete_button = ttk.Button(selected_value_label, text="Удалить", command=delete_selection_block)
        delete_button.pack()

    def accept_button_command(self):
        for i, item in enumerate(self.parameter_dict.items()):
            key, value = item
            self.parameter_dict[key] = self.entry_list[i].get()
        # Трассировка
        # for key in self.parameter_dict:
        #     print(f"{key}: {self.parameter_dict[key]}")
        self.make_set()
        self.draw_diagram()
            


def init_program():
    # Создание экземпляра приложения
    root = tk.Tk()
    app = MyApp(root)
    # Запуск главного цикла Tkinter
    root.update_idletasks()
    root.mainloop()

init_program()