** How to run xgames **
Run xgames as an executable (`./xgames` in linux)
The program will then take two JSON objects from standard input. It is expecting to load a JState object, followed by a JActors object. The program will then run the game, and print out the list of winning players, and kicked players sorted.
Tests are provided in `./Tests`
In order to compare the output of a test with the expected output, you can run the command `./xgames < Tests/n-in.json | diff Tests/n-out.json -`
If no output is printed, the test succeeded.