#! /usr/bin/env python3

''' This class is exactly the same as the sstate.py 
    from the server, beacuse we still want the client 
    to be updated on events happeing'''

class State(object): 
    def __init__(self): 
        print("Processing current state: %s" % str(self))

    def on_event(self,event):
        pass

    def __repr__(self): 
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__
