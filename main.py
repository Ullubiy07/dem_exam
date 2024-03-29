from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyleFactory, QLabel, QLineEdit, QPushButton, QMessageBox
import sys
import csv


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(230, 150, 1500, 900)
        self.setStyleSheet('background-color: rgb(210, 210, 210)')

        self.login = QLabel('Логин', self)
        self.login.setGeometry(470, 210, 200, 60)
        self.login.setFont(QtGui.QFont('Arial', 25))

        self.password = QLabel('Пароль', self)
        self.password.setGeometry(450, 350, 200, 60)
        self.password.setFont(QtGui.QFont('Arial', 25))

        self.password_line = QLineEdit(self)
        self.password_line.setGeometry(650, 350, 400, 80)
        self.password_line.setFont(QtGui.QFont('Arial', 20))
        self.password_line.setStyleSheet('background-color: white')
        self.password_line.setEchoMode(QLineEdit.Password)

        self.login_line = QLineEdit(self)
        self.login_line.setGeometry(650, 200, 400, 80)
        self.login_line.setFont(QtGui.QFont('Arial', 20))
        self.login_line.setStyleSheet('background-color: white')

        self.button_exit = QPushButton('Выйти', self)
        self.button_exit.setGeometry(100, 750, 120, 70)
        self.button_exit.setFont(QtGui.QFont('Arial', 17))
        self.button_exit.clicked.connect(lambda: self.close())
        self.button_exit.setStyleSheet('background-color: rgb(120, 120, 120)')

        self.button_join = QPushButton('Войти', self)
        self.button_join.setGeometry(800, 600, 120, 70)
        self.button_join.setFont(QtGui.QFont('Arial', 17))
        self.button_join.setStyleSheet('background-color: rgb(120, 120, 120)')
        self.button_join.clicked.connect(self.checking)
        self.access = False
        self.name = ''
        self.perm = ''


    def decorator(func):
        def inner(self, *args):
            try:
                func(self)
            except Exception as e:
                print(e)
        return inner

    @decorator
    def check_permission(self):
        with open('data.csv', encoding='utf-8') as file:
            file = csv.reader(file)
            for i in file:
                i = ''.join(i).split(';')
                if i[1] == self.login_line.text() and i[2] == self.password_line.text():
                    self.access = True
                    self.name = i[0]
                    self.perm = i[3]

    def checking(self):
        self.check_permission()
        if self.perm == 'директор' and self.access:
            from Director import Director
            self.director_window = Director(self.name)
            self.director_window.show()
            self.close()
        else:
            self.error()

    def error(self):
        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        error.setText('Неверный логин или пароль')
        error.setIcon(QMessageBox.Information)
        error.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    home = MainWindow()
    home.show()
    sys.exit(app.exec_())
