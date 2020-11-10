"""
def GetArea(width, height):
    area = width * height
    return area
ret1 = GetArea(6,9)
print(ret1)
"""

'''
listname = ["anla",'tylen','hank']
listchinese = [100,70,82]
listtmath = [87, 88,65]
listenglish=[79,100,8]
print("name",'nus','A',"B",'C')
for i in range(0,3):
    print(listname[i].ljust(5),str(i+1).rjust(3),)
'''
'''    
import os 

print(os.getcwd())
'''

'''
class Animal():
     def fly(seif):
        print('時速20公里!!')

class Bird(Animal):
    def fly(self,speed):
        print("時速"+str(speed)+"公里!")

class Plane():
    def fly(self):
        print("時速1000公里!")
def fly(speed):
    print("時速"+str(speed)+"英里!!")

amimal = Animal()
amimal.fly()

bird = Bird()
bird.fly(60,)

plane=Plane()
plane.fly()

fly(5)


print(amimal,bird,plane,fly)
'''

''''''


class Father():
    def __init__(self, name):
        self.name = name
        self.__eye = '黑色'

    def getEye(self):
        return self.__eye


class Child(Father):
    def __init__(self, name, eye):
        super().__init__(name)
        self.eye = eye
        self.fatherEye = super().getEye()


joe = Child("小華", "棕色")
print(joe.name + joe.eye + joe.fatherEye)

'''           
class A(object):
   def __init__(self):
    print("Enter A")
    print("Leave A")

class B(A):
   def __init__(self):
    print("Enter B")
    A.__init__(self)
    print("Leave B")

class C(A):
   def __init__(self):
    print("Enter C")
    A.__init__(self)
    print("Leave C")

class D(A):
   def __init__(self):
    print("Enter D")
    A.__init__(self)
    print("Leave D")

class E(B, C, D):
   def __init__(self):
    print("Enter E")
    B.__init__(self)
    C.__init__(self)
    D.__init__(self)
    print("Leave E")

E()      
'''

''' 
def xxx(s):
	stack = []
	paren_map = {')':'(',']':'[','}':'{'}
	for c in s:
		if c not in paren_map:
			stack.append(c)
		elif not stack or paren_map[c] != stack.pop():
			return False
	return not stack
if __name__ == '__main__':
	xxx("([{}]){}")

 '''

''' 
class A(object):
   def __init__(self):
    print("Enter A")
    print("Leave A")

class B(A):
   def __init__(self):
    print("Enter B")
    super(B, self).__init__()
    print("Leave B")

class C(A):
   def __init__(self):
    print("Enter C")
    super(C, self).__init__()
    print("Leave C")

class D(A):
   def __init__(self):
    print("Enter D")
    super(D, self).__init__()
    print("Leave D")

class E(B, C, D):
   def __init__(self):
    print("Enter E")
    super(E, self).__init__()
    print("Leave E")

E()          
'''





