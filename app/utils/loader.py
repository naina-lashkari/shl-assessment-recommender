import json


def load_assessments():

    with open("data/assessments.json", "r") as file:
        assessments = json.load(file)

    return assessments