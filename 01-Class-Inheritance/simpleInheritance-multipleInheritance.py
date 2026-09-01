# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 22:58:10 2026

@author: pabda
"""

class Person:
    
    def __init__(self, name):
        self.name = name
        
    def introduceYourself(self):
        print(f"Hi, my name is {self.name}")
        
class Activity:
    
    def __init__(self, activity_name):
        self.activity_name = activity_name
        
    def activityToDo(self):
        pass
    
# Student class who inherint to Person and Activity
class Student(Person, Activity):
    
    def __init__(self, name, course, activity_name):
        # Initialize
        Person.__init__(self, name)
        Activity.__init__(self, activity_name)
        self.course = course
        
    def doActivity(self):
        print(f" I'm {self.name} and I'm participating on the activity: {self.activity_name}")
        
    def homeworks(self):
        print(f"Hi, I'm {self.name}, and I'm doing my homework, currently I'm in to the course: {self.course}")
        
# Generate instance
student1 = Student(name="Juan", course="10th grade",activity_name="Football")
student1.introduceYourself()
student1.doActivity()
student1.homeworks()

# Remember
# -- The Python ihnerint allow to the clases all the attributes and methods from the base class, prommoting
#    the code reutilization and the system modularity