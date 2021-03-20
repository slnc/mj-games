#!/usr/bin/python
'''NPCs (non-player-characters) generator.

1. (Optional) Edit CONFIG block to change the behavior of the script.
2. Run the script ./generate_npcs.py.
'''

import csv
import random

# START CONFIG
_NUM_NPCS = 10  # number of NPCs to generate
_P_FEMALE = 0.5  # probability of the NPC being female
# END CONFIG

# The CSV must have 3 columns called:
# - profession: name of a profession.
# - p_male: probability of this profession being chosen for a male NPC.
#     The sum of all p_male must be exactly 1.
# - p_female: like p_male but for female NPCs.

# TODO: every time a new profession is added or removed the whole table of
# frequencies needs to be updated. An alternative could be to make this column
# represent a factor and choose 1.0 to mean "this profession is as likely as the
# average profession", and that way new professions can be added / removed
# without having to modify the whole frequencies table. The disadvantage is that
# it'sn harder to think in terms of an abstract "average" profession vs thinking
# in terms of population totals.
_PROFESSIONS_CSV = '''profession,p_male,p_female
blacksmith,0.7,0.1
innkeeper,0.2,0.2
cook,0.1,0.7'''

_CSV_P_MALE_COLUMN_NAME = 'p_male'
_CSV_P_FEMALE_COLUMN_NAME = 'p_female'

_MALE = 'male'
_FEMALE = 'female'


def generate_npc():
    gender = generate_gender()
    profession = generate_profession(gender)
    return (gender, profession)


def generate_gender():
    if random.random() < _P_FEMALE:
        return _FEMALE
    else:
        return _MALE


def generate_profession(gender):
    professions = csv.DictReader(_PROFESSIONS_CSV.splitlines())
    # TODO: check that CSV is sane (probability columns add up to 1.0, etc)
    p_threshold = random.random()
    sum_probabilities = 0

    last_profession = None
    for profession in professions:
        sum_probabilities += get_probability(profession, gender)

        if sum_probabilities >= p_threshold:
            return profession['profession']

        last_profession = profession

    return last_profession  # needed to handle float rounding issues


def get_probability(profession, gender):
    '''Returns the probability of a profession given the NPC's gender.'''
    p_column = _CSV_P_MALE_COLUMN_NAME
    if gender == _FEMALE:
        p_column = _CSV_P_FEMALE_COLUMN_NAME

    return float(profession[p_column])


if __name__ == '__main__':
    for _ in range(_NUM_NPCS):
        print('%s %s' % generate_npc())