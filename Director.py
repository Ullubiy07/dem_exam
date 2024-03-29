from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
import sys
import csv


class Director(QtWidgets.QDialog):
    def __init__(self, name):
        super().__init__()
        self.setGeometry(230, 150, 1500, 900)
        self.setStyleSheet('background-color: rgb(210, 210, 210)')

        self.name = name
        self.greet = QLabel('Привет, ' + name + '!', self)
        self.greet.setGeometry(600, 50, 200, 200)
        self.greet.setFont(QtGui.QFont('Arial', 20))
        self.greet.adjustSize()
        self.create_table()
        self.table_data()

        self.button_exit = QPushButton('Назад', self)
        self.button_exit.setGeometry(100, 750, 120, 70)
        self.button_exit.setFont(QtGui.QFont('Arial', 17))
        self.button_exit.clicked.connect(self.exit)
        self.button_exit.setStyleSheet('background-color: rgb(120, 120, 120)')

        self.button_delete = QPushButton('Удалить', self)
        self.button_delete.setGeometry(300, 660, 150, 70)
        self.button_delete.setFont(QtGui.QFont('Arial', 14))
        self.button_delete.setStyleSheet('background-color: rgb(120, 120, 120)')
        self.button_delete.clicked.connect(self.delete_row)

        self.button_change = QPushButton('Изменить', self)
        self.button_change.setGeometry(470, 660, 150, 70)
        self.button_change.setFont(QtGui.QFont('Arial', 14))
        self.button_change.setStyleSheet('background-color: rgb(120, 120, 120)')
        self.button_change.clicked.connect(self.change)

        self.button_add = QPushButton('Добавить', self)
        self.button_add.setGeometry(640, 660, 150, 70)
        self.button_add.setFont(QtGui.QFont('Arial', 14))
        self.button_add.setStyleSheet('background-color: rgb(120, 120, 120)')
        self.button_add.clicked.connect(self.add_data)

        self.v1, self.v2, self.v3, self.v4, self.v5 = '', '', '', '', ''

    def exit(self):
        from main import MainWindow
        home = MainWindow()
        home.show()
        self.close()

    def decorator(func):
        def inner(self, *args):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner


    def create_table(self):
        self.table = QTableWidget(self)
        self.table.setStyleSheet('background-color: white')
        self.table.setGeometry(300, 150, 1030, 500)
        mas = ['Номер заказа', 'Имя клиента', 'Название товара', 'Количество товара', 'Оставшийся срок']
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(mas)
        self.table.horizontalHeader().setFixedHeight(60)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 200)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFont(QtGui.QFont('Arial', 12))

        count = 0
        for j in mas:
            item = QTableWidgetItem(j)
            item.setFont(QtGui.QFont('Arial', 12))
            item.setBackground(QtGui.QColor(120, 120, 120))
            self.table.setHorizontalHeaderItem(count, item)

            count += 1


    @decorator
    def table_data(self):
        with open('product.csv', 'r', encoding='utf-8') as file:
            file = csv.reader(file)
            count = 0
            for i in file:
                i = ''.join(i).split(';')
                if count != 0:
                    self.table.setRowCount(count)
                    self.table.setItem(count - 1, 0, QTableWidgetItem(i[0]))
                    self.table.setItem(count - 1, 1, QTableWidgetItem(i[1]))
                    self.table.setItem(count - 1, 2, QTableWidgetItem(i[2]))
                    self.table.setItem(count - 1, 3, QTableWidgetItem(i[3]))
                    self.table.setItem(count - 1, 4, QTableWidgetItem(i[4]))

                count += 1

    def delete_row(self):
        if self.table.selectedIndexes():
            self.row = self.table.currentIndex().row()
            if self.row >= 0:
                self.table.removeRow(self.row)
                self.remove_csv()
    @decorator
    def remove_csv(self):
        with open('product.csv', 'r', encoding='utf-8') as file:
            file = csv.reader(file)
            count = -1
            data = []
            for i in file:
                if count != self.row:
                    data.append(i)
                count += 1

        file = open('product.csv', 'w', encoding='utf-8')
        file.truncate()

        with open('product.csv', 'w', encoding='utf-8', newline='') as file:
            file = csv.writer(file)
            for j in data:
                file.writerow(j)

    def change(self):
        if self.table.selectedIndexes():
            row = self.table.currentIndex().row()
            if row >= 0:
                self.v1, self.v2, self.v3, self.v4, self.v5 = self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text(), self.table.item(row, 3).text(), self.table.item(row, 4).text()
                self.func = 1
                self.form_window = Form(self)
                self.form_window.show()
                self.close()

    def add_data(self):
        self.func = 0
        self.form_window = Form(self)
        self.form_window.show()
        self.close()


