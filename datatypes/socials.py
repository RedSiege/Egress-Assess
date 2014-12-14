'''

This module generates social security numbers

'''

from common.lib import helpers


class Datatype:

    def __init__(self, total_data):
        self.datatype = "social security numbers"
        self.filetype = "text"
        self.datasize = total_data

    def create_ssn(self):
        ssn = helpers.randomNumbers(9)
        ssn = ssn[0:3] + "-" + ssn[3:5] + "-" + ssn[5:9]
        return ssn

    def generate_data(self):
        ssns = ''
        # This is approx 1 meg of socials
        for single_ssn in range(0, 81500 * self.datasize):
            ssns += self.create_ssn() + ', '
        return ssns
