class FieldValidatorBase:
    def is_valid(self, value):
        return True


class IsStringValidator(FieldValidatorBase):
    def is_valid(self, value):
        return isinstance(value, str)


class IsIntegerValidator(FieldValidatorBase):
    def is_valid(self, value):
        return isinstance(value, int)


class GreaterThanValidator(FieldValidatorBase):
    def __init__(self, min_value=None):
        self.min_value = min_value

    def is_valid(self, value):
        return value >= self.min_value


class MaxLengthValidator(FieldValidatorBase):
    def __init__(self, max_length=None):
        self.max_length = max_length

    @property
    def max_length(self):
        return self._max_length

    @max_length.setter
    def max_length(self, value):
        if value is None:
            value = 0
        if value < 0:
            value = 0
        self._max_length = value

    def is_valid(self, value):
        return self.max_length == 0 or len(value) <= self.max_length


class IsSchemaTypeValidator(FieldValidatorBase):
    def __init__(self, range_type=None):
        self.range_type = range_type

    def is_valid(self, value):
        return hasattr(value, "_meta") and value._is_schema_type(self.range_type)