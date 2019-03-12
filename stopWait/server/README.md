# **SERVER UDP Protocol**
Simple server that sends files to client and saves files from the client

## Future tasks to do
- [] Implement an error state where all the errors are logged into a file.
- [] Create a class object for server state handlers
- [] Sliding window

### Contributors
- Eder Rodriguez
- Briana Sanchez

### Running server
```
python3 server.py [Optional: --serverport <server address>:<port>]
```
The servers happy state is its "idle."
The server will run for ever waiting for clients to connect. 
The server updates its state based on events happening. 

#### States
- Idle
- Wait
- Get
- Put
- TODO: Error

#### Events
- Message recived 
- Message sent 
- Timeout 
- Resend message times limit reached
