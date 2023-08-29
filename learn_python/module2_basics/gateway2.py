"""
Gateway Assignment 2

This assignment is designed to exercise your knowledge of the basics of
Python covered in the module 2 lesson. Take your time and if you get
frustrated ask for help! Some of these tasks can be tricky and some of
the later ones especially are designed to challenge your handle of 
looping, conditionals and sequence indexing. This is the hard part, but
it is the gateway to the fun part! If you get intimidated looking at 
a large block of hard to understand code, take a breath and focus on
each line one by one. 

To run these tests from the command line:

    poetry run pytest -k test_gateway2

The tests will run for each task as you attempt to do the task - if no
implementation is found the test will be skipped. Once you have completed
the gateway assignment you should see that all tests pass with no skipped
tests!

Remember, if you want to run one of your functions outside of the pytest
environment you can do so like this:

    poetry run ipython
    >> from learn_python.module2.gateway2 import my_function
    >> my_function()

print statements can be useful for debugging!
"""


# TODO Task 1
# Write a function called "is_even" that accepts an integer as an 
# argument and returns True if the integer is even and False if it is not.
#   - hint use modulus operator %
def is_even(x):
    return x % 2 == 0


# TODO Task 2
# Write a function called "is_odd" that returns True if an integer is odd
# and False if it is not. You must use the is_even function you wrote above
# to implement this function. Why do it this way? Because it is more DRY
# (Dont Repeat Yourself) - If we know our is_even function works lets use
# it! Our code will be cleaner and less buggy the more of it we can reuse.
def is_odd(x):
    return not is_even(x)


# TODO Task 3
# Because None is a special value in Python that is commonly used to 
# represent uninitialized variables, it is sometimes a good idea to
# check if a variable is None before using it. Implement a function 
# called is_even_safe that works exactly like is_even but that checks
# if the value is None first and if it is returns None
def is_even_safe(x):
    if x is not None:
        return is_even(x)
    return None


# TODO Task 4
# Re-implement is_even_safe in a function called is_even_safe_ternary
# that uses a ternary expression to accomplish the same thing in a single
# statement
def is_even_safe_ternary(x):
    """
    Return True if x is even, False if it is odd and None if it is None.
    """
    return is_even(x) if x is not None else None


# TODO Task 5
# Implement a function called logic_play that accepts two integers as
# arguments and returns their product (the result of multiplying them together)
# if both are even, their quotient (the result of dividing the first by the
# second) if both are odd, and None otherwise. You must use "and" in your
# implementation of this function. You may assume all inputs will be integers.
def logic_play(first, second):
    if is_even(first) and is_even(second):
        return first * second
    elif is_odd(first) and is_odd(second):
        return first / second
    return None


# TODO Task 6
# Reimplement logic_play and call it logic_play2. This time you cannot
# use any logical operators (and, or, not) and you may make a maximum
# of three function calls. Your implementation should not exceed 5 
# statements.
def logic_play2(first, second):
    if is_even(first):
        if is_even(second):
            return first * second
    elif is_odd(second):
        return first / second
    

# Which version of logic_play is more clear? Which is more efficient?
# Which is more readable? Which is more maintainable?
#   Cleverness is not always a virtue in programming and there are
#   always tradeoffs!


# TODO Task 7
# Define a function called default_args that accepts 4 arguments, each 
# with a default value of your choosing. The function must return 4
# True/False values, one for each argument, where the value is True
# if the argument passed in was equal to the default value and False
# otherwise.
def default_args(w=0, x=1.0, y='2', z=None):
    return w == 0, x == 1.0, y == '2', z is None


# TODO Task 8
# Define a function called is_close that takes two floats as arguments
# and a third argument that is a tolerance. The function should return
# True if the difference between the two floats is less than the tolerance
# and False otherwise. You should provide a default tolerance of 1e-9.
# You may not call math.isclose()
#  hint: checkout the python built-in function abs()
def is_close(x, y, tol=1e-9):
    return abs(x - y) < tol


