# MPC

Main.py forwards all messages to MessageParser.py

MessageParser.py checks if the message is a command. 
If: message command -> do some checks and execute
else: forward message to Photochallenge.py

Photochallenge keeps track of active photochallenges and checks entries for validity

Config.py holds and persists the state of some important variables. Avoids invalid states after restarting / crashing etc.
Configuration gets stores as json

Messenger.py is responsible for communicating with users.
