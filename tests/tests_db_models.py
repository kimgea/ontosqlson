import unittest
from ontosqlson.schema import Schema
from ontosqlson.field import (TextField,
                              RelationField,
                              MixField,
                              IntegerField)


########################################################################################################################


# NB: Not propper test by using Schema as standing for a db model class.
# Test are only to check tath it shoulf be easelt possible. Acural retrieval has to many dependancies to add to project



class ThingModel(Schema):
    id = TextField()
    name = TextField()


class PersonModel(Schema):
    id = TextField()
    thing = RelationField(ThingModel)
    birth_place = TextField()


class OrganizationModel(Schema):
    id = TextField()
    thing = RelationField(ThingModel)
    org_nr = TextField()


class CreativeWorkModel(Schema):
    id = TextField()
    thing = RelationField(ThingModel)


class BookEditionModel(Schema):
    id = TextField()
    creative_work = RelationField(CreativeWorkModel)
    isbn = TextField()


class ContributorModel(Schema):
    id = TextField()
    creative_work = RelationField(CreativeWorkModel)
    contributor = MixField([PersonModel, OrganizationModel])
    role = TextField()


########################################################################################################################


class SchemaExtended(Schema):

    def __init_subclass__(cls, db_model=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if db_model is not None:
            cls._db_model = db_model

    def get_from_db(self, id, db, schema=None):
        # Do db lookup logick inside here. Using simplified mock no as proof of concept
        for instance in db.get(self._meta.schema_class_name, []):
            if instance.id != id:
                continue
            if schema is None:
                schema = self._meta.concrete_model()
            self._get_from_db_attributes(instance, schema)
            self._get_from_db_relations(instance, schema, db)
            for parent_key in self._meta.parents:
                parent = self._meta.parents[parent_key]()
                parent.get_from_db(id, db, schema)
        return schema

    def _get_from_db_attributes(self, instance, schema):
        pass

    def _get_from_db_relations(self, instance, schema, db):
        pass

    def save_to_db(self, db=None, schema=None, related=None):
        # Do db lookup logick inside here. Using simplified mock no as proof of concept
        if db is None:
            db = {}

        if isinstance(self._meta.concrete_model, SchemaExtended):
            return None

        if schema is None:
            schema = self

        if db.get(self._meta.schema_class_name, None) is None:
            db[self._meta.schema_class_name] = []

        # get existing isntance
        instance = None
        if schema.id is not None:
            for temp in db.get(self._meta.schema_class_name, []):
                if temp.id == schema.id:
                    instance = temp
        if instance is None and getattr(self, "_db_model", None) is not None:
            instance = self._db_model()
            if schema.id is not None:
                instance.id = schema.id
                db[self._meta.schema_class_name].append(instance)
        if instance is None:
            return None

        for parent_key in self._meta.parents:
            parent = self._meta.parents[parent_key]()
            parent_isntance = parent.save_to_db(db=db, schema=schema)

        self._save_to_db_self_no_relations(instance, schema, db, related)

        return instance

    def _save_to_db_self_no_relations(self, instance, schema, db, related):
        pass


class PersonLink(SchemaExtended):
    id = TextField()
    name = TextField()

    def _get_from_db_attributes(self, instance, schema):
        schema.name = instance.thing.name
        schema.id = instance.thing.id

    class Meta:
        schema_class_name = "Person"


class OrganizationLink(SchemaExtended):
    id = TextField()
    name = TextField()

    def _get_from_db_attributes(self, instance, schema):
        schema.name = instance.thing.name
        schema.id = instance.thing.id

    class Meta:
        schema_class_name = "Organization"


class Contributor(SchemaExtended, db_model=ContributorModel):
    contributor = MixField([PersonLink, OrganizationLink])
    is_type = TextField()  # TODO: Make chouse or enum field
    role = TextField()

    def _get_from_db_attributes(self, instance, schema):
        schema.id = instance.id
        schema.role = instance.role

    def _get_from_db_relations(self, instance, schema, db):
        for contr in db.get("Person", []):
            if contr.id != instance.contributor.id:
                continue
            contributor = PersonLink()
            contrib_schema = contributor.get_from_db(contr.id, db)
            schema.contributor = contrib_schema
            schema.is_type = "person"
        for contr in db.get("Organization", []):
            if contr.id != instance.contributor.id:
                continue
            contributor = OrganizationLink()
            contrib_schema = contributor.get_from_db(contr.id, db)
            schema.contributor = contrib_schema
            schema.is_type = "company"

    def _save_to_db_self_no_relations(self, instance, schema, db, related):
        instance.role = schema.role
        for contr in db.get("Organization", []):
            if contr.id == schema.contributor.id:
                instance.contributor = contr
        for contr in db.get("Person", []):
            if contr.id == schema.contributor.id:
                instance.contributor = contr
        if related is not None:
            instance.creative_work = related


class Thing(SchemaExtended, db_model=ThingModel):
    id = TextField()
    name = TextField()

    def _get_from_db_attributes(self, instance, schema):
        schema.id = instance.id
        schema.name = instance.name

    def _save_to_db_self_no_relations(self, instance, schema, db, related):
        instance.id = schema.id
        instance.name = schema.name


class CreativeWork(Thing, db_model=CreativeWorkModel):
    contributors = RelationField(Contributor, many=True)

    def _get_from_db_attributes(self, instance, schema):
        pass

    def _get_from_db_relations(self, instance, schema, db):
        for contr in db.get("Contributor", []):
            if contr.creative_work.id != instance.id:
                continue
            contributor = Contributor()
            contrib_schema = contributor.get_from_db(contr.id, db)
            schema.contributors.append(contrib_schema)

    def _save_to_db_self_no_relations(self, instance, schema, db, related):
        instance.id = schema.id
        for works in db.get("Thing", []):
            if works.id == schema.id:
                instance.thing = works
        # Save before next
        for contrib in schema.contributors:
            contrib.save_to_db(db, related=instance)


class BookEdition(CreativeWork, db_model=BookEditionModel):
    isbn = TextField()

    def _get_from_db_attributes(self, instance, schema):
        schema.isbn = instance.isbn

    def _get_from_db_relations(self, instance, schema, db):
        pass

    def _save_to_db_self_no_relations(self, instance, schema, db, related):
        instance.id = schema.id
        instance.isbn = schema.isbn
        for works in db.get("CreativeWork", []):
            if works.id == schema.id:
                instance.creative_work = works


########################################################################################################################



class TestDbModels(unittest.TestCase):

    def test_retrieve_from_db_models(self):

        thing_model_edition = ThingModel(name="edition1", id="1")
        creative_work_model_edition = CreativeWorkModel(thing=thing_model_edition, id=thing_model_edition.id)
        edition_model = BookEditionModel(
            isbn="123456789", creative_work=creative_work_model_edition, id=thing_model_edition.id)

        thing_model_person = ThingModel(name="person1", id="2")
        person_model = PersonModel(thing=thing_model_person, birth_place="a place", id=thing_model_person.id)

        thing_model_org = ThingModel(name="org1", id="3")
        org_model = OrganizationModel(thing=thing_model_org, org_nr="abc123", id=thing_model_org.id)

        contributor1_model = ContributorModel(
            creative_work=edition_model,
            contributor=person_model,
            role="author", id="c1")
        contributor2_model = ContributorModel(
            creative_work=edition_model,
            contributor=org_model,
            role="distributor", id="c2")

        db = {
            "Thing": [thing_model_edition, thing_model_person, thing_model_org],
            "CreativeWork": [creative_work_model_edition],
            "BookEdition": [edition_model],
            "Person": [person_model],
            "Organization": [org_model],
            "Contributor": [contributor1_model, contributor2_model],
        }

        getter = BookEdition()
        edition = getter.get_from_db("1", db)

        self.assertEqual(edition.isbn, "123456789")
        self.assertEqual(edition.id, "1")
        self.assertEqual(edition.name, "edition1")

        self.assertEqual(edition.contributors[0].contributor.name, "person1")
        self.assertEqual(edition.contributors[0].contributor.id, "2")
        self.assertEqual(edition.contributors[0].role, "author")
        self.assertEqual(edition.contributors[0].is_type, "person")

        self.assertEqual(edition.contributors[1].contributor.name, "org1")
        self.assertEqual(edition.contributors[1].contributor.id, "3")
        self.assertEqual(edition.contributors[1].role, "distributor")
        self.assertEqual(edition.contributors[1].is_type, "company")

    def test_store_to_db_models(self):
        edition = BookEdition(id="1", name="edition1", isbn="123456789")
        edition.contributors.append(
            Contributor(id="c1", role="author", contributor=PersonLink(id="2", name="person1")))
        edition.contributors.append(
            Contributor(id="c2", role="distributor", contributor=OrganizationLink(id="3", name="org1")))

        thing_model_person = ThingModel(name="person1", id="2")
        person_model = PersonModel(thing=thing_model_person, birth_place="a place", id=thing_model_person.id)
        thing_model_org = ThingModel(name="org1", id="3")
        org_model = OrganizationModel(thing=thing_model_org, org_nr="abc123", id=thing_model_org.id)
        db = {
            "Thing": [thing_model_org, thing_model_person],
            "Organization": [org_model],
            "Person": [person_model]
        }

        edition.save_to_db(db)
        self.assertEqual(db["BookEdition"][0].isbn, "123456789")
        self.assertEqual(db["BookEdition"][0].creative_work.thing.id, "1")
        self.assertEqual(db["BookEdition"][0].creative_work.thing.name, "edition1")

        self.assertEqual(db["Thing"][2].id, "1")
        self.assertEqual(db["Thing"][2].name, "edition1")

        self.assertEqual(db["Contributor"][0].id, "c1")
        self.assertEqual(db["Contributor"][0].role, "author")
        self.assertEqual(db["Contributor"][0].creative_work.id, "1")
        self.assertEqual(db["Contributor"][0].contributor.id, "2")

        self.assertEqual(db["Contributor"][1].id, "c2")
        self.assertEqual(db["Contributor"][1].role, "distributor")
        self.assertEqual(db["Contributor"][1].creative_work.id, "1")
        self.assertEqual(db["Contributor"][1].contributor.id, "3")
