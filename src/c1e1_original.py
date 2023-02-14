from math import sqrt

# There is a bug in this code when calling it as a future.
# In the file c1e1.py is a fix that returns the x parameter instead of True.
def is_prime(x):
	if x < 2:
		return False
	if x == 2:
		return True
	if x % 2 == 0:
		return False

	limit = int(sqrt(x)) + 1

	for i in range(3, limit, 2):
		if x % i == 0:
			return False

	return True

if __name__ == "__main__":
	input = [i for i in range(10 ** 13, 10 ** 13 + 500)]

	from timeit import default_timer as timer

	# Sequential
	start = timer()
	result = []

	for i in input:
		if is_prime(i):
			result.append(i)

	print("Result 1: ", result)
	print("Took: %.2f seconds." % (timer() - start))

	# Concurrent

	import concurrent.futures

	start = timer()
	result = []

	with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
		futures = [executor.submit(is_prime, i) for i in input]

		for i, future in enumerate(concurrent.futures.as_completed(futures)):
			if future.result():
				result.append(input[i])
	
	result.sort()
	print("Result 2: ", result)
	print("Took: %.2f seconds." % (timer() - start))