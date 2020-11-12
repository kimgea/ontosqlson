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


class Ontology(metaclass=Singleton):
    def __init__(self):
        self.schema_models = {}
        self.schema_properties = {}

    def register_schema_model(self, schema_name, schema_model):
        self.schema_models[schema_name] = schema_model

    def register_schema_property(self, property_name, property_model):
        if property_name not in self.schema_properties:
            if property_model.property_name is None:
                 property_model.property_name = property_name
            self.schema_properties[property_name] = property_model
            return
        self.schema_properties[property_name]._ensure_is_same(property_model)