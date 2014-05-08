"""Plotting functions for Go benchmarks.
"""

import matplotlib.pyplot as plt



# Metrics that we want to plot benchmarks of.
METRICS = ["ns_op", "bandwith"]
COLORS = ["y", "b", "g", "r", "c", "m"]
cur_color_idx = 0


def __next_color() :
	"""Cycles through the COLORS array.
	"""
	global cur_color_idx
	cur_color_idx = (cur_color_idx + 1) % len(COLORS)
	return COLORS[cur_color_idx]

def __plot_add_decreasing_line(datapoints) :
	"""Adds a line to the current pyplot containing:
		- As X values: Range from 1 to len(datapoints).
		- As Y values: datapoints ordered from greatest to lowest.
	"""
	xpoints = xrange(1, len(datapoints) + 1)
	datapoints.sort(reverse=True)
	
	c = __next_color()
	plt.plot(xpoints, datapoints, color=c)

	crossing_X_axis_point = len([i for i in datapoints if i >= 0])
	plt.axvline(x=crossing_X_axis_point, color=c)

def __show_plot(title, legend) :
	"""Displays graphically the current pyplot with a given legend and title.
	"""
	plt.usevlines=True
	plt.axhline(y=0, color="black")
	plt.suptitle(title)
	plt.legend(legend, loc="upper right")
	plt.show()



def normalized_performance_line_plot(benchmarks, base_name) :
	"""Draw, for each metric, a plot with a line that shows the normalized 
	performance of each benchmark configuration.
	"""
	for m in METRICS :
		for bench in benchmarks :
			benchmark_arr = bench["objs"].values()
			# Extract all normalized benchmark scores of the current benchmark
			# array and for one metric into a plain array.
			n_bench_sc = [x.n_metrics[m] for x in benchmark_arr if m in x.n_metrics]
			__plot_add_decreasing_line(n_bench_sc)

		legend = map(lambda x: x["name"], benchmarks)

		__show_plot("Normalized performance (" + m + ") of Go benchmarks " + \
		            "VS " + base_name, legend)
