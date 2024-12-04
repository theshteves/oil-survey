'''
Instead of a proper module name,
repl.it prefers "main.py" for the big `Run >` button
'''
import pprint
import sys


class OilSurvey(object):
    '''The'''

    def __init__(self, data):
        '''Create a new OilSurvey object'''
        self.survey = data
        #self.size  = (len(data[0], len(data)) # Will not assume rectangular survey
        self.deposits = []

    def getDeposits(self):
        '''
        Retrieve list of oil deposits, if any,
        including every square mile coordinates

        Returns a List of Sets (Deposit clusters)
            ...consisting of Tuple pairs (x, y):
        [
            { (0, 1), (0, 2), },
            { (3, 3), (4, 3), },
            { (5, 5), },
        ]
        '''
        if not self.deposits:
            self._detectDeposits()

        return self.deposits

    def __str__(self):
        '''Format deposits distinctly for printing
        
        Executes whenever OilSurvey object gets implicitly cast to a string
        '''
        if not self.deposits:
            self._detectDeposits()
        '''Transform deposits back to row format
        (column indices map to ASCII-named deposits)

        [
            {4: 'B', 2: 'B', 3: 'B', 0: 'D'}, # Line 1
            {3: 'B', 4: 'B'},                 # Line 2
            {4: 'B', 1: 'C'},                 # Line 3
            {4: 'B'},                         # Line 4
            {0: 'A', 1: 'A'},                 # Line 5
        ]
        '''
        output_rows = [{} for _ in range(len(self.survey))]
        for i, deposit in enumerate(
                reversed(self.deposits)
        ):  # reversed() produces a more intuitive ASCII ordering (since deposits were ordered by last edited)
            symbol = chr(65 + (i % 62))  # Cycle through 62 ASCII characters

            for x, y in deposit:
                output_rows[y][x] = symbol

        output = []
        for row in output_rows:
            output_row = ' ' * max(row)

            for x, symbol in row.items():
                output_row = output_row[:x] + symbol + output_row[x + 1:]
            output.append(output_row)

        return '\n'.join(output)

    def _isOilUnderTile(self, tile):
        '''Verify if tile has any oil'''
        x, y = tile
        return self.survey[y][x] == 'X'

    def _isTileInAnotherDeposit(self, tile):
        '''Verify if tile is already in another deposit'''
        return any(tile in deposit for deposit in self.deposits)
        #TODO: Optimze via caching all tiles in a single Set for O(1) lookups

    def _popTileDeposit(self, tile):
        '''Detach tile's deposit from the record, if any, for modication '''

        deposit_id = None
        for i, deposit in enumerate(self.deposits):
            if tile in deposit:
                deposit_id = i
                break

        else:  # Python's unique "for-else" loop
            return set()

        return self.deposits.pop(deposit_id)

    def _detectDeposits(self):
        '''
        Process all survey data for clusters
        & cache the results in self.deposits

        NOTE: this first, naive implementation is solely optimized for correctness. From here, I can quickly generate more test cases. From there, I can explore & prioritize which performance bottlenecks deserve further optimization (which will look very different depending on how much time & funding we have access to, not to mention compute resources).
        
        ...runtime speed & memory usage might not even be the dimensions we're optimising for ;) (I can think of at least 8)
        '''

        adjacent_tiles = [
            # NOTE: After getting to a "correct" solution, I just noticed that these are entirely redundant [given the naive, good-enough, single-threaded, sequential algorithm]!
            #(-1,-1), (0,-1), (1,-1),
            #(-1, 0),         (1, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]

        for y, row in enumerate(self.survey):
            for x, tileType in enumerate(row):
                tile = (x, y)

                if tileType != 'X':
                    continue  # No oil here. Next.

                # Scan neighbors for potential deposit extensions
                deposit = self._popTileDeposit(tile) or {tile}
                #print(f'[{x}, {y}] {tile} in {deposit}')

                for x_delta, y_delta in adjacent_tiles:
                    neighbor = (x + x_delta, y + y_delta)

                    try:
                        if all(coordinate >= 0 for coordinate in neighbor):

                            # Did we find more oil?
                            if self._isOilUnderTile(neighbor):

                                if not self._isTileInAnotherDeposit(neighbor):
                                    deposit.add(neighbor)

                                else:
                                    # Merge connected deposits
                                    connected_deposit = self._popTileDeposit(
                                        neighbor)
                                    deposit.update(connected_deposit)
                                    #print(f'{tile} + {neighbor}\n\n{deposit}\n:\n{connected_deposit}\n\n')

                    except IndexError as e:
                        continue

                # Overwrite deposit based on scan
                self.deposits.insert(0, deposit)
                # NOTE: insert at the beginning so that
                # self.deposits becomes a Least-Recently-Used Cache
                #
                # ...which speeds up _popTileDeposit() in most cases
                # by assuming that neighbors with oil are more likely
                # to be in the most recently seen deposits

                #TODO: potential optimization: appending is MUCH faster for lists
                # ...consider collections.deque if you need lots of 0-inserts
                # ...or just refactoring _popTileDeposit() w/ the reversed() generator

# Only execute when called directly
# (not when imported by other modules)
if __name__ == '__main__':
    #raw_survey_data = [line.strip() for line in sys.stdin]
    raw_survey_data = [
        'X.XXX',
        '...XX',
        '.X.XX',
        '....X',
        'XX...',
    ]
    print('\n'.join(raw_survey_data))

    survey = OilSurvey(raw_survey_data)
    deposits = survey.getDeposits()

    print(f'\n> Discovered {len(deposits)} new deposit(s)! <\n')
    print(survey)
    #pprint.pprint(deposits) # Format nested data extra-nicely with PrettyPrinter
    print(
        '\n\tNOTE: You can view the other test scenarios in the `Code` tab\n')

    # Goofy Makefile workaround for repl.it
    import tests, unittest
    suite = unittest.TestLoader().loadTestsFromModule(tests)
    unittest.TextTestRunner(verbosity=3).run(suite)
