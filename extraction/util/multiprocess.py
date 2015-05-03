from multiprocessing import Process, Queue, Pool
import os, time, random

def test(queue):

    while True:
        try:
            item = queue.get_nowait()
        except:
            return
        index = item['index']
        value = item['value']
        lower = execu(value)
        item['value'] = lower
        result.append(item)
        print result

def execu(data):

    time.sleep(3)
    return data.lower()

if __name__ == "__main__":

    sample = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
              'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    buffer = []
    result = []
    for ind, data in enumerate(sample):buffer.append({'index':ind, 'value':data})

    queue = Queue()
    while True:
        try:
            for i in xrange(10):queue.put(buffer.pop(0)) 
        except: pass

        process = [None for i in range(3)]
        for i in range(3):
            process[i] = Process(target=test, args=(queue,))
            process[i].start()

        for i in range(3):
            process[i].join()

        print "next"
        if buffer == []:break

    print result