# TODO Task 9 - implement this function
def normal_distribution(x, σ=1, μ=0):  # did you know python code is unicode by default? 🤯
    """
    Compute the value of the normal distribution at x given σ and μ.

    See ./resources/normal_distrib.png for the definition of the normal
    distribution.

    Hint: you will need to import three things from math
    Hint: its possible to write this in a single line (not including the imports)

    .. note:
        The test for this task will display a plot of your normal distribution,
        if your VSCode is full-screened, the plot may be hidden behind it. If
        your test is failing the plot will remain open and the other tests will
        not proceed until you have a chance to examine the plot to see what is
        incorrect about your implementation. If your implementation is correct
        the plot will show for 5 seconds and then the remaining tests will proceed.

    :param x: float - the value to compute the normal distribution at
    :param σ: float - the standard deviation of the normal distribution, larger
        values of σ result in a wider distribution, default: 1
    :param μ: float - the mean of the normal distribution (x = μ is the peak 
        of the distribution), default: 0
    """
    #from math import pi, sqrt, exp
    #return 1 / (σ * sqrt(2 * pi)) * exp(-0.5 * ((x - μ) / σ) ** 2)


# TODO Task 9
# Define a function called divide that takes two arguments and returns
# the result of dividing the first by the second using floor division
# if both arguments are integers and regular division otherwise.
# If the second argument is zero, return None
def divide(x, y):
    if y == 0:
        return None
    if type(x) is int and type(y) is int:
        return x // y
    return x / y


# TODO Task 10
# Implement a function called get_decimal that takes a float or an
# integer as an argument and returns decimal portion of the number. 
# For example:
#   get_decimal(3.14159) == 0.14159
#   get_decimal(2.71828) == 0.71828
#   get_decimal(-1.1) == -0.1
#   get_decimal(0) == 0.0
#   get_decimal(5) == 0.0
# Your implementation must be a single statement. The return value
# must be a float even when an integer is passed in.
# Hint: use type coercion
def get_decimal(x):
    return float(x) - int(x)


def float_range(start, stop, step):
    """
    Python's built-in range() function only works with integers. Implement
    a function called float_range that works similar to range() but with 
    floats. Your implementation must work with positive and negative floats.
    You may assume that the step argument will never be zero. If stop is
    < start the range should be in decreasing order.

    For example:

        float_range(0, 1, 0.1)           ==  [0, 0.1, 0.2, ..., 0.9, 1]
        float_range(0, -1, -0.1)         ==  [0, -0.1, -0.2, ..., -0.9, -1]
        float_range(0, -1.01, -0.1)      ==  [0, -0.1, -0.2, ..., -0.9, -1]
        float_range(0, -1, 0.1)          ==  float_range(0, -1, -0.1)
        float_range(3, 2, -0.5)          ==  [3, 2.5, 2]
        float_range(1e-12, 2e-12, 2e-13) ==  [1e-12, 1.2e-12, 1.4e-12, 1.6e-12, 1.8e-12, 2e-12]
        float_range(0.099, 0.297, 0.099) == [0.099, 0.198, 0.297] 😈

    :param start: float - the starting value
    :param stop: float - the ending value (inclusive! - does not include the stop value)
        note, range() is exclusive of the stop value, but float_range() is inclusive
    :param step: float - the spacing between values. This value is insensitive to its
        sign
        
    hint: use built-in abs() and determine directionality from start's relationship to stop
    hint: floating point precision error might cause your loop to terminate early unless
        you account for it by comparing to a tolerance - BUT you do not know how small
        the step size will be so you cannot use a fixed tolerance - your tolerance must be
        relative to the step size. For example, if the step size is 1e-12, a tolerance of 1e-9
        is too large and will either cause the loop to terminate early or blow up the size of
        the list depending on your implementation.
    """
    step = abs(step) * (-1 if start > stop else 1)
    stop = stop + step/2
    rng = []
    # we use step/2 to account for floating point precision error, using any value less than
    # the step size will always work
    while (step > 0 and start < stop) or (step < 0 and start > stop):
        rng.append(start)
        start += step
    return rng


