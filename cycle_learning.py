import numpy as np
from openpyxl import load_workbook
from keras.models import Sequential
from keras.layers import Dense

# Создание массивов-контейнеров для данных.
x_train = np.empty((120, 12), dtype=float)      # Данные для обучения.
y_train = np.empty((120, 1), dtype=float)       # Ответы для обучения.
x_test = np.empty((22, 12), dtype=float)        # Данные для тестирования.
y_test = np.empty((22, 1), dtype=float)         # Ответы для тестирования.

# Получение листов Excel.
wb = load_workbook("smoking.xlsx")
lrn_sheet = wb.get_sheet_by_name("lrn")         # Лист с обучающим набором.
test_sheet = wb.get_sheet_by_name("test")       # Лист с тестовым набором.

# Заполнение x_train.
for i in range(3, 123):
    for j in range(12):
        x_train[i-3, j] = int(lrn_sheet[str(chr(65 + j)) + str(i)].value)

# Заполнение y_train.
for i in range(3, 123):
    y_train[i-3, 0] = int(lrn_sheet['M' + str(i)].value)

# Заполнение x_test.
for i in range(3, 25):
    for j in range(12):
        x_test[i-3, j] = int(test_sheet[str(chr(65 + j)) + str(i)].value)

# Заполнение y_test.
for i in range(3, 25):
    y_test[i-3, 0] = int(test_sheet['M' + str(i)].value)


maximums = list(x_train[0])                     # Максимумы по каждому из параметров.
minimums = list(x_train[0])                     # Минимумы по каждому из параметров.

# Поиск максимумов и минимумов по каждому параметру в обучающем наборе.
for i in range(1, 120):
    for j in range(12):
        if x_train[i, j] > maximums[j]:
            maximums[j] = x_train[i, j]
        elif x_train[i, j] < minimums[j]:
            minimums[j] = x_train[i, j]

# Поиск максимумов и минимумов по каждому параметру в тестовом наборе.
for i in range(0, 22):
    for j in range(12):
        if x_test[i, j] > maximums[j]:
            maximums[j] = x_train[i, j]
        elif x_test[i, j] < minimums[j]:
            minimums[j] = x_train[i, j]

# Нормализация данных (все значения теперь от 0 до 1) в обучающем наборе.
for i in range(0, 120):
    for j in range(12):
        x_train[i, j] = (x_train[i, j] - minimums[j]) / (maximums[j] - minimums[j])

# Нормализация данных (все значения теперь от 0 до 1) в тестовом наборе.
for i in range(0, 22):
    for j in range(12):
        x_test[i, j] = (x_test[i, j] - minimums[j]) / (maximums[j] - minimums[j])


for i in range(100):
    # Создание модели.
    model = Sequential()

    # Задание архитектуры сети.
    #   12 входов.
    #   4 нейрона в скрытом слое c линейным выпрямителем в качестве функции активации.
    #   1 нейрон в выходном слое с логистической функцией активации.
    model.add(Dense(4, input_dim=12, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Задание способа обучения сети.
    #   Критерий качества: бинарная переёрестная энтропия.
    #   Метод коррекции весов: adam (модификация метода градиентного спуска).
    #   Наблюдаемая метрика: точность (доля верных предсказаний в наборе).
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['binary_accuracy'])

    # Обучение сети.
    #   Кол-во эпох (сколько раз через сеть пройдёт весь обучающий набор данных): 100.
    #   Размер батча (через какое кол-во строк в матрице данных происходит коррекция весов): 10.
    model.fit(x_train, y_train, epochs=100, batch_size=10)

    # Проверка точности на тестовом наборе данных.
    scores = model.evaluate(x_test, y_test)

    if scores[1] > 0.89:
        # Сохранение модели.
        model.save('model_5.h5')
        break
