Tanks 
=====
A small two-player game, utlizing the PyGame library for 
obvious reasons and the Twisted library for real-time 
updating via the event-driven programming paradigm.  
Python 2.x.x Required 
Pygame and Twisted libraries required   
Access to terminal required, Linux systems preferred ;)  

##Usage
To run the game, first download the source code from GitHub.  
Once the code is downloaded, change directory to `tanks/`  
To enable execution, run `chmod +x host.py client.py`  
In order to run the programs on your machine, you need to open 
`client.py` and edit the `HOST` to the host computer name you plan 
on using  
To start the two-player game, first run `./host.py` on one machine  
To start the other player, fun `./client.py` on another

##Controls
To move, use the arrow keys on your keyboard  
Another option to move are the `w a s d` keys 
To aim, point the mouse in your desired shooting location  
To fire, left-click or hit the space bar  
  
Your goal is to kill all the enemy tanks, to leave you and your 
partner in victory!

 
##To Do
- [x] set up basic game space  
- [x] create a single level for a single player  
- [x] add networking concepts  

##Future Work
- [ ] add upper levels

##Sources
http://www.pygame.org/docs/  
https://twistedmatrix.com/trac/wiki/Documentation  