# TODO Task 11
def xy_values(pdf, start, stop, step=1e-2):
    """
    Return a list of 2 element tuples (2-tuples) where the first element is the
    x-value and the second element is the y-value of the given probability density
    function (pdf) evaluated at the corresponding x-value. The x-values should
    begin at start and end at stop, with each subsequent value being incremented
    by step.

    For example:

        from functools import partial
        get_distribution(
            normal_distribution,
            -5,
            5,
            1e-2
        ) == [(-5, ), (-4.99, ), (-4.98, ), ..., (4.98, ), (4.99, ), (5, )]

    :param pdf: function - a probability density function that takes a single 
        float argument (x-value) and returns a float (y-value)
    :param start: float - the starting value for x
    :param stop: float - the ending value for x
    :param step: float - the spacing between x values
    :return list of tuples - the (x, y) values of the distribution

    requirement: You must use your float_range function!
    """
    return [(x, pdf(x)) for x in float_range(start, stop, step)]


# TODO Task 12
def separate(list_of_2_tuples):
    """
    Given a list containing tuples of length 2 (2-tuples), return two
    lists where the first list contains the first tuple elements and the
    second list contains the second tuple elements.

    For example:

        separate([(1, 2), (3, 4)]) == [1, 3], [2, 4]

    :param list_of_2_tuples: list of tuples - the list of 2-tuples to expand
    """
    x, y = [], []
    for tpl in list_of_2_tuples:
        x.append(tpl[0])
        y.append(tpl[1])
    return x, y


def combine(list1, list2):
    """
    Return a single list containing 2-tuples where the i-th element of list1 is
    the first tuple element and the i-th element of list2 is the second tuple
    element. This can be thought of as the inverse of separate().

    :param list1: list - the first list
    :param list2: list - the second list
    :return list of tuples - the combined list of tuples

    hint: checkout the built-in function zip()
    """
    return list(zip(list1, list2))


def approximate_integral(curve):
    """
    Use Simpson's rule to approximate the area under the given curve.

    Simpson's rule uses parabolas to approximate the curve between points:

    ∫f(x)dx = (xₙ - x₀)/(3n) * (f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ))

    Simpson's rule requires that len(curve) be even - assert that len(curve) is even
    and non-zero.

    :param curve: list - a list of 2-tuple xy-values representing a curve
    :return float: - the area under the curve as computed by simpson's rule

    hint: use the built-in function sum() with even/odd list slices, and dont forget
        about the x/y tuple indexing!
    """
    assert len(curve) and len(curve) % 2 == 0, 'The length of curve must be even!'
    return (curve[-1][0] - curve[0][0]) / (3*len(curve)) * (
        curve[0][1] + 
        curve[-1][1] + 
        4 * sum([xy[1] for xy in curve[1:-1:2]]) +
        2 * sum([xy[1] for xy in curve[2:-1:2]])
    )


# TODO Task 12
def decimate(vector, factor=10):
    """
    Return a new list reduced in size by the given factor. The elements 
    of the decimated list should be evenly spaced elements of the given list.
    The first element of the returned list should always be the first element 
    of the given list. The size reduction should round up to the nearest whole
    number.

    For example:

        my_list = [1, 2, 3, 4, 5, 6]
        decimate(my_list, 2) == [1, 3, 5]  # 6/2 = 3
        decimate(my_list, 3) == [1, 4]     # 6/3 = 2
        decimate(my_list, 4) == [1, 5]     # 6/4 = 1.5 -> 2
        decimate(my_list)    == [1]        # 6/10 = 0.6 -> 1

    :param vector: list - the list to decimate
    :param factor: int - the factor to reduce the size of the list by

    hint: this is doable in one statement with slicing
    """
    return vector[::factor]


