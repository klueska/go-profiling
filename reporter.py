#!/usr/bin/python
"""This script will parse a list of files that contain Go test outputs in their 
standard format, and make comparisons between a base one (normally, Linux) 
and the rest of them.

Format: <LABEL_FOR_BASE> <PATH_TO_BASE_OUTPUT_FILE>"
           ...followed by at least 1 pair of:"
         <LABEL_OF_COMPARISON>  <PATH_TO_FILE_FOR_COMPARISON>"

 e.g.:   LINUX bench_output_linux.txt"
         AKAROS bench_output_akaros.txt"
         AKAROS_SOMETHING_MODIFIED bench_output_akaros_blah.txt"
"""

import go_benchmark_parser as parser
import go_benchmark_plotter as plotter
import sys



def __check_arguments(argv) :
	"""Checks that the file has been called with the proper arguments.
	"""
	if (len(argv) <= 4) or (len(argv) % 2 != 1) :
		print "Error: Calling reporter.py with wrong number of args."
		print "\t Format: <LABEL_FOR_BASE> <PATH_TO_BASE_OUTPUT_FILE>"
		print "\t           ...followed by at least 1 pair of:"
		print "\t         <LABEL_OF_COMPARISON>  <PATH_TO_FILE_FOR_COMPARISON>"
		print ""
		print "\t e.g.:   LINUX bench_output_linux.txt"
		print "\t         AKAROS bench_output_akaros.txt"
		print "\t         AKAROS_SOMETHING_MODIFIED bench_output_akaros_blah.txt"
		exit(1)

def populate_benchmarks_from_files(files) :
	"""Takes a list of TITLE PATH_TO_FILE TITLE2 PATH_TO_FILE2 ... and parses
	them into an array of maps.
	"""
	benchmarks = []

	# Parse outputs.
	for i in xrange(0, len(files), 2) :
		benchmarks.append({
			"name": files[i],
			"objs": parser.parse_file(files[i+1])
		})

	return benchmarks

def normalize_benchmarks(base, benchmarks) :
	"""Iterates through a list of benchmarks and normalizes them against a given
	array of "base" benchmarks.
	"""
	missing_benchmarks = []
	for bench_name in base["objs"].keys() :
		if bench_name in benchmarks["objs"] :
			base_bench = base["objs"][bench_name]
			benchmarks["objs"][bench_name].normalize_from(base_bench)
		else :
			missing_benchmarks.append(bench_name)

	if len(missing_benchmarks) > 0 :
		print "The following benchmarks were not present in "+benchmarks["name"]
		for bench_name in missing_benchmarks :
			print "\t%s" % bench_name



def main() :
	# Check input.
	__check_arguments(sys.argv)

	# Parse benchmarks from the input files.
	benchmarks = populate_benchmarks_from_files(sys.argv[1:])
	base = benchmarks[0]
	
	# Normalize benchmarks: represent them as a delta improvement over the base.
	for i in xrange(1, len(benchmarks)) :
		normalize_benchmarks(base, benchmarks[i])

	plotter.normalized_performance_line_plot(benchmarks[1:], 
	                                         benchmarks[0]["name"])


main()
