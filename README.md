# Chess Tournament

## Description:
Project 4 of OpenClassrooms Path: Developer Python - Chess Tournament -- create a console based Chess Tournament 
program 

The application must be a stand-alone, offline program. The program must be written in Python and run from the console.
In other words, the execution of the program should look like this: **python3 main.py** . The program should run 
on Windows, Mac or Linux and have a requirements.txt file listing the dependencies needed to run the program.
We would like to contain a database of players in JSON files. 
The program should have a section dedicated to adding players and a tournament.


## Installation:
open terminal
1. `git clone https://github.com/DoriDoro/Chess_Tournament.git`
2. `cd Chess_Tournament`
3. `python -m venv venv`
4. `. venv/bin/activate` (on MacOS/Linux) `venv\Scripts\activate` (on Windows)
5. `pip install -r requirements.txt`
6. `python3 main.py`


## flak8-report:
open terminal
1. `cd Chess_Tournament`
2. `python -m venv venv`
3. `. venv/bin/activate` (on MacOS/Linux) `venv\Scripts\activate` (on Windows)
4. `flake8 --format=html --htmldir=flake8-report`

## Visualisation of the project:
1. start the program with `python3 main.py`
2. The Main Menu:
![Main Menu](/images_Readme/MainMenu.png)
3. Create a new Player:
   1. Choose the Tournament for the new Player:
   ![Choose a Tournament for the new Player](/images_Readme/ChooseTournament.png)
   2. Create a new Player:
   ![Create a Player](/images_Readme/CreateAPlayer.png)
   3. Tournament already all Players:
   ![Tournament full](/images_Readme/Tournament_AlreadyAllPlayers.png)
4. Create a new Tournament:
![Create a Tournament](/images_Readme/CreateTournament.png)
5. Start a Tournament:
   1. Choose the Tournament you want to start:
   ![Choose a Tournament](/images_Readme/ChooseTournament.png)
   2. The chosen Tournament starts the first round
   3. Set the scores for the first round:
   ![Scores first round](/images_Readme/EnterScoreFirstMatch.png)
   4. Results of the first round:
   ![Results first round](/images_Readme/ResultsFirstMatch.png)
   5. Question to continue with next round or quit Tournament:
      (I have chosen to quit the Tournament for demonstrate purpose)
   ![Quit Tournament](/images_Readme/QuitTournament.png)
6. Resume Tournament:
![Resume Tournament](/images_Readme/ResumeTournament.png)
![Second round](/images_Readme/SecondRound.png)
7. Results of Tournaments:
![Results all Players](/images_Readme/ResultDisplayAllPlayers.png)
![Results names of Tournament](/images_Readme/ResultNamesOfTournament.png)
![Results names and dates](/images_Readme/ResutlsNameDatesTournament.png)
![Results players of Tournament](/images_Readme/ResultPlayerOfTournament.png)
![Result of matches](/images_Readme/ResultsMachtesTournament.png)
