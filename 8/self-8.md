The commit we tagged for your submission is 343fdbabe624857f2823f3bafd8148488f65738b.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/tree/343fdbabe624857f2823f3bafd8148488f65738b

## Self-Evaluation Form for Milestone 8

Indicate below each bullet which file/unit takes care of each task:

- concerning the modifications to the referee: 

  - is the referee programmed to the observer's interface
    or is it hardwired?

    https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/343fdbabe624857f2823f3bafd8148488f65738b/Q/Referee/referee.py#L45-L57

    it is hardwired into the referee

  - if an observer is desired, is every state per player turn sent to
    the observer? Where? 

    https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/343fdbabe624857f2823f3bafd8148488f65738b/Q/Referee/referee.py#L201-L221

  - if an observer is not desired, how does the referee avoid calls to
    the observer?

    https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/343fdbabe624857f2823f3bafd8148488f65738b/Q/Referee/referee.py#L50-L57

    display_observer=False means that the observer will not be displayed

- concerning the implementation of the observer:

  - does the purpose statement explain how to program to the
    observer's interface? 

observer purpose statment
#         ___  _                                  
#        / _ \| |__  ___  ___ _ ____   _____ _ __ 
#       | | | | '_ \/ __|/ _ \ '__\ \ / / _ \ '__|
#       | |_| | |_) \__ \  __/ |   \ V /  __/ |   
#        \___/|_.__/|___/\___|_|    \_/ \___|_|   
#
# The Observer class contains states of games. The referee updates the observer
# with a new state after each players turn. 
# 
# - saves states it recieves from referee as pdfs
# - displays the states in a gui 
#   - user can select next and previous from the current state
#   - user can save the state as a json

  - does the purpose statement explain how a user would use the
    observer's view? Or is it explained elsewhere? 

  yes it is explained in the purpose statement
  
The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

