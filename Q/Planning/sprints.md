Memorandum 

TO: 		PROFESSOR FELLEISEN 

FROM:		ETHAN CARPENTER AND MATT STETTER 

DATE:		SEP 14, 2023 

SUBJECT:	PROPOSAL FOR FIRST THREE MILESTONES 

 

For sprint one we estimate it will take about 14 hours. In this time, we hope to implement a player referee interface as a class. We plan on adding to the class a method to set up the initial player state. Then we will add two things, a method so that players can update the referee when they take a turn and a method to insure the validity of the move. Next, we will add a Boolean to determine whether or not the game is finished and getters and setters for it. Then, we will add a method to know when players have joined/left the game. Finally, we will add a method so that the referee can update the players on the changes to the game. 

 

For sprint two we believe it is completable in 12 hours. First, we will create a class for the game state. This class has functionality to determine whether two tiles are connected. It will have a method to receive updates from the referee and a method to view the game. Then, we will create a class for the referee. We will add a method to the referee to create a new board class with the desired parameters. We will add a method that sanitizes player input interactions. We will add functionality to check whether or not the game is over. When it is, it will broadcast that to the players. We will also add a method to update the overserves on the game/player state. 

 

For sprint three we think it is completable in 20 hours. We will create a player class. This class has a method to read input from a file for testing purposes or handle human input. It will have a method that takes the input and determines what methods to call in the player-referee interface. It will also have a method to receive updates from the interface about the game state/what the players standing with the referee is. 

 

By exclusively using methods to communicate it should be straightforward to convert a web version or other version. 
