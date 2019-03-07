#! /usr/bin/env python3
''' This class should also be techically the same as serverstatemachine'''
class ClientStateMachine(object): 
    def __init__(self): 
        self.state = IdleState()

    def on_event(self, event):
        self.state = self.state.on_event(event)

    def getCurrentState(self):
        return str(self.state)
