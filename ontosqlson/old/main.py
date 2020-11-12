from itertools import chain
import inspect
from weakref import WeakKeyDictionary
import copy
from collections import OrderedDict, defaultdict
import sys
import threading


lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SchemaCollection(metaclass=Singleton):
    def __init__(self):
        self.schema_models = {}

    def register_schema_model(self, schema_name, schema_model):
        self.schema_models[schema_name] = schema_model


        


class SchemaPropertyBase(object):
    def __init__(self, many=False):
        self._many = many
        self.default = None
        self.values = WeakKeyDictionary()
        self.defaults = WeakKeyDictionary()

    """def __call__(self, default=None):
        self.default = default
        return self   """

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many:
            if instance not in self.values:
                self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]

   

name_property = SchemaPropertyBase()
age_property = SchemaPropertyBase()
descritpion_property = SchemaPropertyBase()
identification_property = SchemaPropertyBase(many=True)

class Thing:
    name = name_property

class Thing2:
    name = name_property


#def custom_dir(instance):
#    res = 

Thing3 = type("Thing3", (), {"name":name_property})



thing = Thing()
print(thing.name)
thing.name = "test"
print(thing.name)
#print(thing.__dir__())

thing2 = Thing2()
print(thing2.name)
thing2.name = "test2"
print(thing2.name)
#print(thing2.__dir__())

thing3 = Thing3()
print(thing3.name)
thing3.name = "test3"
print(thing3.name)
#print(thing3.__dir__())
#thing3.name