from ontosqlson.schema.schema_base import SchemaBase


class Schema(metaclass=SchemaBase):
    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def load(self, data):
        meta = self._meta

        def ensure_model_exist():
            instance_of = data[meta.instance_of_field_name]
            if instance_of != meta.schema_class_name:
                raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                    schema_class_name=meta.schema_class_name, instance_of=instance_of))

        def get_class_attribute_name(schema_field_name):
            return meta.field_attribute_name_map.get(
                schema_field_name, schema_field_name)

        def try_load_related_model(value):
            schema_model = meta.schema_collection.schema_models.get(value.get(meta.instance_of_field_name, {}), None)
            if schema_model is not None:
                return create_schema_instance(schema_model, value)

        def is_schema(value):
            return meta.instance_of_field_name in value and not isinstance(value, str)

        ensure_model_exist()

        for schema_field_name in data:
            value = data[schema_field_name]
            if is_schema(value):
                value = try_load_related_model(value)

            class_attribute_name = get_class_attribute_name(schema_field_name)
            setattr(self, class_attribute_name, value)

    def save(self, data=None):
        def get_schema_field_name(class_attribute_name):
            return self._meta.attribute_field_name_map.get(class_attribute_name, class_attribute_name)

        def get_value(class_attribute_value):
            if is_schema(class_attribute_value):
                return class_attribute_value.save()
            return class_attribute_value

        def is_schema(class_attribute_value):
            return getattr(getattr(class_attribute_value, "_meta", {}), "schema_class_name", None) is not None

        if data is None:
            data = dict()

        meta = self._meta

        for class_attribute_name in meta.schema_fields:
            schema_field_name = get_schema_field_name(class_attribute_name)
            data[schema_field_name] = get_value(getattr(self, class_attribute_name))

        data[meta.instance_of_field_name] = meta.schema_class_name

        return data

    def _is_schema_type(self, schema_type):
        # TODO: Refactore this... Used by preoperty, wait until then
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


def create_schema_instance(schema, data):
    obj = schema()
    obj.load(data)
    return obj

    ####################################################################################################################

