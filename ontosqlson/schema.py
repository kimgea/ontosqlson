import inspect
from ontosqlson.schema_base import SchemaBase
from ontosqlson.ontology import Ontology


class Schema(metaclass=SchemaBase):
    def __init__(self, **kwargs):

        self._ontology = Ontology()

        fields = self._get_fields()
        if kwargs:
            for key in kwargs.keys():
                if key in fields:
                    setattr(self, key, kwargs[key])
        super().__init__()

    def load(self, data):
        instance_of = data[self._meta.instance_of_field_name]
        if instance_of != self._meta.schema_class_name:
            raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                schema_class_name=self._meta.schema_class_name, instance_of=instance_of))

        # TODO: Code below is suposed to be for when a class can be part of multiple schemas.... but not working. second part match against partial strings, not only lists
        """try:
            if instance_of != self._meta.schema_class_name:
                raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                    schema_class_name=self._meta.schema_class_name, instance_of=instance_of))
        except:
            if self._meta.schema_class_name not in instance_of:
                raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                    schema_class_name=self._meta.schema_class_name, instance_of=instance_of))"""

        for property_name in data.keys():
            attribute_name = self._property_name_attribute_name_lookup.get(property_name, property_name)
            try:
                if getattr(self, attribute_name)._is_schema_property:
                    property_name = getattr(self, attribute_name).property_name
            except AttributeError:
                pass

            value = data[property_name]
            try:
                if self._meta.instance_of_field_name in value:
                    obj = self._meta.schema_collection.schema_models[value[self._meta.instance_of_field_name]]()
                    obj.load(value)
                    value = obj
            except TypeError:
                pass
            setattr(self, attribute_name, value)

    def dump(self, data=None):
        if data is None:
            data = dict()
        fields = self._get_fields(schema_field_only=True)
        for key in fields:
            property_name = self._attribute_name_property_name_lookup.get(key, key)
            if getattr(getattr(getattr(self, key), "_meta", {}), "schema_class_name", None) is not None:
                data[property_name] = getattr(self, key).dump(data[key])
            else:
                data[property_name] = getattr(self, key)
        data[self._meta.instance_of_field_name] = self._meta.schema_class_name
        return data

    def _get_fields(self, schema_field_only=False):
        def _include_attr(attr):
            if attr.startswith("__"):
                return False
            if callable(getattr(self, attr)):
                return False
            if schema_field_only:
                if getattr(getattr(self._meta.concrete_model, attr, {}), "_is_schema_property", False):
                    return True
                return False

            return True
        return set([attr[0] for attr in inspect.getmembers(self) if _include_attr(attr[0])])

    def _is_schema_type(self, schema_type):
        if isinstance(schema_type, str):
            if self._meta.schema_class_name == schema_type:
                return True
            for ascendant in self._meta.ascendants.values():
                if ascendant._meta.schema_class_name == schema_type:
                    return True
            return False
        if self._meta.concrete_model == schema_type:
            return True
        for ascendant in self._meta.ascendants.values():
            if ascendant._meta.concrete_model == schema_type:
                return True
        return False

