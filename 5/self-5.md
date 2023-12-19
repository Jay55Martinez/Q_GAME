The commit we tagged for your submission is 0fc5598554b15796120d921652fe5e8417264674.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/0fc5598554b15796120d921652fe5e8417264674

## Self-Evaluation Form for Milestone 5

Indicate below each bullet which piece of your code takes care of each task:

1. a data definition (inc. interpretation) for the result of a strategy
https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/0fc5598554b15796120d921652fe5e8417264674/Q/Player/strategy.py#L6-L10
2. the `dag` strategy 
https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/0fc5598554b15796120d921652fe5e8417264674/Q/Player/strategy.py#L34-L45
3. the `ldasg` strategy 
https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/0fc5598554b15796120d921652fe5e8417264674/Q/Player/strategy.py#L16-L29
4. a data definition (inc. interpretation) for the result of a strategy iterator
https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/0fc5598554b15796120d921652fe5e8417264674/Q/Player/strategy.py#L47-L50
5. unit tests for the `dag` strategy
   - one for a 'pass' decision
   - one for a 'replace all tiles' decision
   - one for a 'place this tile there' decision
Have not created the unit tests for this method yet
6. unit tests for the `ldaag` strategy
   - one for a 'pass' decision
   - one for a 'replace all tiles' decision
   - one for a 'place this tile there' decision
Have not created the unit tests for this method yet
7. unit tests for the strategy iteration functionality 
   - one for a 'pass' decision
   - one for a 'replace all tiles' decision
   - one for a _sequence of_ 'place this tile there' decision
Have not created the unit tests for this method yet
8. how does your design abstract the common strategy iteration functionality 
We use method that takes in an object function either dag or ldaag and runs the iteration using that.
https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/0fc5598554b15796120d921652fe5e8417264674/Q/Player/strategy.py#L51-L70
9. does your design abstract the common search through the sorted tiles?
   (for a bonus)
Our code does not
The ideal feedback for each of these points is a GitHub perma-link to
the range of lines in a specific file or a collection of files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.


