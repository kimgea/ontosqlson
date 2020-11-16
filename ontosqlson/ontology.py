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
        self.schema_fields = {}

    def register_schema_model(self, schema_name, schema_model):
        self.schema_models[schema_name] = schema_model

    def register_schema_fields(self, field_name, field_instance):
        if field_name in self.schema_fields:
            raise ValueError("Field name already registered '{field_name}'".format(field_name=field_name))

        if field_instance.field_name is None:
             field_instance.field_name = field_name

        self.schema_fields[field_name] = field_instance
