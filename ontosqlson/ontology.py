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

    def register_schema_property(self, property_name, property_instance):
        # TODO: Rewrite so this also save model and not instance... if possible

        if property_name not in self.schema_properties:
            if property_instance.property_name is None:
                 property_instance.property_name = property_name

            self.schema_properties[property_name] = property_instance
        else:
            _ensure_properties_is_same(self.schema_properties[property_name], property_instance)


def _ensure_properties_is_same(one, two):
    # TODO: Probably belongs in property_base.py Dont want this to link to it...
    #  Might have to add it on property_base class

    property_name = one.property_name if one.property_name is not None else two.property_name

    if not isinstance(two, type(one)):
        raise ValueError("Property of different type already registered with "
                         "'{property_name}' - {original} != {property_model}"
                         .format(property_name=property_name,
                                 property_model=one._meta.concrete_model,
                                 original=one.schema_properties[property_name]))
    for key in one.__dict__:
        value_one = one.__dict__[key]
        value_two = two.__dict__.get(key, "")

        if value_one != value_two:
            raise ValueError("Property with different attributes already registered on "
                             "'{property_name}' - {key}: {original} != {new_value}"
                             .format(property_name=property_name,
                                     new_value=value_two,
                                     original=value_one,
                                     key=key))
