import inspect

from ontosqlson.options import Options


class SchemaBase(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        super_new = super().__new__
        # Also ensure initialization is only performed for subclasses of Schema
        # (excluding Schema class itself).
        parents = [b for b in bases if isinstance(b, SchemaBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Create the class.
        module = attrs.pop('__module__')
        new_attrs = {'__module__': module}
        classcell = attrs.pop('__classcell__', None)
        if classcell is not None:
            new_attrs['__classcell__'] = classcell
        attr_meta = attrs.pop('Meta', None)

        contributable_attrs = {}
        for obj_name, obj in list(attrs.items()):
            if _has_contribute_to_class(obj):
                contributable_attrs[obj_name] = obj
            else:
                new_attrs[obj_name] = obj

        new_class = super_new(cls, name, bases, new_attrs, **kwargs)

        meta = attr_meta or getattr(new_class, 'Meta', None)
        new_class.add_to_class('_meta', Options(meta, parents))

        # Add remaining attributes (those with a contribute_to_class() method)
        # to the class.
        for obj_name, obj in contributable_attrs.items():
            new_class.add_to_class(obj_name, obj)

        new_class._meta.concrete_model = new_class
        new_class._meta.schema_collection.register_schema_model(
            new_class._meta.schema_class_name, new_class._meta.concrete_model)

        new_class._property_name_attribute_name_lookup = {}
        new_class._attribute_name_property_name_lookup = {}
        for key in new_class._get_fields(new_class, schema_field_only=True):
            getattr(new_class, key)._register_property(key)
            new_class._property_name_attribute_name_lookup[getattr(new_class, key).property_name] = key
            new_class._attribute_name_property_name_lookup[key] = getattr(new_class, key).property_name



        """def _include_attr(obj, attr):
            if attr != "name":
                return False
            print("_-_-_-_")
            print(attr)
            print(dir(obj.name))
            print(getattr(obj, attr))

            print(getattr(getattr(obj, attr), "__dict__"))
            print(getattr(getattr(obj, attr), "_is_schema_property"))
            if getattr(getattr(obj, attr), "_is_schema_property", False):
                return True
            return False
        # return set([attr for attr in dir(self) if _include_attr(attr)])
        # print(dir(new_class))
        print( set([attr for attr in dir(new_class) if _include_attr(new_class, attr)]))"""

        return new_class

    def add_to_class(cls, name, value):
        if _has_contribute_to_class(value):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


def _has_contribute_to_class(value):
    return not inspect.isclass(value) and hasattr(value, 'contribute_to_class')