from weakref import WeakKeyDictionary

from ontosqlson.ontology import Ontology


class SchemaPropertyBase(object):
    def __init__(self, range_includes, property_name=None, default=None, many=False, *args, **kwargs):
        self._many = many
        self.default = default
        self.values = WeakKeyDictionary()
        self.schema_collection = Ontology()
        self.property_name = property_name
        self._is_schema_property = True
        self.range_includes = []
        self.range_includes_classes = []
        self.range_includes_class_names = []
        for i in range_includes:
            self.range_includes.append(i)
            if hasattr(i, "_meta"):
                self.range_includes_classes.append(i)
                self.range_includes_class_names.append(i._meta.schema_class_name)
            else:
                self.range_includes_class_names.append(i)

        self._validate_default_value()

        if self.property_name:
            self._register_property()

    def _set_property_name_if_not_set(self, property_name=None):
        if self.property_name is None:
            self.property_name = property_name

    def _register_property(self, property_name=None):
        self._set_property_name_if_not_set(property_name)
        if self.property_name is None and property_name is None:
            raise ValueError("self.property_name and property_name can not both be None")
        if self.property_name is not None:
            self.schema_collection.register_schema_property(self.property_name, self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self._many:
            if instance not in self.values:
                self.values[instance] = []
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        if self._many:
            for val in value:
                self._validate_property_type(val)
        else:
            self._validate_property_type(value)
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]

    def _ensure_is_same(self, other):
        property_name = self.property_name if self.property_name is not None else other.property_name
        if not isinstance(other, type(self)):
            raise ValueError("Property of different type already registered with '{property_name}' - {original} != {property_model}" \
                .format(property_name=property_name, property_model=property_model, original=self.schema_properties[property_name]))
        for key in self.__dict__:
            if key in ("property_name",):
                if other.__dict__.get(key, "") is None or self.__dict__[key] is None:
                    continue
            if other.__dict__.get(key, "") != self.__dict__[key]:
                raise ValueError("Property with different attributes already registered on '{property_name}' - {key}: {original} != {new_value}" \
                    .format(property_name=property_name, new_value=other.__dict__.get(key, ""), original=self.__dict__[key], key=key))

    def _validate_default_value(self):
        if self.default is None:
            return
        self._validate_property_type(self.default)

    def _validate_property_type(self, value):
        if hasattr(value, "_meta"):
            for ok_range in self.range_includes_class_names:
                if value._is_schema_type(ok_range):
                    return

            raise ValueError("Invalid property type: {value} not in {range_includes}".format(
                value=value._meta.schema_class_name, range_includes=self.range_includes_class_names))

        if isinstance(value, str) and str in self.range_includes:
            return
        if isinstance(value, int) and int in self.range_includes:
            return

        raise ValueError("Invalid property type: {value} not in {range_includes}".format(
            value=type(value), range_includes=self.range_includes_class_names))