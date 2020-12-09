
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import os
import codecs

import re


reg = None # регулярное выражение
find = None # найденый текст
repl = None # замещеный текст
findedFiles = [] # найденые файлы
replaseFiles = [] # файлы под замену

def readFile(ffile):
    try:
        fs = codecs.open(ffile, "r", 'UTF-8')#, encoding='UTF-8'
        text = fs.read()
        #print(ftext)
        fs.close()
        return text
    except Exception as ex:
        print(f'readFile error: {ffile}')

def writeFile(ffile):
    try:
        fs = codecs.open(ffile, "w", 'UTF-8')#, encoding='UTF-8'
        global repl
        fs.write(repl)
        #print(ftext)
        fs.close()

    except Exception as ex:
        print(f'writeFile error: {ffile}')

def replaseText(path):
    #print(f'replaseText: {path}')
    text = readFile(path)
    global find
    global repl
    global reg
    pattern = reg
    #print(find[0])
    try:
        repl = re.sub(pattern , find[0] , text )
        #print(f'pastText: {repl}')
        writeFile(path)
    except Exception as ex:

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def pastText(path):

    text = readFile(path)
    global find
    global repl
    pattern = r'(?sm)(</rodl_obj>)(\s*?)(</station>|<xi:include.*?/>)'
    print(path)
    try:
        repl = re.sub(pattern , r'\1\n%s\n\3' % find[0] , text )
        #print(f'pastText: {repl}')
        writeFile(path)
    except Exception as ex:

        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


def FilePathConcat(path1, path2):
        start = path1.find('data')
        substr1 = path1[start+4:len(path1)]

        return path2+substr1

def regFunction(num, key1, key2):
    if num == 1:
        return r'(?sm)(%s)(.*?)(%s)' % (key1, key2)


def findText(ffile):
    try:
        text = readFile(ffile)
        #print(ftext)
        #print(f'findText: {reg}')
        global find
        find = re.search(reg, text)
        #print(find[0] if find else 'Not found')
    except Exception as ex:
        print(f'Ошибка в функции findText. регулярка {reg}')

def findFile(ffile, ftext, flag):

    try:
        text = readFile(ffile)
        start = text.find(ftext)
        if start >= 0:
            #print(ffile)
            #findText(text)
            if flag == 'find':
                global findedFiles
                findedFiles.append(ffile)
                #print(f'finder: {findedFiles}')
            if flag == 'replase':
                global replaseFiles
                replaseFiles.append(ffile)
    except Exception as ex:
        print(f'Ошибка в функции findFile, при чтении файла {ffile}')



def finder(chapter, find_start, flag = 'find'):
    names = os.listdir(chapter)#os.getcwd()
    for name in names:
        fullname = os.path.join(chapter, name)
        if os.path.isfile(fullname):
            #print(fullname)
            #a = fullname.replace("\", "\\")
            filename, file_extension = os.path.splitext(name)
            if file_extension not in ('.cur', '.snd'):
                findFile(fullname, find_start, flag)
        else:
            finder(fullname, find_start, flag)





def run_scripts(self, name, *arg, **kwarg):
    global reg
    global find
    global repl
    global findedFiles
    global replaseFiles
    print(name)

    if name == "Обновление коммутатора":
### Обновление коммутатора
      return None
#### Обновление коммутатора


    if name == "Заполнение файла Objects":
### Заполнение файла Objects
      return None
#### Заполнение файла Objects


    if name == "Корректировка ЦП R4":
### Корректировка ЦП R4
      return None
#### Корректировка ЦП R4


    if name == "Обновление ИБП GE SitePro":
