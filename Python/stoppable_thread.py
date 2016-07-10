import threading



class StoppableThread(threading.Thread):
    # This is a Thread class with a stop() method. The thread itself has to check constantly if it's been stopped by
    # using the stopped() method.

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()

    # Stops the thread.
    def stopit(self):
        self._stopper.set()

    # Returns a boolean value telling if the thread has been stopped.
    def stopped(self):
        return self._stopper.is_set()
