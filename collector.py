from prometheus_client import Gauge, CollectorRegistry, generate_latest
import os
from flask import Flask
import socket
import daemon
from config import resource_name, service_name
import argparse
app = Flask(__name__)
host_name = socket.gethostname()


def get_machine_cpu():
    import psutil
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    print(f'{cpu}')


@app.route('/about')
def about():
    return "metric_collector for vm\n", 200


@app.route('/metric/redis')
def get_redis():
    from module.redis import get_redis_metric
    
    ret_val = get_redis_metric(resource_name=resource_name, host_name=host_name)
    
    if len(ret_val) > 0:
        return "\n".join(ret_val), 200
    return "empty data", 500

@app.route('/metric/mongodb')
def get_mongodb():
    from module.mongodb import get_mongo_metrics
    ret_val = get_mongo_metrics(resource_name=resource_name, service_name=service_name, host_name=host_name)
    
    if len(ret_val) > 0:
        return "\n".join(ret_val), 200
    
    return "empty data", 500


@app.route('/metric/docker')
def view_docker_ps_cnt():
    import subprocess
    keys = {"azure_vm_docker_count": {"instance": "", "metric": "docker_count", "resource": resource_name, "service": service_name}}
    metric_num = subprocess.check_output("/usr/bin/ps -adef|/usr/bin/grep 'docker run'|/usr/bin/grep -Ewv 'ps|grep'|/usr/bin/wc -l", shell=True, text=True)
    registry = CollectorRegistry()
    
    label = keys["azure_vm_docker_count"]
    label["instance"] = host_name
    gauge = Gauge("azure_vm_docker_count", "azure_vm_docker_count", label.keys(), registry=registry)
    label_values = label.values()
    gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    
    return metric.decode('utf-8'), 200


@app.route('/metric/containerd')
def view_containerd_cnt():
    import subprocess
    cmd = "/usr/bin/ps -adef|/usr/bin/grep 'containerd-shim-runc-v2'|/usr/bin/grep -v 'grep'|/usr/bin/wc -l"
    keys = {"azure_vm_containerd_count": {"instance": "", "metric": "containerd_count", "resource": resource_name, "service": service_name}}
    metric_num = subprocess.check_output(cmd, shell=True, text=True)
    registry = CollectorRegistry()
    label = keys["azure_vm_containerd_count"]
    label["instance"] = host_name
    gauge = Gauge("azure_vm_containerd_count", "azure_vm_containerd_count", label.keys(), registry=registry)
    label_values = label.values()
    gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    
    return metric.decode('utf-8'), 200


@app.route('/metric/docker-abnormal')
def view_docker_ps_abnormal_cnt():
    import subprocess
    keys = {"azure_vm_docker_abnormal_count": {"instance": "", "metric": "docker_abnormal_count", "resource": resource_name, "service": service_name}}
    cmd = "/usr/bin/docker ps --filter=status=exited --filter=status=created |/usr/bin/wc -l"
    metric_num = subprocess.check_output(cmd, shell=True, text=True)
    registry = CollectorRegistry()
    label = keys["azure_vm_docker_abnormal_count"]
    label["instance"] = host_name
    gauge = Gauge("azure_vm_docker_abnormal_count", "azure_vm_docker_abnormal_count", label.keys(), registry=registry)
    label_values = label.values()
    gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    
    return metric.decode('utf-8'), 200


@app.route('/metric/process')
def view_process_cnt():
    import subprocess
    keys = {"azure_vm_process_count": {"instance": "", "metric": "process_count", "resource": resource_name, "service": service_name}}
    metric_num = subprocess.check_output("/usr/bin/ps -adef|/usr/bin/grep -Ewv 'ps |grep' |/usr/bin/wc -l", shell=True, text=True)
    registry = CollectorRegistry()
    
    label = keys["azure_vm_process_count"]
    label["instance"] = host_name
    gauge = Gauge("azure_vm_process_count", "azure_vm_process_count", label.keys(), registry=registry)
    label_values = label.values()
    gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    
    return metric.decode('utf-8'), 200


def get_folder_count(pid: str) -> int:
    path = f"/proc/{pid}/fd"
    folder_count = sum([len(folder) for r, d, folder in os.walk(path)])
    return folder_count


def get_fd_cnt_by_ps():
    import subprocess
    cmd = "/usr/bin/ps -adef|/usr/bin/grep -Ewv 'grep|ps '|/usr/bin/awk '{print $2}'"
    pids_str = subprocess.check_output(cmd, shell=True, text=True)
    pids = pids_str.split("\n")
    folder_num = 0
    for pid in pids:
        if len(pid) > 0 and pid.isdecimal():
            folder_num += get_folder_count(pid)
    
    return folder_num


def get_fd_cnt_by_lsof():
    import subprocess
    return subprocess.check_output("/usr/bin/lsof|/usr/bin/grep -Ewv 'grep|lsof'|/usr/bin/wc -l", shell=True, text=True)


def view_fd_internal(cmd_type: int):
    keys = {"azure_vm_opened_fd_count": {"instance": "", "metric": "opened_fd_count", "resource": resource_name, "service": service_name, "cmd_type": cmd_type}}
    
    if cmd_type == 1:
        metric_num = get_fd_cnt_by_lsof()
    else:
        metric_num = get_fd_cnt_by_ps()
    
    registry = CollectorRegistry()
    
    label = keys["azure_vm_opened_fd_count"]
    label["instance"] = host_name
    gauge = Gauge("azure_vm_opened_fd_count", "azure_vm_opened_fd_count", label.keys(), registry=registry)
    label_values = label.values()
    gauge.labels(*label_values).set(metric_num)
    metric = generate_latest(registry=registry)
    
    return metric.decode('utf-8'), 200


