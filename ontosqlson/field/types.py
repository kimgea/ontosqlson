from ontosqlson.field.field_base import SchemaFieldTypeBase
from ontosqlson.field.validators import IsStringValidator, MaxLengthValidator, IsIntegerValidator, \
    GreaterThanValidator, IsSchemaTypeValidator


class TextFieldType(SchemaFieldTypeBase):
    def __init__(self, max_length=None, validators=None):
        super().__init__(validators=validators)
        self.validators.append(IsStringValidator())
        self.validators.append(MaxLengthValidator(max_length=max_length))


class IntegerFieldType(SchemaFieldTypeBase):
    def __init__(self, validators=None):
        super().__init__(validators=validators)
        self.validators.append(IsIntegerValidator())


class PositiveIntegerFieldType(SchemaFieldTypeBase):
    def __init__(self, validators=None):
        super().__init__(validators=validators)
        self.validators.append(IsIntegerValidator())
        self.validators.append(GreaterThanValidator(min_value=0))


class RelationFieldType(SchemaFieldTypeBase):
    def __init__(self, range_type, validators=None):
        super().__init__(validators=validators)
        self.range_type = range_type
        self.validators.append(IsSchemaTypeValidator(self.range_type))