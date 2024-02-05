Title of the Experiment: Implementing File transfer using Socket Programming and HTTP GET/POST requests
Objective:
The objective of this lab is to give hands-on experience with socket programming and HTTP file transfer. You will
- implement multithreaded chat from many clients to one server
- set up an HTTP server process with a few objects
- use GET and POST methods to upload and download objects in between HTTP clients and a server

Task 1: File Transfer via Socket Programming
1. Implement a simple file server that listens for incoming connections on a specified port. The server should be able to
handle multiple clients simultaneously.
2. When a client connects to the server, the server should prompt the client for the name of the file they want to
download.
3. The server should then locate the file on disk and send it to the client over the socket.
4. Implement a simple file client that can connect to the server and request a file. The client should save the file to disk
once it has been received.
Task 2: File Transfer via HTTP
1. Implement a simple HTTP file server that listens for incoming connections on a specified port. The server should be
able to handle multiple clients simultaneously.
2. When a client sends a GET request to the server with the path of the file they want to download, the server should
locate the file on disk and send it to the client with the appropriate HTTP response headers. The client should save the
file to disk once it has been received.
3. When a client sends a POST request to the server with a file, the server saves it.