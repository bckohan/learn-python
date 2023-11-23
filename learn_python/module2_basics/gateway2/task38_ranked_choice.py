"""
.. todo::
    It's finally time to make something useful! Implement ranked_choice() according to 
    its docstring.

    * You may assume there will be no ties
    * You may assume there will be no empty ballots
    * You may assume all ballots will have at least one choice
    * You may not assume all ballots will make the same number of choices
    * You can add extra information to the report dictionary if you want

    
.. hint::
    Break your code into smaller functions. You might have one function called 
    determine_ranking that takes a list of ballots and returns a list of tuples 
    where the first element is the candidate id and the second element is the number
    of votes that candidate received in the round. You might have another function 
    called eliminate_candidate that takes a list of ballots and removes all votes
    for the given candidate id - thus returning the cleaned ballots for the next round.

    Using these functions from within a while loop will make what the while loop is 
    doing more clear!
"""

# Test Election Scenario
ELECTION_CANDIDATES = {
    0: 'Ada Lovelace',
    1: 'Grace Hopper',
    2: 'Annie Easley',
    3: 'Katherine Johnson'
}

# unpacking makes the specification of our test ballots very compact!
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
    winner and rounds.

    How RCV works (per https://www.rcvresources.org/faq):
        
        All first choices are counted. When electing a single candidate, if a 
        candidate receives more than half of the first choices, that candidate 
        wins, just like in any other election. However, if there is no majority
        winner after counting the first choices, the race is decided by an 
        instant runoff. The candidate with the fewest first-choice votes is 
        eliminated from all ballots, and the talley starts over. This process
        continues until someone emerges with a majority.

    :param candidates: dict - a mapping of candidate ids to names
        (e.g) {0: 'Obama', 1: 'Romney'}
    :param ballots: a list of ballots cast by voters where each ballot is an 
        ordered list of candidate choices. For example:

        .. code-block:: python

            ballots = [
                [0, 1],
                [1, 0],
                [0]
            ]
        
        The above ballot list shows that the first voter voted for Obama first 
        and Romney second and the second voter voted for Romney first and Obama 
        second. You can assume no empty ballots will be cast.

    :return: a dictionary report containing information about the
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
    """
