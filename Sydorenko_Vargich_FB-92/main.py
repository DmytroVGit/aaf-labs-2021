
from base import Base

if __name__ == '__main__':
    base1 = Base()
    base1.insert([1, 2, 3, 4, 5, 6])
    base1.insert([1, 7 , 8])
    base1.insert([0, 3, 5])
    base1.insert([-1, -3, 5, 0])
    base1.insert([1,5,4,-1,-2,7,0])
    base1.print()
    base1.contains([1, 8, 7])
    base1.search()
    base1.searchInt([1,7,9])
    base1.searchCont([1, 7])
    base1.searchContby([7,8,9,10,1,2,3,4,5,6])



