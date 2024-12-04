import os
import pprint
import unittest

from main import OilSurvey

SURVEY_DIR = os.path.join(os.path.dirname(__file__), 'surveys')


class TestOilSurveys(unittest.TestCase):
    '''I'm well aware that these are beyond the scope of "Unit Tests"

    I just prefer setting up minimal fixtures with this standard library module. No fancy plugins that break every update.'''

    def _count_deposits(self, survey_filename, expected_count, print_deposits=False):
        survey_filename = os.path.join(SURVEY_DIR, survey_filename)

        with open(survey_filename, 'r') as survey_file:
            raw_survey_data = [line.strip() for line in survey_file]
            survey = OilSurvey(raw_survey_data)
            deposits = survey.getDeposits()

            final_tally = len(deposits)
            print(final_tally)

            if print_deposits:
                #pprint.pprint(deposits)
                print(f'\n> Discovered {final_tally} new deposit(s)! <\n')
                print(survey)

            # Did we accurately detect deposits?
            self.assertEqual(final_tally, expected_count,
                msg=(pprint.pformat(deposits) if print_deposits else None)
            )

    def test_BASIC__empty(self):
        self._count_deposits('empty.txt', 0)

    # I discovered my edges were wrapping seamlessly!
    #
    # Over a few square miles,
    # these deposits will not extend around the globe
    def test_BASIC__flat_earth(self):
        self._count_deposits('flat_earth.txt', 8)

    def test_BASIC__original(self):
        self._count_deposits('original.txt', 4)

    def test_BASIC__simple_u_shape(self):
        self._count_deposits('simple_u_shape.txt', 1)

    def test_BASIC__simple_x_shape(self):
        self._count_deposits('simple_x_shape.txt', 1)

    def test_BASIC__wicked_four_dragons(self):
        self._count_deposits('wicked_four_dragons.txt', 4)


    ### Randomized noise tests:

    def test_RANDOM__01_sixteenth(self):
        self._count_deposits('random/1-of-16.txt', 196)

    def test_RANDOM__02_sixteenths(self):
        self._count_deposits('random/2-of-16.txt', 296)

    def test_RANDOM__04_sixteenths(self):
        self._count_deposits('random/4-of-16.txt', 282)

    def test_RANDOM__05_sixteenths(self):
        self._count_deposits('random/5-of-16.txt', 176)

    def test_RANDOM__06_sixteenths(self):
        self._count_deposits('random/6-of-16.txt', 115, print_deposits=True)

    def test_RANDOM__08_sixteenths(self):
        self._count_deposits('random/8-of-16.txt', 20)

    def test_RANDOM__10_sixteenths(self):
        self._count_deposits('random/10-of-16.txt', 4)

    def test_RANDOM__14_sixteenths(self):
        self._count_deposits('random/14-of-16.txt', 2)
   

    ### Larger tests for studying bottlenecks
    # TODO: add many more

    def test_LARGER_256_small_islands(self):
        self._count_deposits('larger/256-small-islands.txt', 256)

    def test_LARGER_256x256_checkerboard(self):
        self._count_deposits('larger/256x256-checkerboard.txt', 1)

    def test_LARGER_543_large_islands(self):
        self._count_deposits('larger/543-large-islands.txt', 543)



def main():
    unittest.main()

if __name__ == '__main__':
    main()