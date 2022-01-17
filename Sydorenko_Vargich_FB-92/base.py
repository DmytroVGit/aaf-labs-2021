from copy import deepcopy


class Base:
    def __init__(self):
        self.data = []
        self.id = -1
        self.rows = []

    def insert(self, args):
        id = self.id + 1
        self.id = self.id + 1
        args = sorted(args)
        rw = Row(id, args)
        self.rows.append(rw)
        ind = []
        rm = []
        for i in range(0, len(self.data)):
            for el in args:
                if self.data[i][0] == el:
                    self.data[i][1].append(id)
                    rm.append(el)
                elif self.data[i][0] > el:
                    ind.append([i, el])
                    rm.append(el)
            for el in rm:
                args.remove(el)
            rm.clear()
        for el in args:
            self.data.append([el,[id]])
        for i in range(0, len(ind)):
            rw = [ind[len(ind) - i - 1][1], [id]]
            self.data.insert(ind[len(ind) - i - 1][0], rw)

    def print(self):
        for el in self.data:
            print(el[0], end= ":")
            for i in range(0,len(el[1])):
                print(" s",end ="")
                if i != len(el[1])-1:
                    print(el[1][i], end = ",")
                else:
                    print(el[1][i])

    def contains(self, args):
        print("Contains", end=" ")
        print(args)
        args = sorted(args)
        check = None
        for el in self.data:
            if el[0] == args[0]:
                check = deepcopy(el[1])
                break
        if check is None:
            print(False)
            return False
        for el in check:
            if self.rows[el].row == args:
                print(True)
                return True
        print(False)
        return False
    def search(self):
        print("Search all:")
        for el in self.rows:
            print("s", end="")
            print(el.id, end = ": ")
            print (el.row)

    def searchInt(self, args):
        print("Intersects with", end = " ")
        print(args)
        res = []
        for el in self.data:
            if el[0] in args:
                for i in el[1]:
                    res.append(i)
        res = list(set(res))
        for el in res:
            print("s", end="")
            print(self.rows[el].id, end=": ")
            print(self.rows[el].row)
    def searchCont(self, args):
        print("Search contains", end=" ")
        print(args)
        args = sorted(args)
        check = None
        for el in self.data:
            if el[0] == args[0]:
                check = deepcopy(el[1])
                break
        if check is None:
            print("")
            return
        for el in check:
            if  set(args).issubset(set(self.rows[el].row)):
                print("s", end="")
                print(self.rows[el].id, end=": ")
                print(self.rows[el].row)
        print("")
        return
    def searchContby(self,args):
        print("Search contained_by", end=" ")
        print(args)
        args = sorted(args)
        check = []
        for el in self.data:
            for i in args:
                if el[0] == i:
                    temp = deepcopy(el[1])
                    check = check + temp
        check = list(set(check))
        if len(check)==0:
            print("")
            return
        for el in check:
            if set(self.rows[el].row).issubset(set(args)):
                print("s", end="")
                print(self.rows[el].id, end=": ")
                print(self.rows[el].row)
        print("")
        return
class Row:
    def __init__(self, id, args):
        self.id = id
        self.row = []
        for el in args:
            self.row.append(el)

