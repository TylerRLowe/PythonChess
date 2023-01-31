# PythonChess
A chess engine built using Python and pygame.I challanged myself to crete it form scratch without any outside resources, they only code I looked at from other was pygame related. I found it was faster to recalculate the moves every time then just progressing through depth, as having the moves in sorted order allows for much more efficent pruning. The engine is weak in general, but espically at the start and end of a game where it struggles to look far enough ahead to find the optimal moves. In order to run, you must install pygame using *pip install pygame* (consult https://pypi.org/project/pygame/ for more in depth instructions).
Here is a short clip of playing the game:
![image](https://user-images.githubusercontent.com/99204234/215834988-11f8baad-db52-4bb3-8cfa-ea390aa75444.png)

