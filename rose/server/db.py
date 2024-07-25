from datetime import datetime
import json
from rose.common import config
import os


class Record:
    def __init__(self, seed, high_score, driver_name):
        self.seed = seed
        self.high_score = high_score
        self.driver_name = driver_name


class Database:
    def __init__(self):
        self.records = {}

    def load(self, filename):
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("{}")

        # load records from json file
        with open(filename, "r") as f:
            self.records = json.load(f)

    def save(self, filename):
        # save records to json file
        with open(filename, "w") as f:
            json.dump(self.records, f)