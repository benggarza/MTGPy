class Event():
    def __init__(self, **kwargs):
        if 'creature' in kwargs:
            self.creature = True
            self.permanent = True
        if 'land' in kwargs:
            self.land = True
            self.permanent = True
        # TODO: finish the rest of the permanent types...
        # with this dev design we can leave this incomplete
        # and game objects can still interact