'''

This module generates social security numbers

'''

from common.lib import helpers


class Datatype:

    def __init__(self, total_data):
        self.datatype = "social security numbers"
        self.filetype = "text"
        self.datasize = total_data

    def generate_data(self):
        ssn = helpers.randomNumbers(9)
        ssn = ssn[0:3] + "-" + ssn[3:5] + "-" + ssn[5:9]
        return ssn
