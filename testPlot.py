import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Создаем окно Tkinter
window = tk.Tk()
window.title("Отображение графика Matplotlib")

# Создаем фигуру Matplotlib
fig = Figure(figsize=(5, 4), dpi=100)
# Создаем подзаголовок (subplot) на фигуре
ax = fig.add_subplot(111)
# Создаем данные для графика
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
# Строим график
ax.plot(x, y)

# Создаем виджет FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack()

# Запускаем главный цикл Tkinter
tk.mainloop()
