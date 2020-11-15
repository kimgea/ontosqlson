# ontosqlson  (Work in progress)

## Purpose
- Create a simplified ontology data structure with python classes
- Map json into classes (schemas) in this ontology 
- Validate the data (ontology like rules)
- import and export from and to these classes/schemas and json data
- Map from different json structure into a created ontology setup
- Map from this ontology json and into sql tables (mainly json column, but should be possiblr to map some fields to other columns)


## Why
Going to be used for importing, storing, and displaying data in a django project

### Represent data structure
- Look at first part of purpose

### Import
- Import API takes many diferent json structures. Import client is free to choose
- mapping rules will be used to map thise imports into a internal structure

### Storing main internal structure
- Jsonb column in postges wil be used as a document storage
- A class/schema in an ontology must be able to be mapped to a corresponding table
- A classes/shemas parents might be mapped to different tables. A relation mus be mapped
- Fields must be able to be mapped to corresponding columns or related tables
- Fields comming from a parrent schema must know what schema it belongs to so it can map to correct table
- This project should not be tightly connected to django and its tools
- (A little to detaild...)


## TODO:

### Next (Both steps below propably requires some rewriting):
1. Look for the todos in the code and refactor them
2. Refactor some of the functions. Bad names and bade placing on some of them.
3. Must be able to set a default value if vailidator fails, but only if set, else fail totaly. Like cutting on max tring length?
4. Give better invalid message feed back. Not correct message right now... Gather them up, or something

### Later:

#### Refactor Property 
- In progress

#### Check that correct exeption types are used
- Small refactor job

#### Should some exeption less (or as much as possible) be implemented?
- ?

#### schamas with multiple instance_of types 
- Probably requires som major rewrites. 
- Not sure if supporting this is nessesary for my usage

#### Store invalid data? 
- data in maped fields that are invalid 
- in invalid structure. 
- Append __invalid, or seperate _invalid = {} field 
- Is it nesessary? 
- Can propbably wait)

### Versioning?
- Important

#### Map between json structures. 
- From differently mapped json and into this schema ontology 
- Important feature 
- Try to keep it as seperate as possible)

#### Map to sql db. 
- All in json column. 
- But some shoud be posible to map other palces. Relations, and so on....  
- Use field and schema arguments, source???? 
- Important feature 
- Try to keep it seperate as possible

#### Support multiple ontologies? 
- class Thing(Schema, ontology_name="a_name"):  
- Should not be to hard

#### Fin a better project name
- Later