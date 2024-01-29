(a) Establish a TCP connection in between a server process, running on host A and a client process,
running on host B and then perform some operation by the server process requested by the
client and send responses from the server.

(b) Using the above connection, design and implement a non-idempotent operation using exactly-
once semantics that can handle the failure of request messages, failure of response messages
and process execution failures.