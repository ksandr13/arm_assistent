import sys  # sys нужен для передачи argv в QApplication
import os  # Отсюда нам понадобятся методы для отображения содержимого директорий
import json
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import  QInputDialog
import gui  # Это наш конвертированный файл дизайна
import scripts

class ExampleApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        #self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        uic.loadUi('gui.ui', self)

        self.currBase = 'C:\\MultiWork\\fedoseev\\data'
        self.label_OpenCurrentBase.setText(self.currBase)

        f = open("function_name.txt", "r", encoding='UTF-8')
        for line in f:
            line = line.replace("\n", "")
            item = self.listWidget.addItem(str(line))
        f.close()

        self.pushButton_OpenCurrentBase.clicked.connect(self.browse_folder)
        self.pushButton_InsertScript.clicked.connect(self.showDialogInsertScript)
        self.listWidget.itemClicked.connect(self.showScriptText)
        self.pushButton_Run.clicked.connect(self.run_script)

    def run_script(self):
        key = self.listWidget.currentItem().text()
        scripts.run_scripts(self, key, self.currBase, self.currBase)


    def showScriptText(self):
        key = self.listWidget.currentItem().text()
        f = open("scripts.py", "r", encoding='UTF-8')
        text = f.read()
        start = text.find('### %s' % key)
        finish = text.find('#### %s' % key)
        lenght = len('#### %s' % key)
        substr = text[start:finish+lenght]

        self.textEdit.setPlainText(substr) #
        f.close()

    def browse_folder(self):
        self.label_OpenCurrentBase.clear()  # На случай, если в списке уже есть элементы
        directory_OpenCurrentBase = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # открыть диалог выбора директории и установить значение переменной
        # равной пути к выбранной директории

        if directory_OpenCurrentBase:  # не продолжать выполнение, если пользователь не выбрал директорию
            print(directory_OpenCurrentBase)
            self.label_OpenCurrentBase.setText(directory_OpenCurrentBase)
            self.currBase =  directory_OpenCurrentBase
##            for filse_name in os.listdir(directory):  # для каждого файла в директории
##                self.listWidget.addItem(file_name)   # добавить файл в listWidget

    def showDialogInsertScript(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Введите название скрипта:')

        if ok:
            item = self.listWidget.addItem(str(text))

            with open("function_name.txt", "a", encoding='UTF-8') as f:
                f.write(text + '\n')
            f.close()
            with open("scripts.py", "a", encoding='UTF-8') as f:
                f.write(f'\n\n')
                f.write(f'    if name == "{text}":\n')
                f.write(f'### {text}\n')
                f.write(f'        return None\n')
                f.write(f'#### {text}\n')





def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение



if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
