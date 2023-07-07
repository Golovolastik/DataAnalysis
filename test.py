import matplotlib.pyplot as plt
import numpy as np

def display_value(event):
    key = event.artist.get_text()
    value = my_dict[key]
    print(f"Значение для ключа '{key}': {value}")

def zoom_in(event):
    global display_count

    display_count += 2  # Увеличиваем количество отображаемых ключей при приближении
    display_count = min(display_count, len(my_dict))  # Ограничиваем количество ключей

    update_display()

def zoom_out(event):
    global display_count

    display_count -= 2  # Уменьшаем количество отображаемых ключей при отдалении
    display_count = max(display_count, 2)  # Ограничиваем количество ключей

    update_display()

def update_display():
    ax.clear()

    # Рисование круга
    circle = plt.Circle(center, radius, color='red', alpha=0.2)
    ax.add_artist(circle)

    # Выбираем ключи для отображения
    keys = np.random.choice(list(my_dict.keys()), size=display_count, replace=False)

    # Координаты для размещения ключей
    angles = np.linspace(0, 2 * np.pi, display_count, endpoint=False)

    # Построение текста внутри круга
    for angle, key in zip(angles, keys):
        x = center[0] + (radius - offset) * np.cos(angle)
        y = center[1] + (radius - offset) * np.sin(angle)
        ax.text(x, y, key, ha='center', va='center')

    # Добавление обработчика событий при клике на текст
    for text in ax.texts:
        text.set_picker(True)

    ax.axis('off')

    # Обновление отображения
    plt.draw()

# Ваш словарь с 100 ключами
my_dict = {f'Ключ{i}': f'Значение{i}' for i in range(1, 101)}

# Отображаемое количество ключей
display_count = 8

# Создание фигуры и осей
fig, ax = plt.subplots(figsize=(6, 6))  # Установите желаемый размер окна фигуры здесь

# Радиус окружности
radius = 0.5

# Координаты центра окружности
center = (0.5, 0.5)  # Изменено для центрирования круга внутри окна

# Рисование круга
circle = plt.Circle(center, radius, color='red', alpha=0.2)
ax.add_artist(circle)

# Координаты для размещения ключей
angles = np.linspace(0, 2 * np.pi, display_count, endpoint=False)

# Расстояние от центра окружности до текста
offset = 0.25

# Построение текста внутри круга
for angle, key in zip(angles, list(my_dict.keys())[:display_count]):
    x = center[0] + (radius - offset) * np.cos(angle)
    y = center[1] + (radius - offset) * np.sin(angle)
    ax.text(x, y, key, ha='center', va='center')

# Добавление обработчика событий при клике на текст
for text in ax.texts:
    text.set_picker(True)

# Создание кнопок приближения и отдаления
ax_zoom_in = plt.axes([0.8, 0.05, 0.1, 0.075])
ax_zoom_out = plt.axes([0.65, 0.05, 0.1, 0.075])
button_zoom_in = plt.Button(ax_zoom_in, '+')
button_zoom_out = plt.Button(ax_zoom_out, '-')

# Добавление обработчиков событий при нажатии на кнопки
button_zoom_in.on_clicked(zoom_in)
button_zoom_out.on_clicked(zoom_out)

# Установка предотвращения искажения аспекта
ax.set_aspect('equal')

# Убрать значения на шкалах
# ax.set_xticklabels([])
# ax.set_yticklabels([])

ax.axis('off')

# Отображение графика
plt.show()
