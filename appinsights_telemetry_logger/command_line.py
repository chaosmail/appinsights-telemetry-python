from applicationinsights import TelemetryClient
from time import sleep
import argparse
import psutil
import socket


# wait x seconds to compute the CPU utilization
# or compute utilization between the last call
CPU_INTERVAL_S = 0

# wait x seconds to log the telemetry data
LOG_INTERVAL_S = 5

def to_dict(d):
    if d is None:
        return {}
    elif isinstance(d, dict):
        return {k: to_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return {i: to_dict(v) for i, v in enumerate(d)}
    return dict(d._asdict())


def parse_cli_args():
    """Parses the CLI arguments"""
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-k', '--appinsights-key', required=True)
    parser.add_argument('-c', '--cpu-interval', default=CPU_INTERVAL_S, type=int)
    parser.add_argument('-l', '--log-interval', default=LOG_INTERVAL_S, type=int)
    parser.add_argument('-p', '--print', action='store_true')    

    # Configure the counters
    parser.add_argument('--percpu', action='store_true')
    parser.add_argument('--perdisk', action='store_true')
    parser.add_argument('--path', default='/')
    parser.add_argument('--pernic', action='store_true')
    
    # Enable additional counters
    parser.add_argument('--cpu-times', action='store_true')
    parser.add_argument('--cpu-stats', action='store_true')
    parser.add_argument('--virtual-memory', action='store_true')
    parser.add_argument('--swap-memory', action='store_true')
    parser.add_argument('--disk-usage', action='store_true')
    parser.add_argument('--disk-io-counters', action='store_true')
    parser.add_argument('--net-io-counters', action='store_true')

    return parser.parse_args()

def get_cpu_counters(args={}):
    """Returns CPU counters as dict"""
    res = {}

    interval = args.get('cpu_interval', CPU_INTERVAL_S)
    percpu = args.get('percpu', False)
    
    res['cpu_percent'] = psutil.cpu_percent(interval=interval, percpu=percpu)

    # Convert Unix style CPU utilization to task manager style
    if percpu is False:
        num_cpus = psutil.cpu_count(logical=False)
        res['cpu_percent'] /= num_cpus

    if args.get('cpu_times', False):
        res['cpu_times'] = to_dict(psutil.cpu_times(percpu=percpu))

    if args.get('cpu_stats', False):
        res['cpu_stats'] = to_dict(psutil.cpu_stats())
    
    return res

def get_disk_counters(args={}):
    """Returns the diks counters as dict"""
    res = {}
    
    path = args.get('path', '/')
    perdisk = args.get('perdisk', False)

    if args.get('disk_usage', False):
        res['disk_usage'] = to_dict(psutil.disk_usage(path=path))
    
    if args.get('disk_io_counters', False):
        res['disk_io_counters'] = to_dict(psutil.disk_io_counters(perdisk=perdisk))

    return res

def get_memory_counters(args={}):
    """Return the memory counters as dict"""
    res = {}

    if args.get('virtual_memory', False):
        res['virtual_memory'] = to_dict(psutil.virtual_memory())
    
    if args.get('swap_memory', False):
        res['swap_memory'] = to_dict(psutil.swap_memory())
    
    return res

def get_network_counters(args={}):
    """Returns the network counters as dict"""
    res = {}

    if args.get('net_io_counters', False):
        res['net_io_counters'] = to_dict(psutil.net_io_counters(pernic=pernic))

    return res

def get_properties(args={}):
    hostname = socket.gethostname()
    fqdn = socket.getfqdn()
    
    return {
        'hostname': hostname,
        'fqdn': fqdn,
    }

def track_dict_as_metric(tc, d, properties={}, prefix=''):
    """Recursively emits a dict of values as metric to app insights"""
    for k, v in d.items():
        if isinstance(v, dict):
            track_dict_as_metric(tc, v, properties, "%s." % k)
        else:
            tc.track_metric("%s%s" % (prefix, k), v, properties=properties)

def perform_log(tc, args={}):
    """Collects all counters and tracks them"""
    opt_print = args.get('print', False)
    properties = get_properties()

    if print:
        print(properties)

    cpu = get_cpu_counters(args)
    if len(cpu) > 0:
        track_dict_as_metric(tc, cpu, properties=properties)
        if opt_print:
            print(cpu)

    memory = get_memory_counters(args)
    if len(memory) > 0:
        track_dict_as_metric(tc, memory, properties=properties)
        if opt_print:
            print(memory)

    disk = get_disk_counters(args)
    if len(disk) > 0:
        track_dict_as_metric(tc, disk, properties=properties)
        if opt_print:
            print(disk)
    
    network = get_network_counters(args)
    if len(network) > 0:
        track_dict_as_metric(tc, network, properties=properties)
        if opt_print:
            print(network)

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

