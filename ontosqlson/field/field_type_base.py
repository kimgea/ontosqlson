class SchemaFieldTypeClass:
    pass


class SchemaFieldTypeDataType:
    pass


class SchemaFieldTypeBase:
    def __init__(self, range_name, validators=None, fix_value=False):
        self.validators = validators if validators else []
        self._range_name = range_name
        self._fix_value = fix_value

    @property
    def range_name(self):
        return self._range_name

    def is_valid(self, value):
        for validator in self.validators:
            if not validator.is_valid(value):
                return False
        return True

    def try_fix_value(self, value):
        if not self._fix_value:
            return value
        new_value = value
        for validator in self.validators:
            if not validator.is_valid(value) and validator.should_fix_it():
                new_value = validator.fix_it(new_value)
        if self.is_valid(new_value):
            return new_value
        return value
