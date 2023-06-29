import tkinter as tk
import pandas as pd
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

        
        # Создание второй вертикальной части (график)
        self.plot_frame = ttk.Frame(self.root, width=400, height=400)
        self.plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Создание третьей вертикальной части (таблица)
        self.table_frame = ttk.Frame(self.root, width=200, height=200)
        self.table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Создание комбобокса
        self.combobox = ttk.Combobox(self.combobox_frame)
        self.combobox.pack(padx=10, pady=10)
        self.add_button = ttk.Button(self.combobox_frame, text="Добавить", command=self.add_selection_block)
        self.add_button.pack(padx=10, pady=10)
        
        # Установка обработчика события выбора значения в комбобоксе
        #self.combobox.bind("<<ComboboxSelected>>", self.show_selected_value)
        
        # Чтение данных из CSV-файла
        df = pd.read_csv("sample.csv", sep=';')
        
        # Получение списка названий колонок
        column_names = df.columns.tolist()
        
        # Установка значений комбобокса как названия колонок
        self.combobox['values'] = column_names
        
        self.draw_diagram()

        # Создание заголовков столбцов для таблицы
        columns = ["Автор", "Название", "Год"]
        
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
        # Создание блока с виджетами
        selected_value_block = ttk.Frame(self.combobox_frame)
        selected_value_block.pack(padx=10, pady=10)

        name = self.combobox.get()
        # Создание виджетов в блоке
        selected_value_label = ttk.Label(selected_value_block, text=f"{name}")
        selected_value_label.pack()

        selected_value_entry = ttk.Entry(selected_value_block)
        selected_value_entry.pack(pady=10)

        def delete_selection_block():
            selected_value_block.destroy()

        save_button = ttk.Button(selected_value_block, text="Удалить", command=delete_selection_block)
        save_button.pack()


    def show_selected_value(self, event):
        selected_value = self.combobox.get()
        self.selected_value_label['text'] = f"{selected_value}"
        self.selected_value_entry.delete(0, tk.END)
        self.save_button['state'] = tk.NORMAL
        
        
# Создание экземпляра приложения
root = tk.Tk()
app = MyApp(root)

# Запуск главного цикла Tkinter
root.mainloop()
