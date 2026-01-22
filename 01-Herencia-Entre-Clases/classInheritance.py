# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 22:22:59 2026

@author: pabda
"""

# Base class

class Animal:
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def sound(self):
        pass
    
    def information(self):
        print(f"My name it's: {self.name}, and I've {self.age} years old")
        

# Son class
class Dog(Animal):
    
    def __init__(self, name, age, race):
        # Initialize base class
        Animal.__init__(self, name, age)
        self.race = race
        
    def sound(self):
        return "Guau!"
    
class Cat(Animal):
    
    def __init__(self, name, age, color):
        # Initialize base class
        super().__init__(name, age)
        self.color = color
        
    def sound(self):
        return "Miau!"
    
# Instances creations
dog1 = Dog(name="Alaska", age=3, race="Husky")
cat1 = Cat(name="Whiskers", age=4, color="Siamese")


#call all methods
print(f"{dog1.name} says: {dog1.sound()}")
print(f"{cat1.name} says: {cat1.sound()}")


#Print information
dog1.information()
cat1.information()

# Remember:
# -- The python inherint foments the code reutilization avoidint the duplicity
#    and making easier the modularity and scalability
# -- The subclases amplyes or addapt the behavior of the superclass through the adition 
#    or attributes and method writes, bring them flexibility and personalization at the classes 
#    design and all the program behavior