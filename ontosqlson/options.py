from collections import OrderedDict

from ontosqlson.ontology import Ontology


class Options:
    def __init__(self, meta, parents):
        self._meta = meta
        self._parents_holder = parents

        # self.local_fields = list()  # TODO: Nesesary to generate json ontology schemas. Can wait

        self.schema_class_name = None
        self.parents = OrderedDict()
        self.ascendants = dict()
        self.concrete_model = None

    def _get_ascendants(self):
        if not self.parents:
            return self.ascendants

        if self.ascendants:
            # Already processed
            return self.ascendants

        for parent_name in self.parents:
            parent = self.parents[parent_name]
            self.ascendants[parent._meta.object_name] = parent
            partent_ascendants = parent._meta._get_ascendants()
            if partent_ascendants:
                self.ascendants.update(partent_ascendants)

        return self.ascendants

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.model = cls

        # Default values
        self.object_name = cls.__name__
        self.schema_class_name = self.object_name
        self.instance_of_field_name = "instance_of"

        self.schema_collection = Ontology()

        if self._parents_holder:
            for parent in self._parents_holder:
                if not hasattr(parent, "_meta"):
                    continue
                self.parents[parent._meta.object_name] = parent
        del self._parents_holder

        self._get_ascendants()

        if self._meta:
            meta_attrs = self._meta.__dict__.copy()
            for name in self._meta.__dict__:
                if name.startswith('__'):
                    del meta_attrs[name]
            for attr_name in meta_attrs:
                if attr_name in meta_attrs:
                    setattr(self, attr_name, meta_attrs[attr_name])
                elif hasattr(self.meta, attr_name):
                    setattr(self, attr_name, getattr(self._meta, attr_name))
        del self._meta