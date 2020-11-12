from ontosqlson.property_base import SchemaPropertyBase


class TextProperty(SchemaPropertyBase):
    def __init__(self, property_name=None, default=None, many=False, *args, **kwargs):
        super().__init__([str], default=default, property_name=property_name, many=many, *args, **kwargs)


class IntegerProperty(SchemaPropertyBase):
    def __init__(self, property_name=None, default=None, many=False, *args, **kwargs):
        super().__init__([int], default=default, property_name=property_name, many=many, *args, **kwargs)


class PositiveIntegerProperty(SchemaPropertyBase):
    def __init__(self, property_name=None, default=None, many=False, *args, **kwargs):
        super().__init__([int], default=default, property_name=property_name, many=many, *args, **kwargs)


class ClassProperty(SchemaPropertyBase):
    def __init__(self, range_type, property_name=None, default=None, many=False, *args, **kwargs):
        if not isinstance(range_type, str) and not hasattr(range_type, "_meta"):
            raise ValueError("Invalid range value: Must be a schema class or a string name of a schema class")
        super().__init__([range_type], default=default, property_name=property_name, many=many, *args, **kwargs)


class ClassPropertyMix(SchemaPropertyBase):
    def __init__(self, range_includes, property_name=None, default=None, many=False, *args, **kwargs):
        if not range_includes:
            raise ValueError("Missing value: range_includes can not be empty")
        for range_type in range_includes:
            if not isinstance(range_type, str) and not hasattr(range_type, "_meta"):
                raise ValueError(
                    "Invalid range value: Must be a schema class or a string name of a schema class - {range_type}"
                        .format(range_type=range_type))
        super().__init__(range_includes, default=default, property_name=property_name, many=many, *args, **kwargs)