class Form(QtWidgets.QDialog):
    def __init__(self, lol):
        super().__init__()

        self.setGeometry(230, 150, 1500, 900)
        self.setStyleSheet('background-color: rgb(210, 210, 210)')

        self.lol = lol
        self.order_number_value = QLabel('Номер заказа:', self)
        self.order_number_value.setGeometry(250, 100, 250, 50)
        self.order_number_value.setFont(QtGui.QFont('Arial', 20))

        self.cilent_name_value = QLabel('Имя клиента:', self)
        self.cilent_name_value.setGeometry(260, 200, 250, 50)
        self.cilent_name_value.setFont(QtGui.QFont('Arial', 20))

        self.product_name_value = QLabel('Название товара:', self)
        self.product_name_value.setGeometry(200, 300, 300, 50)
        self.product_name_value.setFont(QtGui.QFont('Arial', 20))

        self.product_amount_value = QLabel('Количество товара:', self)
        self.product_amount_value.setGeometry(170, 400, 300, 50)
        self.product_amount_value.setFont(QtGui.QFont('Arial', 20))

        self.deadline_value = QLabel('Дата отгрузки:', self)
        self.deadline_value.setGeometry(250, 500, 500, 50)
        self.deadline_value.setFont(QtGui.QFont('Arial', 20))

        try:
            self.order_number_input = QLineEdit(self)
            self.order_number_input.setGeometry(500, 100, 400, 50)
            self.order_number_input.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.order_number_input.setFont(QtGui.QFont('Arial', 20))
            self.order_number_input.setText(self.lol.v1)

            self.cilent_name_input = QLineEdit(self)
            self.cilent_name_input.setGeometry(500, 200, 400, 50)
            self.cilent_name_input.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.cilent_name_input.setFont(QtGui.QFont('Arial', 20))
            self.cilent_name_input.setText(self.lol.v2)

            self.product_name_input = QLineEdit(self)
            self.product_name_input.setGeometry(500, 300, 400, 50)
            self.product_name_input.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.product_name_input.setFont(QtGui.QFont('Arial', 20))
            self.product_name_input.setText(self.lol.v3)

            self.product_amount_input = QLineEdit(self)
            self.product_amount_input.setGeometry(500, 400, 400, 50)
            self.product_amount_input.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.product_amount_input.setFont(QtGui.QFont('Arial', 20))
            self.product_amount_input.setText(self.lol.v4)

            self.deadline_input = QLineEdit(self)
            self.deadline_input.setGeometry(500, 500, 400, 50)
            self.deadline_input.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.deadline_input.setPlaceholderText("Пример: 2024-6-17")
            self.deadline_input.setFont(QtGui.QFont('Arial', 20))
            self.deadline_input.setText(self.lol.v5)

            self.button_exit = QPushButton('Выйти', self)
            self.button_exit.setFont(QtGui.QFont('Arial', 17))
            self.button_exit.setStyleSheet('background-color: rgb(120, 120, 120)')
            self.button_exit.setGeometry(200, 700, 120, 70)
            self.button_exit.clicked.connect(self.exit)

            self.button_join = QPushButton('Принять', self)
            self.button_join.setFont(QtGui.QFont('Arial', 17))
            self.button_join.setStyleSheet('background-color: rgb(120, 120, 120)')
            self.button_join.setGeometry(550, 600, 120, 70)
            self.button_join.clicked.connect(self.checking)
            self.access = False
            self.access1 = False
        except Exception as e:
            print(e)

    def exit(self):
        self.director_window = Director(self.lol.name)
        self.director_window.show()
        self.close()

    def checking(self):
        if self.order_number_input.text() != '' and self.product_name_input.text() != '' and self.cilent_name_input.text() != '' and self.product_amount_input.text() != '' and self.deadline_input.text() != '':
            self.access = True
            if self.deadline_input.text().count('-') == 2 and len(self.deadline_input.text().split('-')) == 3:
                self.access1 = True
            else:
                self.access1 = False
                error = QMessageBox()
                error.setWindowTitle('Ошибка')
                error.setIcon(QMessageBox.Information)
                error.setText('Неверный формат даты, следуйте примеру')
                error.exec_()
        else:
            self.access = False
            error = QMessageBox()
            error.setWindowTitle('Ошибка')
            error.setIcon(QMessageBox.Information)
            error.setText('Заполните все поля')
            error.exec_()


        if self.access and self.access1 and self.lol.func == 0:
            with open('product.csv', 'a', encoding='utf-8', newline='') as file:
                file = csv.writer(file, delimiter=';')
                file.writerow([self.order_number_input.text(), self.cilent_name_input.text(), self.product_name_input.text(), self.product_amount_input.text(), self.deadline_input.text()])

            self.exit()
        elif self.access and self.access1 and self.lol.func == 1:
            with open('product.csv', 'r', encoding='utf-8', newline='') as file:
                file = csv.reader(file)
                data = []
                for i in file:
                    i = ''.join(i).split(';')
                    if i[0] == self.lol.v1 and i[1] == self.lol.v2 and i[2] == self.lol.v3 and i[3] == self.lol.v4 and i[4] == self.lol.v5:
                        data.append([self.order_number_input.text(), self.cilent_name_input.text(), self.product_name_input.text(), self.product_amount_input.text(), self.deadline_input.text()])
                    else:
                        data.append(i)
            file = open('product.csv', 'w', encoding='utf-8')
            file.truncate()

            with open('product.csv', 'a', encoding='utf-8', newline='') as file:
                file = csv.writer(file, delimiter=';')
                for i in data:
                    file.writerow(i)
            self.exit()



