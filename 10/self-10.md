The commit we tagged for your submission is b4537f7210d21bb07db4d07e6aaf8705e6eb8ade.
**If you use GitHub permalinks, they must refer to this commit or your self-eval will be rejected.**
Navigate to the URL below to create permalinks and check that the commit hash in the final permalink URL is correct:

https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/tree/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade

## Self-Evaluation Form for Milestone 10

Indicate below each bullet which file/unit takes care of each task.

The data representation of configurations clearly needs the following
pieces of functionality. Explain how your chosen data representation 

- implements creation within programs _and_ from JSON specs 
Referee from spec
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Server/server.py#L156
Referee regular
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Referee/referee.py#L31 

- enforces that each configuration specifies a fixed set of properties (no more, no less)
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Common/json_io.py#L532-L591

- supports the retrieval of properties 
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Player/player.py#L89

- sets properties (what happens when the property shouldn't exist?) 
Sets properties of refs
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Referee/referee.py#L31

- unit tests for these pieces of functionality
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Server/server_test.py#L15
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Client/client_tests.py#L23

Explain how the server, referee, and scoring functionalities are abstracted
over their respective configurations.
We did not abstract the configuration functinoalities. We added configuration functionality to the existing classes. 

Does the server touch the referee or scoring configuration, other than
passing it on?
Yes, it changes the JState such that the players will also include the proxy players
https://github.khoury.northeastern.edu/CS4500-F23/whimsical-camels/blob/b4537f7210d21bb07db4d07e6aaf8705e6eb8ade/Q/Server/server.py#L155

Does the referee touch the scoring configuration, other than passing
it on?
No

The ideal feedback for each of these three points is a GitHub
perma-link to the range of lines in a specific file or a collection of
files.

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

You may wish to add a sentence that explains how you think the
specified code snippets answer the request.

If you did *not* realize these pieces of functionality, say so.

