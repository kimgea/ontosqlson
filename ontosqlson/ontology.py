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
        # TODO: Rewrite so this also save model and not instance... if possible

        if field_name not in self.schema_fields:
            if field_instance.field_name is None:
                 field_instance.field_name = field_name

            self.schema_fields[field_name] = field_instance
        else:
            _ensure_fields_is_same(self.schema_fields[field_name], field_instance)


def _ensure_fields_is_same(one, two):
    # TODO: Probably belongs in field_base.py Dont want this to link to it...
    #  Might have to add it on field_base class

    def range_includes_is_valid(value_one, value_two):
        if len(value_one) != len(value_two):
            return False
        return all(type(r1) == type(r2) for r1, r2 in zip(value_one, value_two))

    field_name = one.field_name if one.field_name is not None else two.field_name

    if not isinstance(two, type(one)):
        raise ValueError("Field of different type already registered with "
                         "'{field_name}' - {original} != {field_model}"
                         .format(field_name=field_name,
                                 field_model=one._meta.concrete_model,
                                 original=one.schema_fields[field_name]))
    for key in one.__dict__:
        value_one = one.__dict__[key]
        value_two = two.__dict__.get(key, "")

        # Special checks
        if key in ("range_includes", "range_includes_class_names") \
                and range_includes_is_valid(value_one, value_two):
            continue

        # Regular equal check
        if value_one != value_two:
            raise ValueError("Field with different attributes already registered on "
                             "'{field_name}' - {key}: {original} != {new_value}"
                             .format(field_name=field_name,
                                     new_value=value_two,
                                     original=value_one,
                                     key=key))
