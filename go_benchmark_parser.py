"""Parses a list of Go benchmark output lines into a formatted structure.
"""

import re



# RAW REGEX PATTERNS
PATTERN_NAME_ITERATIONS = '^Benchmark(\w+)(?:\s*)([0-9]+)'
PATTERN_NS_OP = '([0-9]+(?:\.[0-9]+)?) ns/op'
PATTERN_BWITH = '([0-9]+(?:\.[0-9]+)?) MB/s'
PATTERN_B_OP = '([0-9]+(?:\.[0-9]+)?) B/op'
PATTERN_ALLOCS_OP = '([0-9]+(?:\.[0-9]+)?) allocs/op'
PATTERN_BENCHMARK_LINE = PATTERN_NAME_ITERATIONS + \
                         '(?:(?:\s*)' + PATTERN_NS_OP + ')?' + \
                         '(?:(?:\s*)' + PATTERN_BWITH + ')?' + \
                         '(?:(?:\s*)' + PATTERN_B_OP + ')?' + \
                         '(?:(?:\s*)' + PATTERN_ALLOCS_OP + ')?' + \
                         '(?:\s*)$'

# COMPILED REGEX PATTERNS
REGEX_NAME_ITERATIONS = re.compile(PATTERN_NAME_ITERATIONS)
REGEX_NS_OP = re.compile(PATTERN_NS_OP)
REGEX_BWITH = re.compile(PATTERN_BWITH)
REGEX_B_OP = re.compile(PATTERN_B_OP)
REGEX_ALLOCS_OP = re.compile(PATTERN_ALLOCS_OP)
REGEX_BENCHMARK_LINE = re.compile(PATTERN_BENCHMARK_LINE)


class Benchmark(object):
	"""Represents the output of a Go benchmark"""
	def __init__(self, name, iterations) :
		super(Benchmark, self).__init__()
		self.name = name
		self.iterations = iterations
		self.metrics = {}
		self.n_metrics = {} # Normalized metrics with respect of a base.

	def parse_and_add_num(self, m_name, regex, line) :
		"""Parses a line of benchmark output looking for a given metric
		(specified by 'regex'), and if it finds it, it stores it under
		self.metrics[m_name]
		"""
		match = re.search(regex, line)
		if match :
			self.metrics[m_name] = float(match.group(1))

	def normalize_from(self, base) :
		"""It normalizes all metrics from a base Benchmark object, following 
		the following rules:
			- [ns_op]     -> (base_val - self_val) / base_val
			- [bandwith]  -> (self_val - base_val) / base_val
			- [B_op]      -> UNIMPLEMENTED
			- [allocs_op] -> UNIMPLEMENTED
		The normalized outputs are stored under self.n_metrics (dict).
		"""
		for base_metr, base_val in base.metrics.items() :
			if base_val == 0 :
				print "Warning: detected base score of 0 in %s>%s" % \
				      (base.name, base_metr)
				continue

			if base_metr in self.metrics :
				self_val = self.metrics[base_metr]

				if base_metr in ["ns_op"] :
					self.n_metrics[base_metr] = (base_val - self_val) / base_val
				elif base_metr in ["bandwith"] :
					self.n_metrics[base_metr] = (self_val - base_val) / base_val
				else :
					pass
					# TODO: Figure out what is the proper way for normalizing
					# B_op and allocs_op

def __parse_line(benchmarks, line) :
	"""Checks if the given line is the output from a Go benchmark, and if so, 
	it parses all its contents into a Benchmark object which gets added to 
	benchmarks[name] (where name is the name of the individual benchmark case)
	"""
	is_benchmark = re.match(REGEX_BENCHMARK_LINE, line)
	if is_benchmark:
		name = is_benchmark.group(1)
		iterations = int(is_benchmark.group(2))
		benchmark = Benchmark(name, iterations)

		benchmark.parse_and_add_num('ns_op', REGEX_NS_OP, line)
		benchmark.parse_and_add_num('bandwith', REGEX_BWITH, line)
		benchmark.parse_and_add_num('B_op', REGEX_B_OP, line)
		benchmark.parse_and_add_num('allocs_op', REGEX_ALLOCS_OP, line)

		benchmarks[name] = benchmark

def parse_file(file) :
	"""Opens a file and parses it looking for lines which contain valid Go 
	benchmark output text. Creates Benchmark objects from that output into an
	array that gets returned.
	"""
	try :
		output_file = open(file)
	except :
		print "Error: called go_benchmark_parser with nonexisting file."
		exit(1)
	
	benchmarks = {}
	for line in output_file :
		__parse_line(benchmarks, line)

	return benchmarks
