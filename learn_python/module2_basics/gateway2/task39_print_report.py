"""
.. todo::
    Implement print_report() according to its docstring.

    The output for the test scenario should look like this::

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
"""

def print_report(report):
    """
    Print a human readable report of the ranked_choice report dictionary to the terminal.

    The are separated by 32 dashes. Each round is labeled with the round number and the last 
    round will have (Winner: <name>) appended to the label. Each candidate participating in a 
    appears in vote count order with the number of votes they received and the percentage of 
    votes they received in parentheses.

    The format of the candidate lines is:

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
