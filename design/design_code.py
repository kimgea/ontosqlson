
"""


    Just a place to write none functional code to get exampel designs before coding starts



    TODO: Remove this later

"""


"""
class StringFieldType:
    def __init__(self, *args, **kwargs):
        pass


class SchemaFieldType:
    def __init__(self, *args, **kwargs):
        pass


class Field:
    def __init__(self, *args, **kwargs):
        pass


class ThingSchema:
    title = Field([StringFieldType()])


class PersonSchema(ThingSchema):
    pass


class OrgSchema(ThingSchema):
    pass


class WorkSchema(ThingSchema):
    copyrightHolder = Field([SchemaFieldType(PersonSchema), OrgSchema])


class BookSchema(WorkSchema):
    pages = Field()
    citation = Field([WorkSchema, StringFieldType()])




person = PersonSchema()
org = OrgSchema()
work = WorkSchema()
book = BookSchema()

book.copyrightHolder = []
book.copyrightHolder.append(person)
book.copyrightHolder.append(org)
book.copyrightHolder.append("Invalid")  # ERROR: Not allowed

book.citation = []
book.citation.append(work)
book.citation.append("title of a none mapped book")
book.citation.append(person)  # ERROR: Not allowed

"""