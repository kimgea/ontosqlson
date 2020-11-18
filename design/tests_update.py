import unittest
import copy
import json


json_import1 = dict(
                id="Q56876444",
                url="https://www.wikidata.org/wiki/Q56876444",
                p1476="The Mandalorian1",
                p136=[
                    dict(title="science fiction television2", url="https://www.wikidata.org/wiki/Q336059", id="Q336059"),
                    dict(title="Space Western1", url="https://www.wikidata.org/wiki/Q4235011", id="Q4235011")
                ],
                p170=[
                    dict(title="Jon Favreau", url="https://www.wikidata.org/wiki/Q295964", id="Q295964")
                ]
            )


json_import2 = dict(
                id="Q56876444",
                url="https://www.wikidata.org/wiki/Q56876444",
                p1476="The Mandalorian",
                p136=[
                    dict(title="Space Western", url="https://www.wikidata.org/wiki/Q4235011", id="Q4235011"),
                    dict(title="adventure film", url="https://www.wikidata.org/wiki/Q319221", id="Q319221")
                ],
                p793=[
                    dict(title="première", url="https://www.wikidata.org/wiki/Q204854", id="Q204854",
                         p585=[dict(title="13 November 2019")],
                         p276=[dict(title="El Capitan Theatre", url="https://www.wikidata.org/wiki/Q849284", id="Q849284")]
                         )
                ]
            )


json_import3 = dict(
                id="Q56876444",
                url="https://www.wikidata.org/wiki/Q56876444",
                p1476="The Mandalorian",
                p136=[
                    dict(title="science fiction television", url="https://www.wikidata.org/wiki/Q336059", id="Q336059"),
                    dict(title="Space Western", url="https://www.wikidata.org/wiki/Q4235011", id="Q4235011"),
                    dict(title="adventure film", url="https://www.wikidata.org/wiki/Q319221", id="Q319221")
                ],
                p170=[
                    dict(title="Jon Favreau", url="https://www.wikidata.org/wiki/Q295964", id="Q295964")
                ],
                p793=[
                    dict(title="première", url="https://www.wikidata.org/wiki/Q204854", id="Q204854",
                         p585=[dict(title="13 November 2019")],
                         p276=[dict(title="El Capitan Theatre", url="https://www.wikidata.org/wiki/Q849284", id="Q849284")]
                         )
                ]
            )


def update(old, new):
    for key in old:
        if key not in new:
            continue
        if isinstance(old[key], list):
            if isinstance(new[key], list):
                old[key] = update(old[key], new[key])
            continue
        if isinstance(old[key], dict):
            if isinstance(new[key], dict):
                old[key] = update(old[key], new[key])
            continue
        old[key] = new[key]
    return old



class TestUpdateJsons(unittest.TestCase):

    def test_update_jsons(self):
        data1 = copy.deepcopy(json_import1)
        data2 = copy.deepcopy(json_import2)
        data3 = copy.deepcopy(json_import3)

        print(data1)
        update(data1, data2)
        out = json.dumps(data1)
        print(out)

