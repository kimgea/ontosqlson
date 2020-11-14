from collections import OrderedDict

from ontosqlson.ontology import Ontology


class Meta:
    def __init__(self, owner=None):

        # self.local_fields = list()  # TODO: Nesesary to generate json ontology schemas. Can wait
        self.model = owner
        self.concrete_model = owner  # TODO: remove model concrete_model
        self.object_name = self.model.__name__
        self.schema_class_name = self.object_name
        self.instance_of_field_name = "instance_of"
        self.parents = OrderedDict()
        self.ascendants = dict()
        self.property_name_attribute_name_lookup = {}
        self.attribute_name_property_name_lookup = {}
        self.schema_collection = Ontology()

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


def _update_meta_with_custom_meta(new_meta, custom_meta):
    if not custom_meta:
        return

    for attr_name in custom_meta.__dict__:
        if attr_name.startswith('__'):
            continue  # Skipp python specific stuff
        setattr(new_meta, attr_name, custom_meta.__dict__[attr_name])


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


