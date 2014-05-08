#!/bin/bash
# Launches go benchmarks in Linux and AKAROS and plots comparisons.

# Scripts.
readonly SCR_REPORTER=./reporter.py

# Temporary output files.
readonly RAW_OUTPUT_FILE_LINUX=./tmp/raw_output_linux.txt
readonly RAW_OUTPUT_FILE_AKAROS_NORMAL=./tmp/raw_output_akaros_normal.txt
readonly BENCH_OUTPUT_FILE_LINUX=./tmp/bench_output_linux.txt
readonly BENCH_OUTPUT_FILE_AKAROS_NORMAL=./tmp/bench_output_akaros_normal.txt


mkdir -p tmp

# Get Linux benchmarks.
# go test std -bench="." > $RAW_OUTPUT_FILE_LINUX
cat $RAW_OUTPUT_FILE_LINUX | grep Benchmark > $BENCH_OUTPUT_FILE_LINUX

# Get Akaros benchmarks
# TODO(alfongj): implement
cat $RAW_OUTPUT_FILE_AKAROS_NORMAL | grep Benchmark > $BENCH_OUTPUT_FILE_AKAROS_NORMAL

# Parse benchmarks and plot based on them.
$SCR_REPORTER LINUX $BENCH_OUTPUT_FILE_LINUX AKAROS $BENCH_OUTPUT_FILE_AKAROS_NORMAL

# Cleanup
rm -f ./tmp/*
