#! /usr/bin/env python3

#TODO: create client states based on state machine diagram 
#TODO: update each state to the next state based on the event that has occured


class GetState(State):
    def on_event(self,event):
        if event['event'] == 'msg_send'
        return WaitState()
    return self

class PutState():
    def on_event(self,event):
        if event['event'] == 'ACK'
        return WaitState()
    return self


