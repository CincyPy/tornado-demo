Tornado Server Demo for CincyPy

This is a simple example of a Tornado app that simulates a dice roll that
is shared between web clients. When opened in two tabs, when the dice is
rolled, it will update each tab with the new number.

To run:
1) Create a virtual environment, activate
2) Install pip dependencies: pip3 install -r requirements.txt
3) Run server: python3 server.py
4) Open app in several browser tabs by going to URL: localhost:8888
5) Roll the dice and watch it update!
6) To exit the server: CTRL-c

Sources:
Tornado Documentation: https://www.tornadoweb.org/en/stable/index.html
Chat demo: https://github.com/tornadoweb/tornado/tree/master/demos/chat
