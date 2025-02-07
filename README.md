These three files together form a simple client-server chat application with basic administrative functionalities.

gui_client.pyw
This file is the client-side script for a chat application using Tkinter for the GUI and socket programming for network communication. 
It handles user interactions, message sending, and receiving, as well as administrative commands like kicking or banning users.
The script also includes functions for changing usernames and handling password input for admin users.

BAN.txt
This file contains a list of banned users. Each line in the file represents a username that has been banned from the chat application. 
The server script reads from and writes to this file to manage the list of banned users.

server_chat.py
This file is the server-side script for the chat application. 
It handles incoming client connections, relays messages between clients, and processes administrative commands such as kicking, banning, and pardoning users.
The server uses threading to manage multiple client connections simultaneously and maintains a list of connected users and their addresses.
