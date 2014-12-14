'''

This is for functions potentially used by all modules

'''

import random
import string


def randomNumbers(b):
    """
    Returns a random string/key of "b" characters in length, defaults to 5
    """
    random_number = int(''.join(random.choice(string.digits) for x in range(b))
                        ) + 10000

    if random_number < 100000:
        random_number = random_number + 100000

    return str(random_number)
