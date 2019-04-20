from applicationinsights import TelemetryClient
from time import sleep
import argparse
import psutil


# wait x seconds to compute the CPU utilization
# or compute utilization between the last call
CPU_INTERVAL_S = None

# wait x seconds to log the telemetry data
LOG_INTERVAL_S = 5

to_dict = lambda d: dict(d._asdict()) if d is not None else {}

def parse_cli_args():
    """Parses the CLI arguments"""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-k', '--appinsights-key', required=True)
    parser.add_argument('-c', '--cpu-interval', default=CPU_INTERVAL_S)
    parser.add_argument('-l', '--log-interval', default=LOG_INTERVAL_S)
    
    parser.add_argument('--percpu', nargs='?', const=True, default=False)
    parser.add_argument('--perdisk', nargs='?', const=True, default=False)
    parser.add_argument('--path', default='/')
    parser.add_argument('--pernic', nargs='?', const=True, default=False)
    
    return parser.parse_args()

def get_cpu_counters(interval=None, percpu=False):
    """Returns CPU counters as dict"""
    cpu_times = to_dict(psutil.cpu_times(percpu=percpu))
    cpu_percent = psutil.cpu_percent(interval=interval, percpu=percpu)
    cpu_stats = to_dict(psutil.cpu_stats())
    return {
        'cpu_percent': cpu_percent, 
        'cpu_times': cpu_times, 
        'cpu_stats': cpu_stats,
    }

def get_disk_counters(path='/', perdisk=False):
    """Returns the diks counters as dict"""
    disk_usage = to_dict(psutil.disk_usage(path=path))
    disk_io_counters = to_dict(psutil.disk_io_counters(perdisk=perdisk))
    return {
        'disk_usage': disk_usage,
        'disk_io_counters': disk_io_counters,
    }

def get_memory_counters():
    """Return the memory counters as dict"""
    virtual_memory = to_dict(psutil.virtual_memory())
    swap_memory = to_dict(psutil.swap_memory())
    return {
        'virtual_memory': virtual_memory,
        'swap_memory': swap_memory,
    }

def get_network_counters(pernic=False):
    """Returns the network counters as dict"""
    net_io_counters = to_dict(psutil.net_io_counters(pernic=pernic))
    return {
        'net_io_counters': net_io_counters,
    }

def track_dict_as_metric(tc, d, prefix=''):
    """Recursively emits a dict of values as metric to app insights"""
    for k, v in d.items():
        if isinstance(v, dict):
            track_dict_as_metric(tc, v, "%s_" % k)
        else:
            tc.track_metric("%s%s" % (prefix, k), v)

def perform_log(tc, args={}):
    """Collects all counters and tracks them"""
    opt_cpu_interval = args.get('cpu_interval', CPU_INTERVAL_S)
    opt_percpu = args.get('percpu', False)
    cpu = get_cpu_counters(interval=opt_cpu_interval, percpu=opt_percpu)
    track_dict_as_metric(tc, cpu)

    memory = get_memory_counters()
    track_dict_as_metric(tc, memory)

    opt_path = args.get('path', '/')
    opt_perdisk = args.get('perdisk', False)
    disk = get_disk_counters(path=opt_path, perdisk=opt_perdisk)
    track_dict_as_metric(tc, disk)

    opt_pernic = args.get('pernic', False)
    network = get_network_counters(pernic=opt_pernic)
    track_dict_as_metric(tc, network)

    tc.flush()


def main():
    """Main programm"""
    args = parse_cli_args()
    tc = TelemetryClient(args.appinsights_key)
    
    while True:
        res = perform_log(tc, args.__dict__)
        sleep(args.log_interval)

if __name__ == "__main__":
    main()
