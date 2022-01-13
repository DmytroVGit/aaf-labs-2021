import ctypes
import re
from copy import deepcopy

from indexes import Index


class DataBase:
    def __init__(self, args):

        self.colNumber = len(args)#количество столбцов
        self.data = []
        i = 0
        self.colNames = []
        self.id = 1
        for arg in args:
            if arg[1] == "0" or arg[1] == 1:
                self.colNames.append([arg[0].strip(), None])#не индексированый столбец
            elif arg[1] == "1" or arg[1] == 0:
                self.colNames.append([arg[0].strip(), Index()])#индексированый столбец
            elif arg[1] is not None:
                self.colNames.append([arg[0].strip(), Index()])# индексированый столбец если копируем таблицу из уже готовой
            else:
                self.colNames.append([arg[0].strip(), None])# неиндекс.
            i += 1
    def ind(self, id, args):
        for i in range(0,len(self.colNames)):
            if self.colNames[i][1] is not None:
                self.colNames[i][1].add(args[i],id)# вызываем добавление ряда в дерево индекса для каждого инд. столбца - дервео храниться в названиях столбцов

    def insert(self, show, args):
        if len(args) != self.colNumber:# если на вставку больше или меньше значений чем столбцов - ошибка
            print("Number of inserted values not equal to number of columns!")
            return
        tempr = []
        for el in args:
            if show == 1:# копирование - на вход одномерный массив
                tempr.append(el)
            else:
                tempr.append(el[0])# создание из мейн файла - ввиду особенностей передается двумерный массив
        self.data.append(tempr)
        self.ind(self.data[len(self.data)-1], tempr)# вызов индексирования
        if show != 1:# отрисовка результата если инсерт вызван из мейна - иначе не нужно
            print(args,end =" ")
            print("was inserted!")

    def selectOneTable(self, selected_cols, where):
        print_data = []# данные для отрисовки
        headers = []# заголовок отрисовываемой таблицы
        leftwherecol = "" # левая колонка в запросе вэр
        rightwherecol = ""# правая колонка в запросе вэр
        value = "" # значение для запроса вэр(одно, ибо если их два - разбиравть не имеет смысла - читай пустой вэр)
        operator ="" # операция сравнения вэра
        rowsToPrint = []  # строки для вывода
        if len(where) > 1: # если есть вэр то записываем левую, правую колонки(или только левую и значение)
            operator = where[2][0]
            if where[0][1] == "value" and where[1][1] == "value":
                c = 0
            if where[0][1] == "value":
                value = where[0][0]
                leftwherecol = where[1][0]
            elif where[1][1] == "value":
                value = where[1][0]
                leftwherecol = where[0][0]
            else:
                leftwherecol = where[0][0]
                rightwherecol = where[1][0]
        else:
            rowsToPrint = self.data

        if rightwherecol == "": # если у нас только одна колонка:
            k = 0
            IndexCol = -1
            indexed = 0
            for name in self.colNames:# находим колонку в списке имеющихся, запоминаем айди
                if name[0] == leftwherecol:
                    IndexCol = k
                    if name[1] is not None:
                        indexed = 1
                    break
                k += 1
            if IndexCol != -1:# если она существует
                if indexed == 1:# если инексирована - выполняем поиск по индексам
                    if operator =="!=":
                        self.colNames[IndexCol][1].searchNEq(rowsToPrint, value)
                    elif operator ==">":
                        self.colNames[IndexCol][1].searchMore(rowsToPrint, value)
                    elif operator =="<":
                        self.colNames[IndexCol][1].searchLess(rowsToPrint, value)
                    elif operator ==">=":
                        self.colNames[IndexCol][1].searchMoreEq(rowsToPrint, value)
                    elif operator =="<=":
                        self.colNames[IndexCol][1].searchLessEq(rowsToPrint, value)
                    elif operator == "=":
                        self.colNames[IndexCol][1].searchEq(rowsToPrint, value)
                else:# если нет - просто проход по всей таблице
                    for c in range(0, len(self.data)):  # проходим по всем рядам таблицы, сравнивая значение столбца с заданым в вэре, если не совпадает - записываем индекс ряда на удаление
                        if operator == "=":
                            if self.data[c][IndexCol] == value:
                                rowsToPrint.append(self.data[c])
                        elif operator == ">":
                            if self.data[c][IndexCol] > value:
                                rowsToPrint.append(self.data[c])
                        elif operator == "<":
                            if self.data[c][IndexCol] < value:
                                rowsToPrint.append(self.data[c])
                        elif operator == ">=":
                            if self.data[c][IndexCol] >= value:
                                rowsToPrint.append(self.data[c])
                        elif operator == "<=":
                            if self.data[c][IndexCol] <= value:
                                rowsToPrint.append(self.data[c])
                        elif operator == "!=":
                            if self.data[c][IndexCol] != value:
                                rowsToPrint.append(self.data[c])

            elif len(where)>1:# если колонки нет и не все колонки запрашиваються - ошибка
                print("Unknown column name in where statement!")
                return
        else:# если клонки две (в основном нужно для джоина)
            IndexCol1 = -1
            IndexCol2 = -1

            k = 0
            for name in self.colNames:
                if name[0] == leftwherecol:
                    IndexCol1 = k

                    break
                k += 1
            k = 0
            for name in self.colNames:
                if name[0] == rightwherecol:
                    IndexCol2 = k

                    break
                k += 1
            if IndexCol1 != -1 and IndexCol2 != -1:# аналогично для двух столбцов ( если оба существуют)
                for c in range(0, len(self.data)):# нет смысле смотреть на индексы, так как нам все равно нужно пройти по всем рядам, тем более, что проверяеться только совпадение в ряду - а это значит, что поиск по индексу может дать неверные и лишние результаты
                    if operator =="=":
                        if self.data[c][IndexCol1] != self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
                    elif operator ==">":
                        if self.data[c][IndexCol1] <= self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
                    elif operator =="<":
                        if self.data[c][IndexCol1] >= self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
                    elif operator ==">=":
                        if self.data[c][IndexCol1] < self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
                    elif operator =="<=":
                        if self.data[c][IndexCol1] > self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
                    elif operator =="!=":
                        if self.data[c][IndexCol1] == self.data[c][IndexCol2]:
                            rowsToPrint.append(self.data[c])
            else:
                print("Unknown column name in where statement!")#если одна или обе колонки не существует в списке имен
                return
        IndexCol = []
        if len(selected_cols) <= 1 and re.search("[&]", selected_cols[0]):# если выбранные колоник меньше одной и там не спецсимвол - выбираем все
            i = 0
            for name in self.colNames:
                headers.append(name[0])
                IndexCol.append(i)
                i += 1
            print_data.append(headers)
        else:# иначе выбираем нужные
            i = 0

            for name in self.colNames:
                if name[0] in selected_cols:
                    headers.append(name[0])
                    IndexCol.append(i)
                i += 1
            if len(selected_cols) > len(IndexCol):
                print("Unknown column name was selected!")
                return
            print_data.append(headers)
        temprow = [] # в этот ряд будет идти запись ряда для вывода
        rowInd = 1
        for row in rowsToPrint:# проходим по всем выделенным рядам - нужно выбрать только правильные колонки
            c = 0
            for name in row:
                if c in IndexCol:
                    temprow.append(name)
                c += 1
            row1 = temprow.copy()  # копируем, чтобы не очистить - ведь в питоне - указатели!
            print_data.append(row1)
            temprow.clear()
            rowInd += 1

        self.print_pretty_table(print_data) # вызываем функцию отрисовки таблицы, найденную на просторах интернета


    def selectJoin(self, tbl2, selected_cols, join, where):
        FirstTableCol = join[0]# колонка из первой таблицы для джоина
        SecondTableCol = join[1]# колонка из второй таблицы для джоина
        IndexCol1 = -1 # индекс наличия колонки джоина в первой таблицы
        i = 0
        headers = []
        indexed =0
        for name in self.colNames:
            headers.append(name)
            if name[0] == FirstTableCol:
                IndexCol1 = i
                if name[1] is not None:
                    indexed +=1

            i += 1
        i = 0
        IndexCol2 = -1
        for name in tbl2.colNames:
            headers.append(name)
            if name[0] == SecondTableCol:# если столбец  существует
                IndexCol2 = i
                if name[1] is not None:
                    indexed +=1


            i += 1
        tblnew = DataBase(headers)
        if IndexCol2 == -1 or IndexCol1 == -1:# если колонки нет - отклоняем запрос
            print("There are no columns with same names!")
            return
        indleft = []# строки, в которых столбцы про которым джоин совпали из первой
        indright = []# и второй таблицы
        templeftrows = []
        checkedvalues =[]
        if indexed == 2:
            for i in range(0, len(tbl2.data)):
                if tbl2.data[i] not in checkedvalues:# если значение правой таблицы не проверялось( для двух одинаковых рядов)
                    self.colNames[IndexCol1][1].searchEq(templeftrows, tbl2.data[i][IndexCol2])# поиск по индексу
                    if len(templeftrows)>0:# если нашло - соединяем ряды и готовим к выводы записывая в новую таблицу
                        checkedvalues.append(tbl2.data[i])
                        templeftrows1 = deepcopy(templeftrows)
                        for el in templeftrows1:
                            for c in range(0, len(tbl2.colNames)):
                                el.append(tbl2.data[i][c])
                            tblnew.insert(1, el)

                    else:#иначе закидываем ряд в ненашедший пару, правый
                        el = deepcopy(tbl2.data[i])
                        for i in range(0, len(self.colNames)):
                            el.insert(0,"")
                        indright.append(el)
                    templeftrows.clear()
            checkedvalues.clear()
            templeftrows.clear()
            for i in range(0, len(self.data)):# аналогично ищем пару для ненашедших левых рядов(левой таблицы)
                if self.data[i][IndexCol1] not in checkedvalues:
                    tbl2.colNames[IndexCol2][1].searchEq(templeftrows, self.data[i][IndexCol1])
                    if len(templeftrows)>0:
                        checkedvalues.append(self.data[i][IndexCol1])
                    else:
                        el = deepcopy(self.data[i])

                        for i in range(0, len(tbl2.colNames)):
                            el.append("")
                        indleft.append(el)
                    templeftrows.clear()


            for el in indleft:# добавляем левые без пары
                tblnew.insert(1,el)
            for el in indright:# и правые
                tblnew.insert(1,el)

        else:# если нету хотя бы одного индекса - простой перебор гораздо быстрее
            for i in range(0, len(self.data)):
                for j in range(0, len(tbl2.data)):
                    if self.data[i][IndexCol1] == tbl2.data[j][IndexCol2]:
                        tblnew.insert(1, self.data[i] + tbl2.data[j])  # создаем новую таблицы из строки первой и второй, где нужные колонки совпадат
                        indright.append(j)
                        indleft.append(i)
            for i in range(0, len(self.data)):  # записываем не попавшие в список строки - добавляя пустые значения в соответствующих местах
                if i not in indleft:
                    temp = []
                    for j in range(0, tbl2.colNumber):
                        temp.append("")
                    tblnew.insert(1, self.data[i] + temp)
            for i in range(0, len(tbl2.data)):
                if i not in indright:
                    temp = []
                    for j in range(0, self.colNumber):
                        temp.append("")
                    tblnew.insert(1, temp + tbl2.data[i])


        tblnew.selectOneTable(selected_cols, where) # вызываем обычный селект для новосозданной таблицы, избегая копирования кода


    def print_pretty_table(self, data, cell_sep=' | ', header_separator=True):# функция отрисовки таблицы
        rows = len(data)
        cols = len(data[0])

        col_width = []
        for col in range(cols):
            columns = [data[row][col] for row in range(rows)]
            col_width.append(len(max(columns, key=len)))

        separator = "-+-".join('-' * n for n in col_width)

        for i, row in enumerate(range(rows)):
            if i == 1 and header_separator:
                print(separator)

            result = []
            for col in range(cols):
                item = data[row][col].rjust(col_width[col])
                result.append(item)

            print(cell_sep.join(result))

    def delete(self, where):
        if len(where)>1:# если условие есть - делаем проверки как в селекте
            leftwherecol = ""
            rightwherecol = ""
            value = ""
            if len(where) > 1:
                operator = where[2][0]
                if where[0][1] == "value":
                    value = where[0][0]
                    leftwherecol = where[1][0]
                elif where[1][1] == "value":
                    value = where[1][0]
                    leftwherecol = where[0][0]
                else:
                    leftwherecol = where[0][0]
                    rightwherecol = where[1][0]
            rowsToPrint = []# список строк на удаление
            if rightwherecol == "":  # если у нас только одна колонка:
                k = 0
                IndexCol = -1
                indexed = 0
                for name in self.colNames:  # находим колонку в списке имеющихся, запоминаем индекс
                    if name[0] == leftwherecol:
                        IndexCol = k
                        if name[1] is not None:
                            indexed = 1
                        break
                    k += 1
                if IndexCol != -1:  # если она существует
                    if indexed == 1 :# если индексирована
                        if operator == "!=":
                            self.colNames[IndexCol][1].searchNEq(rowsToPrint, value)
                        elif operator == ">":
                            self.colNames[IndexCol][1].searchMore(rowsToPrint, value)
                        elif operator == "<":
                            self.colNames[IndexCol][1].searchLess(rowsToPrint, value)
                        elif operator == ">=":
                            self.colNames[IndexCol][1].searchMoreEq(rowsToPrint, value)
                        elif operator == "<=":
                            self.colNames[IndexCol][1].searchLessEq(rowsToPrint, value)
                        elif operator == "=":
                            self.colNames[IndexCol][1].searchEq(rowsToPrint, value)
                    else:
                        for c in range(0,
                                       len(self.data)):  # проходим по всем рядам таблицы, сравнивая значение столбца с заданым в вэре, если не совпадает - записываем индекс ряда на удаление
                            if operator == "=":
                                if self.data[c][IndexCol] == value:
                                    rowsToPrint.append(self.data[c])
                            elif operator == ">":
                                if self.data[c][IndexCol] > value:
                                    rowsToPrint.append(self.data[c])
                            elif operator == "<":
                                if self.data[c][IndexCol] < value:
                                    rowsToPrint.append(self.data[c])
                            elif operator == ">=":
                                if self.data[c][IndexCol] >= value:
                                    rowsToPrint.append(self.data[c])
                            elif operator == "<=":
                                if self.data[c][IndexCol] <= value:
                                    rowsToPrint.append(self.data[c])
                            elif operator == "!=":
                                if self.data[c][IndexCol] != value:
                                    rowsToPrint.append(self.data[c])

                elif len(where) > 1:
                    print("Unknown column name in where statement!")
                    return
            else:
                IndexCol1 = -1
                IndexCol2 = -1

                k = 0
                for name in self.colNames:
                    if name[0] == leftwherecol:
                        IndexCol1 = k

                        break
                    k += 1
                k = 0
                for name in self.colNames:
                    if name[0] == rightwherecol:
                        IndexCol2 = k

                        break
                    k += 1
                if IndexCol1 != -1 and IndexCol2 != -1:  # аналогично для двух столбцов, индекс не проверяем по тем же соображениям что и раньше
                    for c in range(0, len(self.data)):
                        if operator == "=":
                            if self.data[c][IndexCol1] != self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                        elif operator == ">":
                            if self.data[c][IndexCol1] <= self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                        elif operator == "<":
                            if self.data[c][IndexCol1] >= self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                        elif operator == ">=":
                            if self.data[c][IndexCol1] < self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                        elif operator == "<=":
                            if self.data[c][IndexCol1] > self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                        elif operator == "!=":
                            if self.data[c][IndexCol1] == self.data[c][IndexCol2]:
                                rowsToPrint.append(self.data[c])
                else:
                    print("Unknown column name in where statement!")
                    return
            ind = []
            i = 0
            for el in self.colNames:
                if el[1] is not None:
                    ind.append(i)

                i+=1
            if len(ind)>0:
                for rw in rowsToPrint:
                    for el in ind:
                        self.colNames[el][1]=self.colNames[el][1].delt(rw,rw[el])# удаляем все индексы связанные с каждым рядом
                    self.data.remove(rw)# удаляем сам ряд( по ссылке в питоне нельзя удалить обьект, только изменить)


            print(len(rowsToPrint),end="")
            print(" rows were deleted from table ",end="")
        else:# иначе удаляем все
            self.data.clear()
            for cln in self.colNames:
                cln[1]= Index()# чистим индексы
            print("All data was deleted!")
