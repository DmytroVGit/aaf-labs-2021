import Command_parser
import re

import sys

from database import DataBase

if __name__ == '__main__':
    tbls = [] #список созданных таблиц
    res = "" # от точки с запятой до конца строки - чтобы можно было писать команды не в однгу строку
    while True:

        print("Line:")
        line = res + sys.stdin.readline() + " " # считываем новую строку добавляя ее к предыдущему остатку
        if "exit" in line: # выходим из цикла если команда exit, завершаем работу программы
            break
        line = re.sub('\n', ' ', line) # заменяем переносы строки на пробелы
        commands = line.split(";") # разбиваем строку по точке с запятой - на команды
        res = commands[len(commands)-1] # записываем от последней точки с запятой до конца строки в перенос
        for i in range(0, len(commands)-1): # проходим по разбитым командам, кроме последней - которая ушла в перенос
            parsed = Command_parser.split_command(commands[i])  #вызываем парсер
            print("Result of command: " + commands[i]) #для красоты
            check = -1 # проверка на то, есть ли такое имя таблицы в нашем списке
            name = "" # имя таблицы
            name2 = "" # имя второй таблицы для операции full_join
            selected_cols = [] # список выбраных колонок для селекта
            where = [] # список условий для селекта и удаления
            full_join = [] # список условий джоина
            if parsed[0][0] != "error": # если не ошибка - то:
                for token in parsed: # разбираем каждую часть нашей команды. токен состоит из двух частей - аргумента и подписи, что это за аргумент
                    if token[1] == "name":
                        name = token[0].strip()
                    elif token[1] == "name2":
                        name2 = token[0].strip()
                    elif token[1] == "col name": # тут мы заполняем выбранные колонки для селекта
                        if re.search("[&]", token[0]):
                            selected_cols.append("&")
                        else:
                            selected_cols.append(token[0].strip())
                    elif token[1] == "full_join": # тут - для джоина
                        full_join.append(token[0].strip())
                    elif token[1] != "command" and parsed[0][0] == "select" or parsed[0][0] == "delete": # все что не попало в предыдущие условия - это условия для вера
                        where.append(token)
                i = 0
                for tbl in tbls: # проверяем наличие вызываемой таблицы в уже созданных таблицах
                    if tbl[0] == name:
                        check = i
                        break
                    i += 1
                if parsed[0][0] == "create" and check != -1: # если нужно создать а такая уже есть - ошибка
                    print(name + " is already created!")
                    continue
                elif parsed[0][0] != "create" and check == -1: # если нужно вставить, удалить, выбрать - а таблицы нету - ошибка
                    print(name + " isn`t already created!")
                    continue
                elif parsed[0][0] == "create": # для каждой команды вызываем нужную функцию, передав аргументы в нее.
                    tbl = DataBase(parsed[2:])
                    print("Table "+name + " was created!")
                    tbls.append([name, tbl])
                elif parsed[0][0] == "insert":
                    tbls[check][1].insert(0,parsed[2:])
                elif parsed[0][0] == "delete":
                    tbls[check][1].delete(parsed[2:])
                elif parsed[0][0] == "select":
                    i = 0
                    check2 = -1
                    for tbl in tbls: # для селекта с джоином - нужно проверить для второй таблицы ее наличие
                        if tbl[0] == name2:
                            check2 = i
                            break
                        i += 1
                    if check2 == -1 and name2 != "":
                        print(name2 + " isn`t already created!") # ошибка, если вторая таблица не существует

                    if name2 == "":
                        tbls[check][1].selectOneTable(selected_cols, where) # если у нас нет имени второй таблицы - селект без джоина
                    else:
                        tbls[check][1].selectJoin(tbls[check2][1], selected_cols, full_join, where) # если есть - с джоином
            else:
                print("Error: ", parsed[0][1]) # если ошибка - вывести ее
