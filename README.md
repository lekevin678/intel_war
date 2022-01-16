# War
Python implementation of the card game War.

## Gameplay
* Two players, each with half a deck
* "Battle" begins with both players reveal top card of their deck
* Player with higher card wins and takes all cards on the board
* Aces are high and suites are ignored
* If the two cards are equal, then there is a "war"
    * Both players draw three cards from the top of their deck
    * Then "battle" again
    * Repeat until one player has higher reveal card 
    * Winner will get all cards on the board
* Play until a player gets all 52 cards or until a player does not have enough cards to put down for war or to reveal.

## Assumptions
* I am assuming that this is player vs computer and not player vs player.
* If player runs out of cards for war or battle, they instantly lose.

## Corner Cases
**War occurring 2+ times:** My code handles this with recursion. In the "battle" function, if "war" occurs, it will call "battle" again, passing in the current cards on the board. Recursion will stop when a player wins the battle (has higher card than other player) or when a player does not have enough cards to put down.
``` 
battle
|___war
    |___battle
        |___war
            |___battle
``` 
## If I Had More Time
