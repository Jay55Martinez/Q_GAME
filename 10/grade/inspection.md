Pair: whimsical-camels \
Commit: [b4537f7210d21bb07db4d07e6aaf8705e6eb8ade](https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/tree/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade) \
Self-eval: https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/4dfafb6895440f4692aebc98000285f69fe08c90/10/self-10.md \
Score: 66/110 \
Grader: Vish Jeyaraman


#### [66/110pts] Program Inspection
1. [20/20pts] Helpful and accurate self-eval. 
2. [30/70pts] A well-designed data representation for configurations.
   - [0/10pts] Purpose statement for data representation.
      - Missing purpose statement 
   - [0/10pts] Language internal constructor.
      - Incorrect, Uses a dictionary instead of a class
   - [0/10pts] A separate "builder" that creates the data representation from JSON.
      - Incorrect, Uses a dictionary instead of a class
   - [0/10pts] A way to enforce "key correcteness".
      - Incorrect, Uses a dictionary instead of a class
   - [10/10pts] Method(s) that retrieves the value of entries.
   - [10/10pts] Method(s) that modifies the value of entries.
   - [10/10pts] unit tests.
3. [6/10pts] Server does not touch the referee configuration inside of a server configuration other than passing it on to the referee.
   - Server touch the referee configuration. Partial credit for honesty
4. [10/10pts] Referee does not touch the scoring configuration inside of a referee configuration other than passing it on to the scoring functionality.


