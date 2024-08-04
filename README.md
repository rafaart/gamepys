# gamepys
# Parkour Game

## Description
This is a game inspired by Russ's project from the "Code with Russ" YouTube channel. Thank you, Russ! It has modifications because the goal was just to understand the functioning of the Pygame library. If you want, check out the project website before starting here.
<http://www.codingwithruss.com/gamepage/Platformer/>

The sprites and images are open source from the Kenney website. Feel free to look at the assets they provide and donate to the maintenance of the site.
<https://kenney.nl/>

The game is structured to be a platform game, so you must move through the game frames until you reach the final goal, which is the door.

The game scenario is divided into a matrix, and the dimensions of each frame of this matrix are what I call bricks.

The method of scaling and transforming the game characters was modified to always be relative to the size of the bricks. Thus, you can have the expected result in the transformations and positioning of the character and brick images, regardless of the resolution of the screen.
