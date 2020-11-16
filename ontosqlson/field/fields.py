from ontosqlson.field.field_base import (SchemaFieldBase)
from ontosqlson.field.field_type_base import SchemaFieldTypeBase
from ontosqlson.field.field_types import (TextFieldType,
                                          IntegerFieldType,
                                          PositiveIntegerFieldType,
                                          RelationFieldType)


class TextField(SchemaFieldBase):
    def __init__(self,
                 field_name=None, default=None,
                 many=False, max_length=None,
                 validators=None, fix_value=False,
                 *args, **kwargs):
        super().__init__([TextFieldType(max_length=max_length, validators=validators, fix_value=fix_value)],
                         default=default, field_name=field_name, many=many, *args, **kwargs)


class IntegerField(SchemaFieldBase):
    def __init__(self,
                 field_name=None, default=None,
                 many=False, validators=None, fix_value=False,
                 *args, **kwargs):
        super().__init__([IntegerFieldType(validators=validators, fix_value=fix_value)],
                         default=default, field_name=field_name, many=many, *args, **kwargs)


class PositiveIntegerField(SchemaFieldBase):
    def __init__(self,
                 field_name=None, default=None,
                 many=False, validators=None, fix_value=False,
                 *args, **kwargs):
        super().__init__([PositiveIntegerFieldType(validators=validators, fix_value=fix_value)],
                         default=default, field_name=field_name, many=many, *args, **kwargs)


class RelationField(SchemaFieldBase):
    def __init__(self,
                 range_type, field_name=None,
                 default=None, many=False,
                 validators=None, fix_value=False,
                 *args, **kwargs):
        self._ensure_range_type_is_valid(range_type)
        in_range_type = self._get_range_field_type(range_type, validators, fix_value)

        super().__init__([in_range_type], default=default, field_name=field_name, many=many, *args, **kwargs)

    @staticmethod
    def _ensure_range_type_is_valid(range_type):
        check_range = range_type
        if isinstance(range_type, RelationFieldType):
            check_range = range_type.range_type
        if not isinstance(check_range, str) and not hasattr(check_range, "_meta"):
            raise ValueError("Invalid range value: Must be a schema class or a string name of a schema class")

    @staticmethod
    def _get_range_field_type(range_type, validators, fix_value):
        if not isinstance(range_type, RelationFieldType):
            return RelationFieldType(range_type, validators=validators, fix_value=fix_value)
        return range_type


class MixField(SchemaFieldBase):
    def __init__(self,
                 range_includes, field_name=None,
                 default=None, many=False,
                 validators=None, fix_value=False,
                 *args, **kwargs):
        if not range_includes:
            raise ValueError("Missing value: range_includes can not be empty")
        new_ranges = self._clean_range_includes(range_includes, validators, fix_value)
        super().__init__(new_ranges, default=default, field_name=field_name, many=many, *args, **kwargs)

    def _clean_range_includes(self, range_includes, validators, fix_value):
        new_ranges = []
        for check_range in range_includes:
            check_range = self._get_range_field_type(check_range, validators, fix_value)
            self._ensure_range_type_is_valid(check_range)
            new_ranges.append(check_range)
        return new_ranges

    @staticmethod
    def _get_range_field_type(range_type, validators, fix_value):
        if isinstance(range_type, str) or hasattr(range_type, "_meta"):
            return RelationFieldType(range_type, validators=validators, fix_value=fix_value)
        return range_type

    @staticmethod
    def _ensure_range_type_is_valid(range_type):
        if isinstance(range_type, RelationFieldType):
            check_range_type = range_type.range_type
            if not isinstance(check_range_type, str) and not hasattr(check_range_type, "_meta"):
                raise ValueError("Invalid range type: "
                                 "Must be a schema class or a string name of a schema class. "
                                 "It is {check_range_type}".format(check_range_type=check_range_type))

        if not isinstance(range_type, SchemaFieldTypeBase):
            raise ValueError("Invalid range type: {check_range} is not bae on {field_type_base}"
                             .format(check_range=range_type, field_type_base=SchemaFieldTypeBase))