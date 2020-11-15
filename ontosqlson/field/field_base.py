from weakref import WeakKeyDictionary
from ontosqlson.ontology import Ontology


class SchemaFieldTypeBase:
    def __init__(self, validators=None):
        self.validators = validators if validators else []

    def is_valid(self, value):
        for validator in self.validators:
            if not validator.is_valid(value):
                return False
        return True


class SchemaFieldBase(object):
    def __init__(self, range_includes, field_name=None, default=None, many=False, *args, **kwargs):
        self.values = WeakKeyDictionary()
        self.schema_collection = Ontology()

        self.field_name = field_name
        self._many = many
        self.default = default

        self.range_includes = []
        self.range_includes_classes = []
        self.range_includes_class_names = []
        _set_range_includes(self, range_includes)

        _ensure_validate_default_value(self)

        if self.field_name:
            _register_field(self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many and instance not in self.values:
            self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if self._many:
            _ensure_validate_field_types(self, value)
        else:
            _ensure_validate_field_type(self, value)
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


def _set_range_includes(field, range_includes):
    for i in range_includes:
        field.range_includes.append(i)
        if hasattr(i, "_meta"):
            field.range_includes_classes.append(i)
            field.range_includes_class_names.append(i._meta.schema_class_name)
        else:
            field.range_includes_class_names.append(i)


def _set_field_name_if_not_set(field, field_name=None):
    if field.field_name is None:
        field.field_name = field_name


def _register_field(field, field_name=None):
    _set_field_name_if_not_set(field, field_name)

    if field.field_name is None and field_name is None:
        raise ValueError("self.field_name and field_name can not both be None")

    if field.field_name is not None:
        field.schema_collection.register_schema_fields(field.field_name, field)


def _ensure_validate_default_value(field):
    if field.default is None:
        return

    _ensure_validate_field_type(field, field.default)


def _ensure_validate_field_types(field, values: list):
    [_ensure_validate_field_type(field, value) for value in values]


def _ensure_validate_field_type(field, value):
    if not any(ok_range.is_valid(value) for ok_range in field.range_includes):
        raise ValueError("Invalid field type: {value} not in {range_includes}".format(
            value=type(value), range_includes=field.range_includes_class_names))
