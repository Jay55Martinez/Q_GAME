The commit we tagged for your submission is d02a1e1b782a175246232b0ec37adcd2ef9df8e8.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/d02a1e1b782a175246232b0ec37adcd2ef9df8e8

## Self-Evaluation Form for Milestone 7

Indicate below each bullet which file/unit takes care of each task:

The require revision calls for turning Q bonus points and
finished-the-game bonus points into named constants

1. Which unit tests check the Q-bonus functionality? Is it abstracted
   over the named constant? 

https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/d02a1e1b782a175246232b0ec37adcd2ef9df8e8/Q/Common/UnitTests/game_state_test.py#L94-L119

However, this tests is not abstracted and has hardcoded values.

2. Which unit tests check the finished-the-game functionality? Is it
   abstracted over the named constant?

https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/d02a1e1b782a175246232b0ec37adcd2ef9df8e8/Q/Common/UnitTests/game_state_test.py#L94-L119

However, this tests is not abstracted and has hardcoded values.

3. Do you also have integration tests that show how setting the bonus
   constants to different constants yields different results for the
   same starting point? (This is optional but helps with milestone 8
   and fits to the request.) 

No we did not make this test. 

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

