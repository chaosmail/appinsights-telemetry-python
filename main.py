from applicationinsights import TelemetryClient
from time import sleep
import argparse
import psutil


# wait x seconds to compute the CPU utilization
CPU_WAIT_TIME = 0.5
# wait x seconds to log the telemetry data
SLEEP_TIME = 1

def parse_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--appinsights-key', required=True)
    parser.add_argument('-c', '--cpu-wait-time', default=CPU_WAIT_TIME)
    parser.add_argument('-s', '--sleep-time', default=SLEEP_TIME)
    return parser.parse_args()

def get_cpu_counters(interval=None, percpu=False):
    cpu_times = dict(psutil.cpu_times(percpu=percpu)._asdict())
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=percpu)
    cpu_stats = dict(psutil.cpu_stats()._asdict())
    return {'cpu_percent': cpu_percent, 'cpu_times': cpu_times, 'cpu_stats': cpu_stats}

def get_disk_counters(path='/'):
    disk_usage = dict(psutil.disk_usage(path=path)._asdict())
    return {'disk_usage': disk_usage}

def get_memory_counters():
    virtual_memory = dict(psutil.virtual_memory()._asdict())
    return {'virtual_memory': virtual_memory}

def get_network_counters(pernic=False):
    net_io_counters = dict(psutil.net_io_counters(pernic=pernic)._asdict())
    return {'net_io_counters': net_io_counters}

def track_dict_as_metric(tc, d, prefix=''):
    for k, v in d.items():
        if isinstance(v, dict):
            track_dict_as_metric(tc, v, "%s_" % k)
        else:
            tc.track_metric("%s%s" % (prefix, k), v)

def main():
    args = parse_cli_args()
    tc = TelemetryClient(args.appinsights_key)
    
    while True:
        cpu = get_cpu_counters(interval=args.cpu_wait_time)
        track_dict_as_metric(tc, cpu)

        memory = get_memory_counters()
        track_dict_as_metric(tc, memory)

        disk = get_disk_counters()
        track_dict_as_metric(tc, disk)

        network = get_network_counters()
        track_dict_as_metric(tc, network)

        tc.flush()
        sleep(args.sleep_time) 

if __name__ == "__main__":
    main()