# TODO Task 13
def deduplicate(sequence, preserve_order=False):
    """
    Remove any duplicate elements from the given sequence.

    .. warning::
        The order of the original sequence is not guaranteed to be preserved!

    :param sequence: list - the sequence to remove duplicates from
    :param preserve_order: bool - if True, the order of the original sequence
        will be preserved, if False the order of the original sequence is not
    :return list - the list with duplicates removed

    requirement: implementation must be a single statement

    hint: use set() and type coercion
    hint: the order of a set() is undefined
    hint: checkout built-in sorted() and list.index()
    hint: you will need a ternary if-else expression
    """
    return (
        sorted(list(set(sequence)), key=sequence.index)
        if preserve_order else
        list(set(sequence))
    )


def list_intersection(list1, list2):
    """
    Return elements that are in both of the given lists.

    :param list1: list - the first list
    :param list2: list - the second list
    :return list - the elements that are in both lists

    requirement: use set() and type coercion to accomplish this in one statement
    """
    return list(set(list1) & set(list2))


def list_difference(list1, list2):
    """
    Return elements that are in the first list but not the second list.

    :param list1: list - the first list
    :param list2: list - the second list
    :return list - the elements that are in the first list but not the second

    requirement: use set() and type coercion to accomplish this in one statement
    """
    return list(set(list1) - set(list2))


def list_symmetric_difference(list1, list2):
    """
    Return elements that are in either of the given lists but not both.

    :param list1: list - the first list
    :param list2: list - the second list
    :return list - the elements that are in either list but not both

    requirement: use set() and type coercion to accomplish this in one statement
    """
    return list(set(list1) ^ set(list2))


def list_union(list1, list2):
    """
    Return elements that are in either of the given lists.

    :param list1: list - the first list
    :param list2: list - the second list
    :return list - the elements that are in either list

    requirement: use set() and type coercion to accomplish this in one statement
    """
    return set(list1 + list2)


# TODO Task XX
def are_same_object(object1, object2):
    """
    Returns True if object1 and object2 are the same object in memory,
    False otherwise.
    """
    return object1 is object2


def fibonacci(length):
    """
    Return a list of the first fibonacci numbers that is length long.

    :param length: int - the number of fibonacci numbers to return
    :return list - the first fibonacci numbers

    requirement: use a while loop
    """
    fib = [0, 1]
    while len(fib) < length:
        fib.append(fib[-1] + fib[-2])
    return fib[:length]


GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def fibonacci_gr(golden_ratio_tol):
    """
    In the limit as n approaches infinity, the ratio of the n+1 fibonacci number
    to the n fibonacci number approaches the golden ratio. This function uses
    a ratio tolerance instead of a length parameter to determine the length of
    the fibonacci sequence to generate.

    :param golden_ratio_tol: float - the tolerance to use to determine the length
        of the fibonacci sequence to generate - stop generating when we are within
        abs(golden_ratio_tol) of the GOLDEN_RATIO (1.61803398875...)
    :return list - the fibonacci sequence

    requirement: use break to exit the loop
    """
    fib = [0, 1]
    while True:
        fib.append(fib[-1] + fib[-2])
        if abs(fib[-1] / fib[-2] - GOLDEN_RATIO) < abs(golden_ratio_tol):
            break
    return fib


# TODO Task XX
def identity_matrix(size):
    """
    Return the identity matrix of size=n (i.e. n x n):

        0  1  2  ...  n
    0 [[1, 0, 0, ..., 0],
    1  [0, 1, 0, ..., 0],
    2  [0, 0, 1, ..., 0],
       ...
    n  [0, 0, 0, ..., 1]]

    An identity matrix is a square matrix with 1s on the main diagonal and 0s
    everywhere else.

    :param size: int - the number of rows and columns
    :return list of lists - the identity matrix of dimensions size x size
        if size is 0, return an empty list, if size is < 0 return None
    """
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    
    if size < 0:
        return None
    return matrix