@app.route('/metric/fd/<cmd_type>')
def view_fd(cmd_type: int):
    try:
        return view_fd_internal(cmd_type)
    except Exception as e:
        return str(e), 500


@app.route('/metric/fd')
def view_fd_default():
    try:
        return view_fd_internal(2)
    except Exception as e:
        return str(e), 500


def generate_registry(datas, keys):
    registry = CollectorRegistry()
    
    for key in keys.keys():
        label = keys[key]
        label["instance"] = host_name
        metric_num = datas[key]
        gauge = Gauge(key, key, label.keys(), registry=registry)
        label_values = label.values()
        gauge.labels(*label_values).set(metric_num)
    return registry


def get_mongostat():
    from pymongo import MongoClient
    uri = "mongodb://admin1:bluewhale0321!@dev-db-vm01.koreacentral.cloudapp.azure.com:37027,dev-db-vm02.koreacentral.cloudapp.azure.com:37027"
    client = MongoClient(uri)
    client.get_database('admin').command('serverStatus')


@app.route('/metric/cpu')
def view_cpu():
    import psutil
    keys = {"azure_vm_cpu_percent": {"instance": "", "metric": "cpu_percent", "resource": resource_name, "service": service_name}}
    
    metrics = []
    
    datas = {"azure_vm_cpu_percent": psutil.cpu_percent()}
    
    registry = generate_registry(datas=datas, keys=keys)
    metric = generate_latest(registry=registry)
    metrics.append(metric.decode('utf-8'))
    
    metric_str = "\n".join(metrics)
    return metric_str, 200


@app.route('/metric/disk')
def view_disk():
    import psutil
    
    keys = {"azure_vm_disk_total": {"instance": "", "device": "", "metric": "disk_total", "resource": resource_name, "service": service_name},
            "azure_vm_disk_used": {"instance": "", "device": "", "metric": "disk_used", "resource": resource_name, "service": service_name},
            "azure_vm_disk_used_percent": {"instance": "", "device": "", "metric": "disk_used_percent", "resource": resource_name, "service": service_name}}
    
    metrics = []
    
    for disk in psutil.disk_partitions():
        if disk.fstype and 'loop' not in disk.device:
            registry = CollectorRegistry()
            total = round(int(psutil.disk_usage(disk.mountpoint).total) / (1024.0 ** 3), 4)
            used = round(int(psutil.disk_usage(disk.mountpoint).used) / (1024.0 ** 3), 4)
            used_percent = (used / total) * 100
            
            datas = {"azure_vm_disk_total": total,
                     "azure_vm_disk_used": used,
                     "azure_vm_disk_used_percent": used_percent}
            for key in keys.keys():
                label = keys[key]
                label["instance"] = host_name
                label["device"] = disk.device
                metric_num = datas[key]
                gauge = Gauge(key, key, label.keys(), registry=registry)
                label_values = label.values()
                gauge.labels(*label_values).set(metric_num)
            metric = generate_latest(registry=registry)
            metrics.append(metric.decode('utf-8'))
    
    metric_str = "\n".join(metrics)
    return metric_str, 200


@app.route('/metric/memory')
def view_memory():
    import psutil
    
    keys = {"azure_vm_mem_total": {"instance": "", "metric": "mem_total", "resource": resource_name, "service": service_name},
            "azure_vm_mem_used": {"instance": "", "metric": "mem_used", "resource": resource_name, "service": service_name},
            "azure_vm_mem_used_percent": {"instance": "", "metric": "mem_used_percent", "resource": resource_name, "service": service_name}}
    
    mem = psutil.virtual_memory()
    # total=950054912, available=117116928, percent=87.7, used=675012608, free=68538368
    # print(f'{mem.total}, {mem.available}, {mem.free}, {mem.used}')
    
    metrics = []
    
    total = mem.total
    used = mem.used
    used_percent = (used / total) * 100
    
    datas = {"azure_vm_mem_total": total,
             "azure_vm_mem_used": used,
             "azure_vm_mem_used_percent": used_percent}
    
    registry = generate_registry(datas=datas, keys=keys)
    
    metric = generate_latest(registry=registry)
    metrics.append(metric.decode('utf-8'))
    
    metric_str = "\n".join(metrics)
    return metric_str, 200


def main():
    app.run(host="0.0.0.0", port=5001)


if __name__ == '__main__':
    file_name = f'python {__name__}'
    parser = argparse.ArgumentParser(
        prog=file_name,
        description='collect the system metrics')
    parser.add_argument('-d', '--daemon', type=int, default=1,
                        help='An integer which means daemon or not. Default values is 1.')
    parser.add_argument('-c', '--redis_cron', type=int, default=0,
                        help='An integer which means to use cron daemon. Default values is 0.')
    args = parser.parse_args()
    
    if args.redis_cron == 1:
        from module.redis import init_redis_cron_lock
        init_redis_cron_lock()
    
    if args.daemon == 1:
        with daemon.DaemonContext():
            main()
    else:
        main()

    if args.redis_cron == 1:
        from module.redis import fint_redis_cron_lock
        fint_redis_cron_lock()
