import time
import thread
import threading

class MyThread(threading.Thread):

    def __init__(self, name, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.delay = delay

    def run(self):
        count = 2
        while True:
            print self.name
            count -= 1
            if count == 0 : 
                break
            time.sleep(self.delay)

if __name__ == "__main__":

    count = 0
    delay = 5
    while True:
        if threading.activeCount() < 5:
            print "active: %d" % threading.activeCount()
            thread = MyThread(count, delay)
            thread.start()
            count += 1
            delay -= 1
            if delay == 1 : delay = 5
