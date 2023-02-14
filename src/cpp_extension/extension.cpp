#include <algorithm>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <thread>
namespace py = pybind11;

using NumberList = std::vector<size_t>;

PYBIND11_MAKE_OPAQUE(NumberList);

size_t is_prime(const size_t x)
{
	if (x < 2)
	{
		return 0;
	}
	if (x == 2)
	{
		return 0;
	}
	if (x % 2 == 0)
	{
		return 0;
	}

	const auto limit = static_cast<size_t>(std::sqrtl(x)) + 1;

	for (size_t i = 3; i < limit; i += 2)
	{
		if (x % i == 0)
		{
			return 0;
		}
	}

	return x;
}

NumberList get_primes(const NumberList &numbers, const size_t num_threads = 1)
{
	if (num_threads == 1)
	{
		NumberList primes{};

		for (const auto &number : numbers)
		{
			if (is_prime(number))
			{
				primes.push_back(number);
			}
		}

		return primes;
	}
	else
	{
		const auto chunk_size = numbers.size() / num_threads;
		std::vector<NumberList> prime_lists(num_threads);
		std::vector<std::thread> threads{};

		for (size_t i = 0; i < num_threads; ++i)
		{
			auto &primes = prime_lists[i];
			const auto start = numbers.begin() + i * chunk_size;
			const auto end = (i == num_threads - 1) ? numbers.end() : start + chunk_size;

			threads.emplace_back([start, end, &primes]()
								 {
				for (auto it = start; it != end; ++it)
				{
					if (is_prime(*it))
					{
						primes.push_back(*it);
					}
				} });
		}

		for (auto &thread : threads)
		{
			thread.join();
		}

		NumberList primes{};
		for (auto &prime_list : prime_lists)
		{
			primes.insert(primes.end(), prime_list.begin(), prime_list.end());
		}

		std::sort(primes.begin(), primes.end());
		return primes;
	}

	return {};
}

PYBIND11_MODULE(mastering_concurrency_cpp, m)
{
	py::bind_vector<NumberList>(m, "NumberList");
	m.doc() = "C++ versions of the functions from the book Mastering Concurrency in Python by Quan Nguyen.";
	m.def("is_prime", is_prime, "A function that checks if a number is prime.");
	m.def("get_primes", get_primes, "A function that returns a list of prime numbers from a list of numbers.");
}