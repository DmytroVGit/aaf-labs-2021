class Index:
    def __init__(self ):# создание индекса при создании индексированой колнки в виде бинарного дереве
        self.right = None#правое поддерево
        self.str = None # значение в узле
        self.left = None# левое поддерево
        self.id = None# ряд, проиндексированый

    def add(self, str, id):# добавление ряда в индекс - для каждой колонки отдельно
        if self.str is None:
            self.str = str
            self.id = id
            return
        else:
            if self.str <= str:# добавляем в дерево по значению колонки
                if self.right is None:
                    self.right = Index()
                self.right.add(str,id)
            else:
                if self.left is None:
                    self.left = Index()
                self.left.add(str, id)
    def rebuild(self, right, left, new):# перестройка дерева для удаления, когда удаялется узел с двумя потомками - создается новое поддерево из потомков
        if right is not None:
            new.add(right.str, right.id)
            new.rebuild(right.right, right.left, new)
        if left is not None:
            new.add(left.str, left.id)
            new.rebuild(left.right, left.left, new)


    def delt(self, id, str):
        if self.str == str and self.id == id:# если это наш узел то:
            if self.right is None and self.left is None:#если листовой - удаляем его

                del self
                return None

            elif self.right is None and self.left is not None:# если есть только левый потомок то подставляем его вместо удаленного

                return self.left
            elif self.right is not None and self.left is None:# если есть только правый

                return self.right
            else:# если есть два - перестройка
                new = Index()

                self.rebuild(self.right, self.left, new)
                return new
        elif self.str < str or(self.str == str and self.id != id):# если узел не на удаление - по рекурсии вызываем функцию, в результате либо вернет узел вместо удаленного, либо неизмененный узел, если узел под удаление дальше
            if self.right is not None:
                self.right = self.right.delt(id, str)
        elif self.str > str:
            if self.left is not None:
                self.left =  self.left.delt(id, str)
        return self

    def searchNEq(self, array, str):# поиски - обычные, по дереву, сравнивается узел дерева и значение self.str *operation* str operation = =|!=|>|<|>=|<=
        if self.str < str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchNEq(array, str)
        elif self.str > str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchNEq(array, str)
            if self.left is not None:
                self.left.searchNEq(array, str)
        else:

            if self.right is not None:
                self.right.searchNEq(array, str)

    def searchEq(self, array, str):
        if self.str < str:
            if self.right is not None:
                self.right.searchEq(array, str)
        elif self.str > str:
            if self.left is not None:
                self.left.searchEq(array, str)
        else:
            array.append(self.id)
            if self.right is not None:
                self.right.searchEq(array, str)
    def searchMore(self, array, str):
        if self.str > str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchMore(array, str)
            if self.left is not None:
                self.left.searchMore(array, str)
        elif self.str < str:

            if self.right is not None:
                self.right.searchMore(array, str)
        else:
            if self.right is not None:
                self.right.searchMore(array, str)

    def searchLess(self, array, str):
        if self.str < str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchLess(array, str)
            if self.left is not None:
                self.left.searchLess(array, str)
        elif self.str > str:

            if self.left is not None:
                self.left.searchLess(array, str)
        else:
            if self.right is not None:
                self.right.searchLess(array, str)

    def searchMoreEq(self, array, str):
        if self.str >= str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchMoreEq(array, str)
            if self.left is not None:
                self.left.searchMoreEq(array, str)
        elif self.str < str:

            if self.right is not None:
                self.right.searchMoreEq(array, str)


    def searchLessEq(self, array, str):
        if self.str < str:
            array.append(self.id)
            if self.right is not None:
                self.right.searchLessEq(array, str)
            if self.left is not None:
                self.left.searchLessEq(array, str)
        elif self.str > str:

            if self.left is not None:
                self.left.searchLessEq(array, str)
        else:
            array.append(self.id)
            if self.right is not None:
                self.right.searchLessEq(array, str)