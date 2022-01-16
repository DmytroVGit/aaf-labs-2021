import re

Create = '\s*(?i)create\s+(?P<name>\w+)\s+[(](\s*\w+\s*)((?i)indexed)?\s*([,](\s*\w+\s*)((?i)indexed)?\s*)*\s*[)]\s*$'
Insert = '\s*(?i)insert(\s+(?i)into)?\s+(?P<name>\w+)\s+[(](\s*["]\s*[^;,]+\s*["]\s*)\s*([,](\s*["]\s*[^;,]+\s*["]\s*)\s*)*\s*[)]\s*$'
Delete = '\s*(?i)delete\s+((?i)from\s)?\s*(?P<name>\w+)(\s+(?i)where\s+(?P<wh1>["]\s*[^;,]+\s*["]|\w+)\s*(?P<wh3>[=]|[!][=]|[>]|[<]|[>][=]|[<][=])\s*(?P<wh2>["]\s*[^;,]+\s*["]|\w+)\s*)?\s*$'
Select1 = '\s*(?i)select\s+(?:[*]|(\w+(\s*[,]\s*\w+\s*)*))\s*$'
Select2 = '\s*(?P<name>\w+)(\s+(?i)full_join\s+(?P<name2>\w+)\s+(?i)on\s+(?P<fj1>\w+)\s*[=]\s*(?P<fj2>\w+)\s*)?(\s+(?i)where\s+(?P<wh1>["]\s*[^;,]+\s*["]|\w+)\s*(?P<wh3>[=]|[!][=]|[>]|[<]|[>][=]|[<][=])\s*(?P<wh2>["]\s*[^;,]+\s*["]|\w+)\s*)?\s*$'


def split_command(_string):
    result =[]
    _string = re.sub("\\s+", " ", _string)
    _string = re.sub("\\(\\s*", " (", _string)
    _string = re.sub("\\s*\\)", ")", _string)
    _string = re.sub("\\s*,\\s*", ",", _string)
    _string = _string.strip() # избавляемся от лишних пробелов - пробелы больше одного, и в начале+конце команды
    if re.match(Create,_string):
        m = re.match(Create,_string)
        result.append(["create", "command"])
        Lstr = _string.split(" ")
        result.append([m.group("name"), "name"])
        tmp = _string.split(m.group("name"))[0]
        _string = _string.split(tmp+m.group("name"))[1]
        _string = re.sub("[(]", "",_string)
        _string = re.sub("[)]", "",_string).strip()
        Lstr = _string.split(",")
        #del Lstr[len(Lstr)-1]
        for el in Lstr:
            if len(el.split(" "))>=2:
                result.append([el.split(" ")[0].strip(),"1"])
            else:
                result.append([el.strip(),"0"])
    elif re.match(Delete,_string):
        m = re.search(Delete,_string)
        result.append(["delete", "command"])
        result.append([m.group("name"), "name"])
        if m.group("wh1"):
            if re.search('["]', m.group("wh1")):
                result.append([m.group("wh1").replace('"',"").strip(), "value"])
            else:
                result.append([m.group("wh1").strip(), "col"])

            if re.search('["]', m.group("wh2")):
                result.append([m.group("wh2").replace('"', "").strip(), "value"])
            else:
                result.append([m.group("wh2").strip(), "col"])
            result.append([m.group("wh3"),"oper"])
    elif re.match(Insert, _string):
        m = re.search(Insert,_string)
        result.append(["insert", "command"])
        result.append([m.group("name"), "name"])
        tmp = _string.split(m.group("name"))[0]
        _string = _string.split(tmp+m.group("name"))[1]
        _string = re.sub("[(]", "",_string)
        _string = re.sub("[)]", "",_string).strip()
        _string = re.sub('["]', "",_string).strip()
        Lstr = _string.split(",")
        #del Lstr[len(Lstr) - 1]
        for el in Lstr:
            result.append([el.strip(), "0"])
    elif re.search("\s+(?i)from\s+",_string):
        _string1,_string2 = re.split("\s+(?i)from\s+",_string)
        m1 = re.match(Select1, _string1)
        m2 = re.match(Select2, _string2)
        if m1 and m2:
            result.append(["select","command"])
            result.append([m2.group("name"),"name"])
            _string1 = re.split("\s*(?i)select\s+",_string1)[1]
            Lstr = _string1.split(",")
            if Lstr[0].strip()=="*":
                result.append(["&","col name"])
            else:
                #del Lstr[len(Lstr)-1]
                for el in Lstr:
                    result.append([el.strip(),"col name"])
            if m2.group("name2"):
                result.append([m2.group("name2"),"name2"])
            if m2.group("fj1"):
                result.append([m2.group("fj1"),"full_join"])
            if m2.group("fj2"):
                result.append([m2.group("fj2"),"full_join"])
            if m2.group("wh1"):
                if re.search('["]', m2.group("wh1")):
                    result.append([m2.group("wh1").replace('"', "").strip(), "value"])
                else:
                    result.append([m2.group("wh1").strip(), "col"])

                if re.search('["]', m2.group("wh2")):
                    result.append([m2.group("wh2").replace('"', "").strip(), "value"])
                else:
                    result.append([m2.group("wh2").strip(), "col"])
                result.append([m2.group("wh3"), "oper"])
        else:
            result.append(["error","wrong select!"])
    else:
        result.append(["error","unknown command!"])
    return result