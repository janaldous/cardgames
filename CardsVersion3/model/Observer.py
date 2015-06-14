"""Implementation of the Observer pattern from Head First Design Patters
(Chapter 2), using the pull method of passing data from the Subject to the
Observer(s). """

################################################################################
# Subject: thing that is listened to
################################################################################
class Subject:
    def make_observer_list(self):
        self._observer_list = []

    def register_observer(self, observer):
        """Registers an observer with WeatherData if the observer is not
        already registered."""
        try:
            if observer not in self._observer_list:
                self._observer_list.append(observer)
            else:
                raise ValueError
        except ValueError:
            print "ERROR: Observer already subscribed to Subject!"
            #raise ValueError

    def remove_observer(self, observer):
        """Removes an observer from WeatherData if the observer is currently
        subscribed to WeatherData."""
        try:
            if observer in self._observer_list:
                self._observer_list.remove(observer)
            else:
                raise ValueError
        except ValueError:
            print "ERROR: Observer currently not subscribed to Subject!"
            raise ValueError


    def notify_observers(self, *args):
        for observer in self._observer_list:
            observer(*args)

#================================================================
# Observer: thing that listens
#================================================================
class Observer:
	
    def update(self):
		pass#that game has ended or its player's turn

    