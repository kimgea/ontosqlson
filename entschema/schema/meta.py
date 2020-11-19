from collections import OrderedDict


class Meta:
    def __init__(self, owner=None):
        self.concrete_model = owner
        self.object_name = self.concrete_model.__name__
        self.schema_class_name = self.object_name
        self.instance_of_field_name = "instance_of"
        self.identification_field_name = "id"
        self.parents = OrderedDict()
        self.ascendants = dict()
        self.field_attribute_name_map = {}
        self.attribute_field_name_map = {}
        self.schema_fields = []
        self.regular_attributes = []


def set_meta(owner, custom_meta, parents):
    owner._meta = Meta(owner)

    _set_valid_parents(owner._meta, parents)
    _set_ascendants(owner._meta)
    _update_meta_with_custom_meta(owner._meta, custom_meta)


def _set_valid_parents(new_meta, parents):
    for parent in parents:
        if parent.__name__ == "Schema" or not hasattr(parent, "_meta"):
           continue
        new_meta.parents[parent._meta.object_name] = parent


def _set_ascendants(meta):
    if not meta.parents:
        return meta.ascendants

    if meta.ascendants:
        # Already processed
        return meta.ascendants

    for parent_name in meta.parents:
        parent = meta.parents[parent_name]
        meta.ascendants[parent._meta.object_name] = parent
        parent_ascendants = _set_ascendants(parent._meta)  # Recursive

        if parent_ascendants:
            meta.ascendants.update(parent_ascendants)

    return meta.ascendants


def _update_meta_with_custom_meta(new_meta, custom_meta):
    if not custom_meta:
        return

    for attr_name in custom_meta.__dict__:
        if attr_name.startswith('__'):
            continue  # Skipp python specific stuff
        setattr(new_meta, attr_name, custom_meta.__dict__[attr_name])
