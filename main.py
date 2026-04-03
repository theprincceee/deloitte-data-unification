# import the necessary modules and libraries
import json
import unittest
import datetime

# use the open function to open read the three json files
with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)

with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)

with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


# helper function to convert ISO timestamp to milliseconds
def iso_to_millis(iso_str):
    dt = datetime.datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=datetime.timezone.utc)  # 🔥 FIX HERE
    return int(dt.timestamp() * 1000)
# convert json data from format 1 to the expected format
def convertFromFormat1(jsonObject):

    locationParts = jsonObject["location"].split("/")

    result = {
        "deviceID": jsonObject["deviceID"],
        "deviceType": jsonObject["deviceType"],
        "timestamp": jsonObject["timestamp"],  # already in milliseconds
        "location": {
            "country": locationParts[0],
            "city": locationParts[1],
            "area": locationParts[2],
            "factory": locationParts[3],
            "section": locationParts[4],
        },
        "data": {
            "status": jsonObject["operationStatus"],
            "temperature": jsonObject["temp"],
        },
    }

    return result


# convert json data from format 2 to the expected format
def convertFromFormat2(jsonObject):

    timestamp = iso_to_millis(jsonObject["timestamp"])

    result = {
        "deviceID": jsonObject["device"]["id"],
        "deviceType": jsonObject["device"]["type"],
        "timestamp": timestamp,
        "location": {
            "country": jsonObject["country"],
            "city": jsonObject["city"],
            "area": jsonObject["area"],
            "factory": jsonObject["factory"],
            "section": jsonObject["section"],
        },
        "data": {
            "status": jsonObject["data"]["status"],
            "temperature": jsonObject["data"]["temperature"],
        },
    }

    return result


def main(jsonObject):

    if jsonObject.get("device") is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)


# Test cases using unittest module
class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        result = main(jsonData1)
        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 1 failed",
        )

    def test_dataType2(self):
        result = main(jsonData2)
        self.assertEqual(
            result,
            jsonExpectedResult,
            "Converting from Type 2 failed",
        )


if __name__ == "__main__":
    unittest.main()