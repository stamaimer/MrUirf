import multiprocessing

def worker(lock, indices):

	while 1:
		
		lock.acquire()

		print "%s acquire lock, current indices is %d" % (multiprocessing.current_process().name, indices.value)

		indices.value += 1

		print "%s release lock, current indices is %d" % (multiprocessing.current_process().name, indices.value)

		lock.release()

lock = multiprocessing.Lock()

indices = multiprocessing.Value('i', 0)

AMOUNT_OF_PROCESS =  multiprocessing.cpu_count() * 6

process = [ None for i in xrange(AMOUNT_OF_PROCESS) ]

for i in xrange(AMOUNT_OF_PROCESS):

    process[i] = multiprocessing.Process(target=worker, args=(lock, indices))

    process[i].start()

# for i in xrange(AMOUNT_OF_PROCESS):

#     process[i].join()