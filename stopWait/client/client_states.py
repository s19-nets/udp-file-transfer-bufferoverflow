#! /usr/bin/env python3
from cstate import State
#TODO: create client states based on state machine diagram 
#TODO: update each state to the next state based on the event that has occured
class IdleState(State):
    def on_event(self,event):
        if event['event'] == 'msg_sent':
            if event['msg'] == "GET":
                return GetState()
            else:
                return PutState()
        return self

class WaitState(State):
    def on_event(self,event):
        if event['event'] == 'msg_recv':
            if event['msg'] == "ACK":
                return PutState()
            else:
                return GetState()
        return WaitState()

class GetState(State):
    def on_event(self,event):
        if event['event'] == 'msg_send':
            return WaitState()
        return self

class PutState():
    def on_event(self,event):
        if event['event'] == 'msg_send':
            return WaitState()
        return self

