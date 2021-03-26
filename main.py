import numpy as np
from keras.models import load_model
from sys import exit
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from design import Ui_MainWindow

maximums = [2.0, 2.0, 2.0, 2.0, 3.0, 3.0, 2.0, 2.0, 3.0, 3.0, 4.0, 3.0]     # Максимумы по каждому параметру.
minimums = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]     # Минимумы по каждому параметру.

# Загрузка модели нейросети.
model = load_model('model_88_86.h5')
# print(model.layers[1].get_weights())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.next.clicked.connect(self.show_next_question)

        self.counter = 2
        self.data = np.empty([1, 12])

        self.ui.ask1.toggled.connect(self.enable_next_button)
        self.ui.ask2.toggled.connect(self.enable_next_button)
        self.ui.ask3.toggled.connect(self.enable_next_button)
        self.ui.ask4.toggled.connect(self.enable_next_button)

        self.ui.ask3.setVisible(False)
        self.ui.ask4.setVisible(False)

    def get_answer(self):
        if self.ui.ask1.isChecked():
            self.data[0, self.counter-2] = 1
        elif self.ui.ask2.isChecked():
            self.data[0, self.counter-2] = 2
        elif self.ui.ask3.isChecked():
            self.data[0, self.counter-2] = 3
        else:
            self.data[0, self.counter-2] = 4

    def enable_next_button(self):
        self.ui.next.setEnabled(True)

    def show_next_question(self):
        self.get_answer()
        if self.counter in [2, 3, 4, 7, 8]:
            self.ui.ask1.setText("Да")
            self.ui.ask2.setText("Нет")
            if self.counter == 2:
                self.ui.question.setText("2/12    Вы воспитывались в полной семье (мать и отец)?")
            elif self.counter == 3:
                self.ui.question.setText("3/12    Вы единственный ребёнок в семье?")
            elif self.counter == 4:
                self.ui.question.setText("4/12    Курит ли кто-то из ваших близких родственников?")
            elif self.counter == 7:
                self.ui.ask3.setEnabled(False)
                self.ui.ask3.setVisible(False)
                self.ui.question.setText("7/12    Употребляете ли вы алкоголь?")
            else:
                self.ui.question.setText("8/12    Занимаетесь ли вы спортом на регулярной основе?")
        elif self.counter in [5, 6, 9, 10, 12]:
            if self.counter == 5:
                self.ui.question.setText("5/12    Каков ваш уровень образования?")
                self.ui.ask1.setText("Высшее, неоконченное высшее, студент ВУЗа")
                self.ui.ask2.setText("Среднее специальное")
                self.ui.ask3.setText("Среднее")
                self.ui.ask3.setEnabled(True)
                self.ui.ask3.setVisible(True)
            elif self.counter == 6:
                self.ui.question.setText("6/12    Как вы оцениваете ваше финансовое положение?")
                self.ui.ask1.setText("Низкий достаток")
                self.ui.ask2.setText("Средний достаток")
                self.ui.ask3.setText("Высокий достаток")
            elif self.counter == 9:
                self.ui.question.setText("9/12    Как много людей из вашего окружения курит?")
                self.ui.ask1.setText("0-25%")
                self.ui.ask2.setText("26-75%")
                self.ui.ask3.setText("75-100%")
                self.ui.ask3.setEnabled(True)
                self.ui.ask3.setVisible(True)
            elif self.counter == 10:
                self.ui.question.setText("10/12    Как часто вы испытываете стрессовые ситуации?")
                self.ui.ask1.setText("Редко")
                self.ui.ask2.setText("Иногда")
                self.ui.ask3.setText("Часто")
            else:
                self.ui.question.setText("12/12    Как вы относитесь к курению?")
                self.ui.ask1.setText("Считаю, что это это нормально")
                self.ui.ask2.setText("Нейтрально, без осуждения")
                self.ui.ask3.setText("Негативно, неодобрительно")
                self.ui.ask3.setEnabled(True)
                self.ui.ask3.setVisible(True)
                self.ui.ask4.setEnabled(False)
                self.ui.ask4.setVisible(False)
        elif self.counter == 11:
            self.ui.question.setText("11/12    Каков ваш тип темперамента?")
            self.ui.ask1.setText("Сангвиник (энергичный, общительный, легко переживает трудности)")
            self.ui.ask2.setText("Меланхолик (высокочувствительный, легкоранимый)")
            self.ui.ask3.setText("Флегматик (спокойный, со стабильным настроением)")
            self.ui.ask4.setText("Холерик (вспыльчивый, порывистый, энергичный)")
            self.ui.ask4.setEnabled(True)
            self.ui.ask4.setVisible(True)
        else:
            # Нормализация.
            for i in range(12):
                self.data[0, i] = (self.data[0, i] - minimums[i]) / (maximums[i] - minimums[i])

            # Предсказание.
            prediction = model.predict(self.data)
            rounded = round(prediction[0, 0])

            msg = QMessageBox()
            msg.setWindowTitle("Результат")
            if rounded == 0:
                msg.setText("Вы не предрасположены к курению.")
            else:
                msg.setText("Вы предрасположены к курению.")
            ok_button = msg.addButton("Ok", QMessageBox.AcceptRole)
            msg.exec()
            if msg.clickedButton() == ok_button:
                exit(app.exec())

        self.counter += 1


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
exit(app.exec())
