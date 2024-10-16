# python_chess_ai
First defines a chess game using linting, unit tests and an object-oriented structure. When this work is satisfactory pytorch will be used to train an ai using reinforcement learning.

To do:
* Create a working chess game - In progress
* Create AI model that learns to play chess through reinforcement learning.
* Create AI model that predicts the probability of victory/draw/loss.

Ideas:
* Create GUI
* Make the game into an application with an endpoint
* Make containerized players that can act through the endpoint
* Deploy as application that other players can interact with and log the games
* Download chess games from chess.com and use supervised learning to train/pretrain on these. This would ease training considerably.

## Illustration of classes
![Classes](images/chess_classes.png?raw=true "Classes")

## They see me giffin' they hatin'
![Gif](images/chess_game.gif?raw=true "Gif")

## Create a working chess game
Table of classes and main with progress
| status | Name | Description | Assignee | Branch |
|---|---|---|---|---|
| ✅ | ChessPiece   |   |   |   |
| ✅ | King         |   |   |   |
| ✅ | Pawn         |   |   |   |
| ⌛ | Bishop      |   | thelodberg | [Bishop](https://github.com/Marsusss/python_chess_ai/tree/Bishop_Implementation) |
| :x: | Knight      |   |   |   |
| :x: | Rook        |   |   |   |
| :x: | Queen       |   |   |   |
| ✅ | Board        |   |   |   |
| ✅ | Score        |   |   |   |
| ✅ | GameLog      |   |   |   |
| ✅ | GameLogList  |   |   |   |
| ✅ | Game |   |   |   |
| :x: | Games |   |   |   |
| ✅ | Player |   |   |   |
| :x: | HumanPlayer |   |   |   |
| ✅ | AiPlayer    |   |   |   |
| :x: | Model       |   |   |   |
| :x: | main        |   |   |   |
