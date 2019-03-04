#! /usr/bin/env python3

from state import State

class IdleState(State): 
    def on_event(self, event):
        if event['event'] == 'msg_recv':
            if event['msg'] == "GET":
                return GetState()
            else:
                return PutState()
        return self

class WaitState(State):
    def on_event(self, event): 
        if event['event'] == 'msg_recv': 
            if event['msg'] == "ACK": 
                return GetState()
            else: 
                return PutState()
        return self

class GetState(State): 
    def on_event(self, event):
        if event['event'] == 'msg_sent': 
            return WaitState()
        return self

class PutState(State):
    def on_event(self, event):
        if event['event'] == 'msg_sent': 
            return WaitState()
        return self

