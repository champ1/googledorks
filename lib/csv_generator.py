import csv
from output_base import OutputBase

class Csv(OutputBase):
    def __init__(self, args):
        self.args = args

    def set(self, data):
        self.data = data

    def save(self):
        with open('google_dorks.csv', 'w+') as csvfile:
            fieldnames = ['id', 'title', 'dork', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            [ writer.writerow(row) for row in self.data ]


