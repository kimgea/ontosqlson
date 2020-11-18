from ontosqlson.field.field_type_base import SchemaFieldTypeBase, SchemaFieldTypeClass, SchemaFieldTypeDataType
from ontosqlson.field.validators import IsStringValidator, MaxLengthValidator, IsIntegerValidator, \
    GreaterThanValidator, IsSchemaTypeValidator


class TextFieldType(SchemaFieldTypeDataType, SchemaFieldTypeBase):
    def __init__(self, max_length=None, validators=None, fix_value=False):
        super().__init__("Text", validators=validators, fix_value=fix_value)
        self.validators.append(IsStringValidator())
        self.validators.append(MaxLengthValidator(max_length=max_length))


class IntegerFieldType(SchemaFieldTypeDataType, SchemaFieldTypeBase):
    def __init__(self, validators=None, fix_value=False):
        super().__init__("Integer", validators=validators, fix_value=fix_value)
        self.validators.append(IsIntegerValidator())


class PositiveIntegerFieldType(SchemaFieldTypeDataType, SchemaFieldTypeBase):
    def __init__(self, validators=None, fix_value=False):
        super().__init__("PositiveInteger", validators=validators, fix_value=fix_value)
        self.validators.append(IsIntegerValidator())
        self.validators.append(GreaterThanValidator(min_value=0))


class RelationFieldType(SchemaFieldTypeClass, SchemaFieldTypeBase):
    def __init__(self, range_type, validators=None, fix_value=False):
        super().__init__("text", validators=validators, fix_value=fix_value)
        self.range_type = range_type
        self.validators.append(IsSchemaTypeValidator(self.range_type))