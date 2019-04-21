# Python AppInsights Telemetry Logger

Log your system telemetry to AppInsights custom metrics using the [psutil](https://psutil.readthedocs.io/en/latest/) library in Python. To visualize the telemetry data you can use [Kusto Query Language](https://docs.microsoft.com/en-us/azure/kusto/query/) in AppInsights.

## Quick'n'dirty

```sh
curl https://raw.githubusercontent.com/chaosmail/appinsights-telemetry-python/master/main.py
python -m pip install appinsights psutil
python main.py -- options
```

## Options

By default, the telemetry logger only logs the CPU utilization in percent. However, many other metrics exposed by `psutil` can be logged as well using the apppropriate command line options.

```
usage: main.py [-h] -k APPINSIGHTS_KEY [-c CPU_INTERVAL] [-l LOG_INTERVAL]
               [-p] [--percpu] [--perdisk] [--path PATH] [--pernic]
               [--cpu-times] [--cpu-stats] [--virtual-memory] [--swap-memory]
               [--disk-usage] [--disk-io-counters] [--net-io-counters]

optional arguments:
  -h, --help            show this help message and exit
  -k APPINSIGHTS_KEY, --appinsights-key APPINSIGHTS_KEY
  -c CPU_INTERVAL, --cpu-interval CPU_INTERVAL
  -l LOG_INTERVAL, --log-interval LOG_INTERVAL
  -p, --print
  --percpu
  --perdisk
  --path PATH
  --pernic
  --cpu-times
  --cpu-stats
  --virtual-memory
  --swap-memory
  --disk-usage
  --disk-io-counters
  --net-io-counters
```

## Examples

Log the CPU utilization, disk usage and virtual memory consumption every 10 seconds.

```sh
python main.py \
	--appinisghts-key <insert instrumentation key> \
	--log-interval 10 \
	--disk-usage \
	--virtual-memory 
```

## Getting Started

```sh
make setup
make install
```

Run the script using the following command.

```sh
make run APPINSIGHTS_KEY=<insert instrumentation key>
```

The data will be logged to AppInsights `customMetrics`.

## Visualize in AppInisghts

To visualize metrics in AppInsights go to the `Analytics` pane and type your query.

Here is an example visualizing percentage of CPU utilization, memory consumption and used disk space.

```
customMetrics
| where name in ("cpu_percent", "virtual_memory.percent", "disk_usage.percent") 
| where timestamp > ago(15m)
| sort by timestamp desc nulls first
| render timechart 
```

## License

This software is provided under MIT license.
