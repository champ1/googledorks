from output_base import OutputBase

class Dumper(OutputBase):
    def __init__(self, args):
        self.args = args

    def set(self, data):
            self.data = data

    def save(self):
            print self.data


