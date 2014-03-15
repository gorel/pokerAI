from multiprocessing import cpu_count, Pool
import time
import random

def f():
	count = 0
	score = 0
	start = time.time()
	while (time.time() - start < 1):
		count += 1
		if random.random() > 0.5:
			score += 1
	return (score, count)

start = time.time()
cores = cpu_count()
print 'Number of cores:', cores
pool = Pool(processes=cores)
results = []
for _ in range(cores):
	result = pool.apply_async(f, ())
	results.append(result)

pool.close()
pool.join()

score = 0
count = 0
for result in results:
	result = result.get()
	score += result[0]
	count += result[1]

print 'Score:', score, 'Count:', count
print 'Fraction:', score / float(count)
print 'Time elapsed:', time.time() - start
