#! /usr/bin/env python3
from server_states import IdleState

class SeverStateMachine(object): 
    def __init__(self):
        self.state = IdleState()

    def on_event(self, event): 
        self.state = self.state.on_event(event)


