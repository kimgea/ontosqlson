from entschema.schema.schema_base import SchemaBase


class Schema(metaclass=SchemaBase):
    def __init__(self, **kwargs):
        super().__init__()
        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def get_identification(self):
        return getattr(self, self._meta.identification_field_name, "")

    def load(self, data):
        loader = SchemaLoader(self)
        loader.load(data)
        return self

    def save(self, data=None):
        saver = SchemaSave(self)
        data = saver.save(data)
        return data

    """def _is_schema_type(self, schema_type):
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
        return False"""


def create_schema_instance(schema, data):
    obj = schema()
    obj.load(data)
    return obj

########################################################################################################################


class SchemaLoader:
    def __init__(self, schema):
        self.schema = schema
        self.meta = self.schema._meta

    def load(self, data):
        self._ensure_model_exist(data)

        for schema_field_name in data:
            value = data[schema_field_name]
            class_attribute_name = self.meta.field_attribute_name_map.get(schema_field_name, schema_field_name)

            if isinstance(value, list):
                self._load_list(schema_field_name, class_attribute_name, value)
            else:
                self._load_single(schema_field_name, class_attribute_name, value)

        return self.schema

    def _ensure_model_exist(self, data):
        instance_of = data[self.meta.instance_of_field_name]
        if instance_of != self.meta.schema_class_name:
            raise ValueError("Invalid Schema class: {schema_class_name} not in {instance_of}".format(
                schema_class_name=self.meta.schema_class_name, instance_of=instance_of))

    def _load_list(self, schema_field_name, class_attribute_name, values):
        mapped_schema_ids = dict([(schema.get_identification(), schema)
                                  for schema in self._get_attribute_data(class_attribute_name)
                                  if issubclass(type(schema), Schema)])

        none_schema_values = set([x for x in self._get_attribute_data(class_attribute_name) if not issubclass(type(x), Schema)])

        for value in values:
            if self._dictionary_is_schema(value):
                schema_found = mapped_schema_ids.get(self._get_id_from_dictionary(value), None)
                same_class_as_existing_schema = isinstance(schema_found,
                                                           self._get_schema_model(class_attribute_name, value))

                if schema_found and same_class_as_existing_schema:
                    schema_found.load(value)
                else:
                    value = self._try_load_related_model(schema_field_name, value)
                    self._get_attribute_data(class_attribute_name).append(value)
            else:
                if value not in none_schema_values:
                    self._get_attribute_data(class_attribute_name).append(value)

    def _load_single(self, schema_field_name, class_attribute_name, data):
        if self._dictionary_is_schema(data):
            schema = self._get_attribute_data(class_attribute_name)
            is_same_schema_instance = False \
                if not schema \
                else self._get_id_from_dictionary(data) == schema.get_identification()

            if is_same_schema_instance:
                data = self._get_attribute_data(class_attribute_name).load(data)
            else:
                data = self._try_load_related_model(schema_field_name, data)

        setattr(self.schema, class_attribute_name, data)

    def _try_load_related_model(self, class_attribute_name, data):
        schema_model = self._get_schema_model(class_attribute_name, data)
        if schema_model is None:
            return
        return create_schema_instance(schema_model, data)

    def _get_schema_model(self, class_attribute_name, data):
        data_schema_name = data.get(self.meta.instance_of_field_name)
        return getattr(type(self.schema), class_attribute_name).get_linked_schema_model(data_schema_name)

    def _dictionary_is_schema(self, data):
        return self.meta.instance_of_field_name in data and not isinstance(data, str)

    def _get_id_from_dictionary(self, data):
        return data.get(self.meta.identification_field_name, "")

    def _get_attribute_data(self, attribute_name):
        return getattr(self.schema, attribute_name)


########################################################################################################################


class SchemaSave:
    def __init__(self, schema):
        self.schema = schema
        self.meta = self.schema._meta

    def save(self, data=None):
        if data is None:
            data = dict()

        for class_attribute_name in self.meta.schema_fields:
            schema_field_name = self._get_schema_field_name(class_attribute_name)
            field = getattr(self.schema, class_attribute_name)
            if isinstance(field, list):
                data[schema_field_name] = self._get_value_list(field)
            else:
                data[schema_field_name] = self._get_value_single(field)

        data[self.meta.instance_of_field_name] = self.meta.schema_class_name

        return data

    def _get_schema_field_name(self, class_attribute_name):
        return self.meta.attribute_field_name_map.get(class_attribute_name, class_attribute_name)

    def _get_value_list(self, fields):
        return [self._get_value_single(field) for field in fields]

    def _get_value_single(self, field):
        if self._field_is_schema(field):
            return field.save()
        return field

    def _field_is_schema(self, field):
        return issubclass(type(field), Schema)