# TODO Task XX
def identity_matrix_comprehension(size):
    """
    Same output as identity_matrix but this function should be implemented 
    using a single statement - and you can't call identity_matrix()!
    (hint: use a nested list comprehension combined with a ternary if-else expression)

    :param n: int - the size of the identity matrix
    """
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)] if size >= 0 else None


# TODO Task XX
def is_identity(matrix):
    """
    Check if the given matrix is an identity matrix.

    :param matrix: list of lists - the matrix to check
    :return bool - True if matrix is an identity matrix, False otherwise
        if matrix is None or an empty list, return False
    """
    if not matrix:
        return False
    size = len(matrix)
    for row_idx, row in enumerate(matrix):
        if not isinstance(row, (tuple, list)):
            return False
        if len(row) != size:
            return False
        for col_idx, value in enumerate(row):
            if row_idx == col_idx:
                if value != 1:
                    return False
            elif value != 0:
                return False
    return True


# Test Election Scenario
ELECTION_CANDIDATES = {
    0: 'Ada Lovelace',
    1: 'Grace Hopper',
    2: 'Annie Easley',
    3: 'Katherine Johnson'
}
ELECTION_BALLOTS = [
    *([[0, 2, 3]] * 6),  # 6 ballots look like [Ada, Annie, Katherine]
    *([[1, 3, 2]] * 4),  # 4 ballots look like [Grace, Katherine, Annie]
    *([[2, 0, 1, 3]] * 2),
    *([[2, 3]] * 2),
    *([[2, 1]] * 1),
    *([[3, 1, 0, 2]] * 2),
    [3]  # one ballot just picked Katherine!
]

def ranked_choice(candidates, ballots):
    """
    Determine the winner of ranked choice election given a list of ballots
    cast by voters and a mapping of candidate ids to names. Each ballot is
    an ordered list of candidate choices where the first element is the voter's
    first candidate choice. Return a dictionary of information about the
    rounds.

    How RCV works (per https://www.rcvresources.org/faq):
        
        All first choices are counted. When electing a single candidate, if a 
        candidate receives more than half of the first choices, that candidate 
        wins, just like in any other election. However, if there is no majority
        winner after counting the first choices, the race is decided by an 
        instant runoff. The candidate with the fewest first-choice votes is 
        eliminated from all ballots, and the talley starts over. This process
        continues until someone emerges with a majority.

    * You may assume there will be no ties
    * You may assume there will be no empty ballots
    * You may assume all ballots will have at least one choice
    * You may not assume all ballots will make the same number of choices
    * You can add extra information to the report dictionary if you want

    :param candidates: dict - a mapping of candidate ids to names
        (e.g) {0: 'Obama', 1: 'Romney'}
    :param ballots: list of lists - a list of ballots cast by voters where
        each ballot is an ordered list of candidate choices. For example:
        ballots = [
            [0, 1],
            [1, 0],
            [0]
        ]
        means that the first voter voted for Obama first and Romney second
        and the second voter voted for Romney first and Obama second. You can
        assume no empty ballots will be cast.

    :return report: dict - a dictionary report containing information about the
        RCV results and rounds. It should have the following structure:

        .. code-block:: python

            report = {
                'rounds': [  # ordered list - first round first, last round last
                    {
                        'votes': int,  # the total number of votes cast in this round
                        # ordered - first place first, last place last
                        # (name, number of votes)
                        # if a candidate has been eliminated from a round, 
                        # they should not appear here
                        'ranking': [
                            ('Candidate Name', int),
                        ]
                    }
                ],
                'winner': 'Candidate Name'  # the name of the winning candidate
            }

    hint: break your code into smaller functions. You might have one function called determine_ranking
        that takes a list of ballots and returns a list of tuples where the first element is the candidate
        id and the second element is the number of votes that candidate received in the round. You might 
        have another function called eliminate_candidate that takes a list of ballots and removes all votes
        for the given candidate id - thus returning the cleaned ballots for the next round.

        Using these functions from within a while loop will make what the while loop is doing more clear!
    """
    report = {
        'rounds': [],
        'winner': None
    }
    name_to_id = {name: id for id, name in candidates.items()}

    def determine_ranking(round):
        """
        Determine the ranking of candidates for the given round of voting.
        """
        candidate_votes = {id: 0 for id in candidates.keys()}
        for ballot in round:
            candidate_votes[ballot[0]] += 1
        
        return [
            (candidates[candidate], votes)
            for candidate, votes in sorted(
                candidate_votes.items(),
                key=lambda candidate: candidate[1],
                reverse=True
            )
            if votes > 0
        ]
    
    def eliminate_candidate(round, eliminated_candidate):
        """
        Eliminate the given candidate from the given round of voting. Spent (empty) ballots
        will also be discarded.
        """
        return [
            ballot for ballot in [
                [
                    candidate
                    for candidate in ballot
                    if candidate != eliminated_candidate
                ]
                for ballot in round
            ] if ballot
        ]

    rounds = [ballots]
    
    report['rounds'].append({
        'votes': len(ballots),
        'ranking': determine_ranking(ballots)
    })

    while report['rounds'][-1]['ranking'][0][1] / report['rounds'][-1]['votes'] < 0.5:
        rounds.append(
            eliminate_candidate(
                # the previous rounds ballots
                rounds[-1],
                # the last place candidate id from the last round
                name_to_id[report['rounds'][-1]['ranking'][-1][0]]
            )
        )
        report['rounds'].append({
            'votes': len(rounds[-1]),
            'ranking': determine_ranking(rounds[-1]),
        })

    report['winner'] = report['rounds'][-1]['ranking'][0][0]
    return report


