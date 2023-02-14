import pybind11 as pb
import setuptools as st
from setuptools.command.build_ext import build_ext

class BuildExt(build_ext):
	opts = {
		"msvc": ["/EHsc", "/O2", "/std:c++17"],
		"unix": ["-march=native", "-O3", "-std=c++17"]
	}
	
	def build_extensions(self):
		opts = self.opts.get(self.compiler.compiler_type, [])

		for ext in self.extensions:
			ext.extra_compile_args.extend(opts)

		build_ext.build_extensions(self)

if __name__ == "__main__":
	name = "mastering_concurrency_cpp"

	st.setup(
		author="Matěj Chmel",
		author_email="58189701+Matej-Chmel@users.noreply.github.com",
		cmdclass={
			"build_ext": BuildExt
		},
		description="C++ versions of the functions from the book Mastering Concurrency in Python by Quan Nguyen.",
		ext_modules=[
			st.Extension(
				name,
				["./extension.cpp"],
				include_dirs=[pb.get_include()],
				language="c++"
			)
		],
		name=name,
		version="0.0.1",
		zip_safe=False
	)