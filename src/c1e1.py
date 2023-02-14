import concurrent.futures
from functools import partial
from math import sqrt
from timeit import default_timer as timer

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

	return x

def is_prime_cpp(x):
	import mastering_concurrency_cpp as mcc
	return mcc.is_prime(x)

def get_primes_sequential(function: callable, input_list: list[int]):
	return [i for i in input_list if function(i)]

def get_primes_futures(function: callable, input_list: list[int]):
	result = []

	with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
		futures = [executor.submit(function, i) for i in input_list]

		for future in concurrent.futures.as_completed(futures):
			if future.result():
				result.append(future.result())

	result.sort()
	return result

def get_primes_cpp_threads(input_list: list[int], n_threads: int):
	import mastering_concurrency_cpp as mcc
	number_list = mcc.NumberList(input_list)
	return mcc.get_primes(number_list, n_threads)

def run_benchmark(name: str, get_primes: callable, original_result: list[int] = None):
	start = timer()
	result = get_primes()
	elapsed = timer() - start
	print(f"{name}")

	if original_result is not None:
		print("Correct." if list(result) == original_result else "INCORRECT RESULT!")

	print(f"Execution time: {elapsed:.2f} s." "\n")
	return result

def run_benchmarks(data: list[tuple[str, callable]]):
	input_list = [i for i in range(10 ** 13, 10 ** 13 + 500)]
	original_result = run_benchmark(data[0][0], partial(data[0][1], input_list))

	for name, function in data[1:]:
		run_benchmark(name, partial(function, input_list), original_result)

if __name__ == "__main__":
	run_benchmarks([
		("Sequential, only Python", partial(get_primes_sequential, is_prime)),
		("Sequential, C++ extension", partial(get_primes_sequential, is_prime_cpp)),
		("Parallel, only Python", partial(get_primes_futures, is_prime)),
		("Parallel, C++ extension with futures", partial(get_primes_futures, is_prime_cpp)),
		("Parallel, threads in C++ extension", partial(get_primes_cpp_threads, n_threads=20))
	])