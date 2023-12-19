Pair: mysterious-mongooses \
Commit: [0fc5598554b15796120d921652fe5e8417264674](https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/tree/0fc5598554b15796120d921652fe5e8417264674) \
Self-eval: https://github.khoury.northeastern.edu/CS4500-F23/mysterious-mongooses/blob/7f5ba0fd2e698b6f1af25be56acd63e386d75298/5/self-5.md \
Score: 65/ 125\
Grader: Jessica Su

30/85: Programming Task: \
-5: Purpose statements for dag and ldasg should specify what each strategy is for a newcomer to the codebase.\
-15: No unit tests for both strategies\
-15: No unit tests for strategy iterator\
-20: There should be a strategy interface because there are two concrete varients (ldasg and dag which have functions with the same signature.) `ldasg` and `dag` have repeated code that should be abstracted out into a helper function (finding the smallest tile out of the player's smallest tiles), etc\

35/40 Design Task: \
Take turn should not be a function in the referee. Take turn should be a function in the player interface as https://course.khoury.northeastern.edu/cs4500f23/local_protocol.html denotes.

-5: No functionality in game state to check whether the game is over
