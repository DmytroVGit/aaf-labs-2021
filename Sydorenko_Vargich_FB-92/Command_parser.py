import re




def split_command(_string):
    result =[]
    _string = re.sub("\\s+", " ", _string)
    _string = re.sub("\\(\\s*", " (", _string)
    _string = re.sub("\\s*\\)", ",)", _string)
    _string = re.sub("\\s*,\\s*", ",", _string)
    _string = _string.strip() # избавляемся от лишних пробелов - пробелы больше одного, и в начале+конце команды
    splitedCommand = _string.split(" ")

    if re.match("(?i)create", splitedCommand[0]):# если криейт - начинаем парсить как для нее
        result.append(["create", "command"])# закидываем в результат команду и подпись - что это команда
        _string = _string.replace(splitedCommand[0] + " ", "", 1)# удаляем ненужное из строки - будет удобнее парсить дальше
        if re.match("\w*", splitedCommand[1]):# если название таблицы из букв цифр и _ - то записываем его и после удаляем из строки
            result.append([splitedCommand[1], "name"])
            _string = _string.replace(splitedCommand[1] + " ", "", 1).strip()
            if re.match("[(](?:\w+(\s+\w+)?[,])+[)]", _string):# если то, что осталось - выглядит как скобки с названиямми столбцов и возможно наличием слова индексев - идем дальше
                _string = _string.replace("(", "")
                _string = _string.replace(")", "")# убираем скобки
                args = _string.split(",")# разбиваем по запятой - и разбираем названия столбцов
                del args[-1]# удаляем последний елемент - он всегда пустой
                for arg in args:# проходим по всем элементам если одно слово - столбец не индексированый(1), если два - второе индексед или ошибка
                    if re.match("\s*\w+\s+(?i)indexed\s*", arg):
                        result.append([arg.split(" ")[0], "1"])
                    elif re.match("\s*\w+\s*", arg):
                        result.append([arg, "0"])
                    else :
                        result.clear()
                        result.append(["error", "bad col name!"])
                        return result
            else:
                result.clear()
                result.append(["error", "bad col names!"])
                return result
        else:
            result.clear()
            result.append(["error", "bad table name!"])
            return result
    elif re.match("(?i)insert", splitedCommand[0]):# аналогично с инсертом
        result.append(["insert", "command"])
        _string = _string.replace(splitedCommand[0], "", 1).strip()
        if re.match("(?i)into", splitedCommand[1]):# если есть слово инту - удаляем, если нет, то и не важно
            _string = _string.replace(splitedCommand[1], "", 1).strip()
        splitedCommand = _string.split(" ")
        if re.match("\w*", splitedCommand[0]): # проверяем имя на правильность
            result.append([splitedCommand[0], "name"])
            _string = _string.replace(splitedCommand[0], "", 1).strip()
            if re.match('[(](?:["]\s*[^,;"]+\s*["][,])+[)]', _string):# проверяем, правильно ли введены данные
                _string = _string.replace("(", "")
                _string = _string.replace(")", "")
                _string = _string.replace('"', "").strip() # удаляем лишнее и разбиваем на отдельные значения
                args = _string.split(",")
                del args[-1]
                for arg in args:

                    if re.match('\s*[^,;"]+\s*', arg):
                        result.append([arg.strip(), "0"])#записываем значения
                    else:
                        result.clear()
                        result.append(["error", "wrong column name!"])
                        return result
            else:
                result.clear()
                result.append(["error", "wrong column names!"])
                return result
        else:
            result.clear()
            result.append(["error", "bad table name!"])
            return result
    elif re.match("(?i)select", splitedCommand[0]):# аналогично предыдущим
        result.append(["select", "command"])
        _string = _string.replace(splitedCommand[0] + " ", "", 1).strip()
        if re.search("\s+(?i)from\s+", _string):
            splitSearch = re.split("\s+(?i)from\s+", _string) #проверяем наличие ключевого фром
            if re.match("\s*[*]\s*",splitSearch[0]):# если звездочка - записываем спецсимвол как название - тогда при обработке будет ясно, что нужно взять все колонки
                result.append(["&", "col name"])
            elif re.match("(?:\s*\w+\s*[,])+", splitSearch[0]+","):
                cols = splitSearch[0].split(",")
                for col in cols:
                   result.append([col, "col name"])# иначе записываем названия колонок
            else:
                result.clear()
                result.append(["error", "wrong columns in select!"])
                return result
            splitedCommand = splitSearch[1].strip().split(" ")
            if re.match("\s*\w+\s*", splitedCommand[0]):# проверяем имя таблицы
                result.append([splitedCommand[0], "name"])
            else:
                result.clear()
                result.append(["error", "wrong table name!"])
                return result
            if re.search("\s+(?i)full_join\s+", _string) and re.search("\s+(?i)where\s+", _string):# проверяем не идет ли джоин после вэра
                if re.search("\s+(?i)full_join\s+", _string).start() > re.search("\s+(?i)where\s+", _string).start():
                    result.clear()
                    result.append(["error", "join statement after where statement!"])
                    return result
            if re.search("\s+(?i)full_join\s+", _string):# проверяем фул джоин на имя второй таблицы и правильного условия соединения
                _string0 = _string.strip()
                _string0 = re.split("\s+(?i)full_join\s+", _string0)[1].strip()
                _string0 = re.split("(?i)where", _string0)[0].strip()
                if re.match("\s*\w+(\s+((?i)on)\s+\w+\s+[=]\s+\w+\s*)\s*", _string0):
                    if re.search("(?i)on", _string0):
                        result.append([re.split("(?i)on", _string0)[0], "name2"])
                        _string0=re.split("(?i)on", _string0)[1].strip()
                        condition = _string0.split(" ")
                        result.append([condition[0], "full_join"])
                        result.append([condition[2], "full_join"])

                    else:
                        result.clear()
                        result.append(["error", "wrong full_join statement(missed on statement)!"])
                        return result
                else:
                    result.clear()
                    result.append(["error", "wrong full_join statement!"])
                    return result
            if re.search("\s+(?i)where\s+", _string):# проеверяем вэр на правильность записи условий
                _string0 = _string.strip()
                _string0 = re.split("\s+(?i)where\s+", _string0)[1].strip()
                if re.match('\s*[\w]+|("[^,;]+")\s+[=]|[!][=]|[>]|[<]|[>][=]|[<][=]\s+[\w+]|["[^,;]+"]\s*', _string0):
                    condition = _string0.split(" ")
                    if re.match('"', condition[0]):
                        result.append([condition[0].replace('"', "").replace('"', ""), "value"])
                    else:
                        result.append([condition[0], "where_col"])
                    if re.match('"', condition[2]):
                        result.append([condition[2].replace('"', "").replace('"', ""), "value"])
                    else:
                        result.append([condition[2], "where_col"])
                    result.append([condition[1], "where_operation"])
                else:
                    result.clear()
                    result.append(["error", "wrong where statement!"])
                    return result
            else:
                result.append(["&", "where"])
        else:
            result.clear()
            result.append(["error", "wrong usage of select!"])
            return result
    elif re.match("(?i)delete", splitedCommand[0]):# делит - абсолютно аналогично
        result.append(["delete", "command"])
        _string = _string.replace(splitedCommand[0] + " ", "", 1)
        if re.match("(?i)from", splitedCommand[1]):
            splitedCommand = _string.split(" ")
        if re.match("\s*\w+\s*", splitedCommand[1]):
            result.append([splitedCommand[1], "name"])
        else:
            result.clear()
            result.append(["error", "wrong table name!"])
            return result
        if re.search("(?i)where", _string):
            _string0 = _string.strip()
            _string0 = re.split("(?i)where", _string0)[1]
            if re.match('\s*[\w+]|["\w+"]\s+[=]|[!][=]|[>]|[<]|[>][=]|[<][=]\s+[\w+]|["\w+"]\s*', _string0):
                _string0=_string0.strip()
                condition = _string0.split(" ")
                if re.match('"', condition[0]):
                    result.append([condition[0].replace('"', "").replace('"', ""), "value"])
                else:
                    result.append([condition[0], "where_col"])
                if re.match('"', condition[2]):
                    result.append([condition[2].replace('"', "").replace('"', ""), "value"])
                else:
                    result.append([condition[2], "where_col"])
                result.append([condition[1], "where_operation"])
            else:
                result.clear()
                result.append(["error", "wrong where statement!"])
                return result
    else:
        result.clear()
        result.append(["error", "unrecognized command!"])
    return result
