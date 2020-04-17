import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QInputDialog
import gui  # Это наш конвертированный файл дизайна

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.pushButton_OpenCurrentBase.clicked.connect(self.browse_folder)
        self.pushButton_InsertScript.clicked.connect(self.showDialogInsertScript)

    def browse_folder(self):
        self.label_OpenCurrentBase.clear()  # На случай, если в списке уже есть элементы
        directory_OpenCurrentBase = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory_OpenCurrentBase:  # не продолжать выполнение, если пользователь не выбрал директорию
            print(directory_OpenCurrentBase)
            self.label_OpenCurrentBase.setText(directory_OpenCurrentBase)
##            for file_name in os.listdir(directory):  # для каждого файла в директории
##                self.listWidget.addItem(file_name)   # добавить файл в listWidget

    def showDialogInsertScript(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Введите название скрипта:')

        if ok:
            item = self.listWidget.addItem(str(text))
            #item.setText(str(text))
        



def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
