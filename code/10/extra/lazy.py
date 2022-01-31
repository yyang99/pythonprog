# lazy.py

class Lazy:
    def __init__(self, func):
        self.func = func
    def __set_name__(self, owner, name):
        self.key = name
    def __get__(self, instance, owner):
        if instance:
            value = self.func(instance)
            instance.__dict__[self.key] = value
            return value
        else:
            return self

class Rectangle:
    area = Lazy(lambda self: self.length * self.height)
    perimeter = Lazy(lambda self: 2 * self.height + 2 * self.width)
    def __init__(self, width, height):
        self.length = width
        self.height = height
    