# from pprint import pprint
# pprint(ranked_choice(ELECTION_CANDIDATES, ELECTION_BALLOTS))


def print_report(report):
    """
    Print a human readable report of the ranked_choice report dictionary to the terminal.

    The output for the test scenario should look like this:

    --------------------------------
    Round 0
           Ada Lovelace:  6 (33.33%)
           Annie Easley:  5 (27.78%)
           Grace Hopper:  4 (22.22%)
      Katherine Johnson:  3 (16.67%)
    --------------------------------
    Round 1
           Ada Lovelace:  6 (35.29%)
           Grace Hopper:  6 (35.29%)
           Annie Easley:  5 (29.41%)
    --------------------------------
    Round 2 (Winner: Ada Lovelace)
           Ada Lovelace:  8 (53.33%)
           Grace Hopper:  7 (46.67%)

    The rounds should be separated by 32 dashes. Each round should be labeled with the
    round number and the last round should have (Winner: <name>) appended to the label.
    Each candidates participating in a round should appear in vote count order with the
    number of votes they received and the percentage of votes they received in parentheses.

    The format of the candidate lines should be:

    <indent><name padding><candidate name>:<vote padding><votes> (<percent>%)

    where
        - indent is 2-spaces
        - name padding is the number of spaces required to make all candidate names 
          line up (i.e. for each candidate it is the length of the longest 
          candidate name minus the length of their name)
        - vote padding is the number of spaces required to make all vote counts line
          up (use the length of the total number of votes expressed as a string as
          the padding length)

    :param report: dict - the report dictionary returned by ranked_choice
    :param candidates: dict - a mapping of candidate ids to names
    """

    # we can assume the first round has all candidates and the most votes
    max_name_length = max(len(candidate[0]) for candidate in report['rounds'][0]['ranking'])
    max_votes = len(str(report['rounds'][0]['votes']))
    for number, round in enumerate(report['rounds']):
        print('-' * 32)
        if number == len(report['rounds']) - 1:
            print(f'Round {number} (Winner: {report["winner"]})')
        else:
            print(f'Round {number}')
        for candidate, votes in round['ranking']:
            print(f'  {candidate:>{max_name_length}}: {votes:>{max_votes}} ({votes/round["votes"]:.2%})')
