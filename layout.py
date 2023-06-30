import tkinter as tk
import pandas as pd
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from matplotlib_venn import *

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
        self.parametr_list = []
        self.add_button = ttk.Button(self.container_frame, text="Добавить", command=self.add_selection_block, width=10)
        self.add_button.grid(padx=5, pady=5, row=2)

        # Чтение данных из CSV-файла
        def choose_file():
            path = filedialog.askopenfilename()
            df = pd.read_csv(path, sep=';')
            # Получение списка названий колонок
            self.column_names = df.columns.tolist()
            # Установка значений комбобокса как названия колонок
            self.combobox['values'] = self.column_names
            return df
        
        df = choose_file()

        # Создание квадратной кнопки
        self.open_file_button = ttk.Button(self.container_frame, text='Выбрать файл', command=choose_file)
        self.open_file_button.grid(padx=5, pady=5, row=0, column=0)

        self.accept_button = ttk.Button(self.combobox_frame, text="Применить")
        self.accept_button.pack(padx=5, pady=10, side=tk.BOTTOM)

        # Создание второй вертикальной части (график)
        self.plot_frame = ttk.Frame(self.root, width=400, height=400)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Создание третьей вертикальной части (таблица)
        self.table_frame = ttk.Frame(self.root, width=200, height=200)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.draw_diagram()

        # Создание заголовков столбцов для таблицы
        columns = ["Автор", "Название", "Год"]
        columns = df.columns.to_list()
        #print(columns)
        
        # Создание таблицы
        table = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        # Установка заголовков столбцов
        for column in columns:
            table.heading(column, text=column)
        
        # Чтение данных из CSV-файла и добавление их в таблицу
        for row in df[columns].itertuples(index=False):
            table.insert("", "end", values=row)
        
        table.pack(padx=10, pady=10)

    def draw_diagram(self):
        # Создание графика
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Ваш код для создания диаграммы Венна
        venn_data = (set([1, 2, 3, 4]), set([3, 4, 5, 6]), set([5, 6, 7, 8]))
        venn3(subsets=venn_data, set_labels=('Set A', 'Set B', 'Set C'), ax=ax)
        ax.set_title("Venn Diagram")

        # Определение радиуса кругов
        radius = 0.4

        # Размещение значений внутри кругов
        for subset, circle in zip(venn_data, ax.collections):
            center_x, center_y = circle.center
            circle_radius = circle.radius

            # Создание объекта Circle для текущего круга
            circle_patch = Circle((center_x, center_y), circle_radius - radius, color='white')

            # Расчет позиции для размещения текста внутри круга
            text_x, text_y = circle_patch.get_path().interiors[0].coords.mean(axis=0)

            # Отображение значения внутри круга
            ax.text(text_x, text_y, ', '.join(map(str, subset)), ha='center', va='center')

            # Добавление объекта Circle на график
            ax.add_patch(circle_patch)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        

    def add_selection_block(self):
        if self.combobox.get() == '':
            return
        # Создание блока с виджетами
        selected_value_block = ttk.Frame(self.combobox_frame)
        selected_value_block.pack(padx=10, pady=10)
        name = self.combobox.get()
        if name in self.parametr_list:
            return
        else:
            self.parametr_list.append(name)
        # Создание виджетов в блоке
        selected_value_label = ttk.Label(selected_value_block, text=f"{name}")
        selected_value_label.pack()

        selected_value_entry = ttk.Entry(selected_value_block)
        selected_value_entry.pack(pady=10)

        def delete_selection_block():
            selected_value_block.destroy()
            self.parametr_list.remove(name)

        delete_button = ttk.Button(selected_value_block, text="Удалить", command=delete_selection_block)
        delete_button.pack()

        
def init_program():
    # Создание экземпляра приложения
    root = tk.Tk()
    app = MyApp(root)
    # Запуск главного цикла Tkinter
    root.mainloop()

init_program()