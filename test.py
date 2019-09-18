import os


class A:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

class B:
	def __init__(self):
		pass

	def get(self):
		self.a = A(1,3)
		return self.a

a = A(1, 2)
print(a.x, a.y)
b = B()
a = b.get()
print(a.x, a.y)