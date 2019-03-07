#! /usr/bin/env python3

from server_states import IdleState

class ServerStateMachine(object): 
    def __init__(self):
        self.state = IdleState()

    def on_event(self, event): 
        self.state = self.state.on_event(event)

    ''' TODO: create a function to get the current 
        state of the server state machine. 
        Sanchez'''
    def getCurrentState(self):
        return str(self.state)
