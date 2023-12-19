** How to run xstrategy ** 
Run xstrategy as an executable (`./xstrategy` in linux).
The program will expect input from standard in. It will take two lines of input (One line for the JStrategy, and another line for the JPub).
After consuming the input, the program will print out a JAction that will state the turn that should be made based on the strategy and the state of the board.
The provided tests are in `./Tests`.
To run a test, you can run the line `./xstrategy < Tests/n-in.json | diff Tests/n-out.json -`.
This will check for differences between the output of the xstrategy program, and the associated output json file. Ensure that the `n` used for the input and output is the same.