import tkinter as tk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

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
        
        # Установка обработчика события выбора значения в комбобоксе
        self.combobox.bind("<<ComboboxSelected>>", self.show_selected_value)
        
        # Чтение данных из CSV-файла
        df = pd.read_csv("sample.csv", sep=';')
        
        # Получение списка названий колонок
        column_names = df.columns.tolist()
        
        # Установка значений комбобокса как названия колонок
        self.combobox['values'] = column_names
        
        # Создание блока с виджетами
        self.selected_value_block = ttk.Frame(self.combobox_frame)
        self.selected_value_block.pack(padx=10, pady=10)
        
        # Создание виджетов в блоке
        self.selected_value_label = ttk.Label(self.selected_value_block, text="Название параметра:")
        self.selected_value_label.pack()
        
        self.selected_value_entry = ttk.Entry(self.selected_value_block)
        self.selected_value_entry.pack(pady=10)
        
        self.save_button = ttk.Button(self.selected_value_block, text="Сохранить", command=self.save_value)
        self.save_button.pack()
        
        # Создание графика
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

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
    
    def show_selected_value(self, event):
        selected_value = self.combobox.get()
        self.selected_value_label['text'] = f"{selected_value}"
        self.selected_value_entry.delete(0, tk.END)
        self.save_button['state'] = tk.NORMAL
        
    def save_value(self):
        value = self.selected_value_entry.get()
        # Действия по сохранению значения
        
# Создание экземпляра приложения
root = tk.Tk()
app = MyApp(root)

# Запуск главного цикла Tkinter
root.mainloop()