### Обновление ИБП GE SitePro
# Первым параметром передаем рабочую базу arg[0]
# Вторым параметрои передаем эталонную базу arg[1]
# Отступы не просто так, начальный отступ 8 пробелов, далее для условий и циклов по 4 пробела
        ReliseDate = arg[1]
        # Можно эталонную базу прописать руками, меньше будет геморроя
        ReliseDate = r'C:\MultiWork_my\fedoseev\data'
        key1_start = [r'<rodl_obj name="Main UPS">', r'<rodl_obj name="Small UPS">', r'<objtype name="ИБП_GE_SitePro"', r'<type name="ИБП GE SitePro">'] #начало первого ключа
        key1_end = [r'</rodl_obj>', r'</rodl_obj>', r'</objtype>', r'</type>'] #конец первого ключа


        for start, end in zip(key1_start, key1_end):
            print(f'---------{start}==========={end}')
            reg = None
            find = None
            findedFiles = []
            replaseFiles = []

            reg = regFunction(1, start, end) #поиск текста между 2х ключей
            finder(ReliseDate, start, 'find')
            """Ищем файл эталонной базы в котором есть совпадение с start и добавляем в кортеж findedFiles.
             Файлов может быть множество"""
            if findedFiles[0]:
                findText(findedFiles[0]) # Берем первый файл, где есть совпадение и по регулярному выражению копируем найденное в find

            if find: # если найдено
                #print(find)
                """Ищем файл рабочей базы в котором есть совпадение с start и добавляем в кортеж replaseFiles.
                Файлов может быть множество"""
                finder(arg[0], start, 'replase') # ищем по тому же ключу в рабочей базе
                if not replaseFiles: # если файлов для замены нет
                    pastText(FilePathConcat(findedFiles[0],arg[0]))# то вставляем в одноименный файл
                else:# иначе замещаем то что есть
                    replaseText(replaseFiles[0])# регулярное выражение, замещаем в рабочую базу


        return None
#### Обновление ИБП GE SitePro


    if name == "Тест":
### Тест

        QMessageBox.about(self, "Title", "Test")
        return None
#### Тест


    if name == "Контакты с командами":
### Контакты с командами
# Первым параметром передаем рабочую базу arg[0]
# Вторым параметрои передаем эталонную базу arg[1]
# Отступы не просто так, начальный отступ 8 пробелов, далее для условий и циклов по 4 пробела
        ReliseDate = arg[1]
        # Можно эталонную базу прописать руками, меньше будет геморроя
        ReliseDate = r'D:/depot/projects/dalnevostgd/BAM/uyktali/cos/current/data'
        key1_start = [r'<rodl_obj name="Контакт">', r'<rodl_obj name="Пользовательская_разметка">', r'<rodl_obj name="Таблица_времен">', r'<commtype name="Признак_аларма">'] #начало первого ключа
        key1_end = [r'</rodl_obj>', r'</rodl_obj>', r'</rodl_obj>', r'</commtype>'] #конец первого ключа
##        global reg
##        global find
##        global findedFiles
##        global replaseFiles

        for start, end in zip(key1_start, key1_end):
            print(f'---------{start}==========={end}')
            reg = None
            find = None
            repl = None
            findedFiles = []
            replaseFiles = []

            reg = regFunction(1, start, end) #поиск текста между 2х ключей
            finder(ReliseDate, start, 'find')
            print(f'finder 1 complited')
            """Ищем файл эталонной базы в котором есть совпадение с start и добавляем в кортеж findedFiles.
             Файлов может быть множество"""
            if findedFiles[0]:
                findText(findedFiles[0]) # Берем первый файл, где есть совпадение и по регулярному выражению копируем найденное в find
            print(f'findText complited')
            if find: # если найдено
                #print(find)
                """Ищем файл рабочей базы в котором есть совпадение с start и добавляем в кортеж replaseFiles.
                Файлов может быть множество"""
                finder(arg[0], start, 'replase') # ищем по тому же ключу в рабочей базе
                print(f'finder 2 complited')

                if not replaseFiles: # если файлов для замены нет
                    pastText(FilePathConcat(findedFiles[0],arg[0]))# то вставляем в одноименный файл
                    print(f'pastText complited')

                else:# иначе замещаем то что есть
                    replaseText(replaseFiles[0])# регулярное выражение, замещаем в рабочую базу
                    print(f'replaseText complited')


        return None
#### Контакты с командами
