import unittest
import copy


def get_initial_import_show_json():
    json_import = dict(
        meta=dict(
            client="wikidata",
            version=1
        ),
        data=[
            dict(
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
        ]
    )
    return json_import


def bump_version(old_json):
    if old_json.get("meta", {}).get("version", None) != 1:
        return old_json

    old_data = old_json.get("data", [])
    data = copy.deepcopy(old_data)

    for idx, item in enumerate(old_data):
        for field in item:
            if field == "p1476":
                data[idx]["title"] = data[idx].pop(field)
            elif field == "p136":
                data[idx]["genre"] = data[idx].pop(field)
            elif field == "p170":
                data[idx]["creator"] = data[idx].pop(field)
            elif field == "p793":
                for sub_idx, subitems in enumerate(item[field]):
                    for subfield in subitems:
                        if subfield == "p585":
                            data[idx][field][sub_idx]["point_in_time"] = data[idx][field][sub_idx].pop(subfield)
                        elif subfield == "p276":
                            data[idx][field][sub_idx]["location"] = data[idx][field][sub_idx].pop(subfield)
                data[idx]["significant_event"] = data[idx].pop(field)

    new_json = dict(
        meta=dict(
            client="wikidata",
            version=2
        ),
        data=data
    )

    return new_json


class TestVersionBumpJsons(unittest.TestCase):

    def test_convert_json_version_bump(self):
        json_import = get_initial_import_show_json()

        self.assertTrue("meta" in json_import)
        self.assertTrue(all("id" in line for line in json_import["data"]))
        self.assertTrue(all("url" in line for line in json_import["data"]))
        self.assertTrue(all("p1476" in line for line in json_import["data"]))
        self.assertTrue(all("p136" in line for line in json_import["data"]))
        self.assertTrue(all("p170" in line for line in json_import["data"]))
        self.assertTrue(all("p793" in line for line in json_import["data"]))

        self.assertTrue(all("p585" in line2 for line in json_import["data"] for line2 in line["p793"]))
        self.assertTrue(all("p276" in line2 for line in json_import["data"] for line2 in line["p793"]))

        json_import = bump_version(json_import)

        #print(json_import)
        self.assertTrue("meta" in json_import)

        self.assertTrue(all("id" in line for line in json_import["data"]))
        self.assertTrue(all("url" in line for line in json_import["data"]))
        self.assertTrue(all("title" in line for line in json_import["data"]))
        self.assertTrue(all("genre" in line for line in json_import["data"]))
        self.assertTrue(all("creator" in line for line in json_import["data"]))
        self.assertTrue(all("significant_event" in line for line in json_import["data"]))

        self.assertTrue(all("point_in_time" in line2 for line in json_import["data"] for line2 in line["significant_event"]))
        self.assertTrue(all("location" in line2 for line in json_import["data"] for line2 in line["significant_event"]))