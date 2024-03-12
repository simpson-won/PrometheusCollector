from pymongo import MongoClient
from config import mongodb_uri
from prometheus_client import Gauge, CollectorRegistry, generate_latest


def get_mongo_metrics(resource_name, service_name, host_name):
    client = MongoClient(mongodb_uri)
    
    status = client.get_database('admin').command('serverStatus')
    
    mem_st = status['mem']
    connection_st = status['connections']
    extra_info_st = status['extra_info']
    network_st = status['network']
    opcounters_st = status['opcounters']
    
    key_vals = [
        ["mongodb_mem",
         {"instance": "", "metric": "bits", "resource": resource_name, "service": service_name}, mem_st['bits']],
        ["mongodb_mem",
         {"instance": "", "metric": "resident", "resource": resource_name, "service": service_name}, mem_st['resident']],
        ["mongodb_mem",
         {"instance": "", "metric": "virtual", "resource": resource_name, "service": service_name}, mem_st['virtual']],
        ["mongodb_mem",
         {"instance": "", "metric": "supported", "resource": resource_name, "service": service_name}, mem_st['supported']],
        ["mongodb_connections",
         {"instance": "", "metric": "current", "resource": resource_name, "service": service_name}, connection_st['current']],
        ["mongodb_connections",
         {"instance": "", "metric": "available", "resource": resource_name, "service": service_name}, connection_st['available']],
        ["mongodb_connections",
         {"instance": "", "metric": "totalCreated", "resource": resource_name, "service": service_name}, connection_st['totalCreated']],
        ["mongodb_connections",
         {"instance": "", "metric": "rejected", "resource": resource_name, "service": service_name}, connection_st['rejected']],
        ["mongodb_connections",
         {"instance": "", "metric": "active", "resource": resource_name, "service": service_name}, connection_st['active']],
        ["mongodb_connections",
         {"instance": "", "metric": "threaded", "resource": resource_name, "service": service_name}, connection_st['threaded']],
        ["mongodb_network",
         {"instance": "", "metric": "bytesIn", "resource": resource_name, "service": service_name}, network_st['bytesIn']],
        ["mongodb_network",
         {"instance": "", "metric": "bytesOut", "resource": resource_name, "service": service_name}, network_st['bytesOut']],
        ["mongodb_network",
         {"instance": "", "metric": "physicalBytesIn", "resource": resource_name, "service": service_name}, network_st['physicalBytesIn']],
        ["mongodb_network",
         {"instance": "", "metric": "physicalBytesOut", "resource": resource_name, "service": service_name}, network_st['physicalBytesOut']],
        ["mongodb_network",
         {"instance": "", "metric": "numSlowDNSOperations", "resource": resource_name, "service": service_name}, network_st['numSlowDNSOperations']],
        ["mongodb_network",
         {"instance": "", "metric": "numRequests", "resource": resource_name, "service": service_name}, network_st['numRequests']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "insert", "resource": resource_name, "service": service_name}, opcounters_st['insert']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "query", "resource": resource_name, "service": service_name}, opcounters_st['query']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "update", "resource": resource_name, "service": service_name}, opcounters_st['update']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "delete", "resource": resource_name, "service": service_name}, opcounters_st['delete']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "getmore", "resource": resource_name, "service": service_name}, opcounters_st['getmore']],
        ["mongodb_opcounters",
         {"instance": "", "metric": "command", "resource": resource_name, "service": service_name}, opcounters_st['command']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "user_time_us", "resource": resource_name, "service": service_name}, extra_info_st['user_time_us']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "system_time_us", "resource": resource_name, "service": service_name}, extra_info_st['system_time_us']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "maximum_resident_set_kb", "resource": resource_name, "service": service_name}, extra_info_st['maximum_resident_set_kb']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "input_blocks", "resource": resource_name, "service": service_name}, extra_info_st['input_blocks']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "output_blocks", "resource": resource_name, "service": service_name}, extra_info_st['output_blocks']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "page_reclaims", "resource": resource_name, "service": service_name}, extra_info_st['page_reclaims']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "page_faults", "resource": resource_name, "service": service_name}, extra_info_st['page_faults']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "voluntary_context_switches", "resource": resource_name, "service": service_name},
         extra_info_st['voluntary_context_switches']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "involuntary_context_switches", "resource": resource_name, "service": service_name},
         extra_info_st['involuntary_context_switches']],
        ["mongodb_extra_info",
         {"instance": "", "metric": "threads", "resource": resource_name, "service": service_name}, extra_info_st['threads']],
    ]
    
    metrics = []
    registry = CollectorRegistry()
    
    for key_val in key_vals:
        label = key_val[1]
        label["instance"] = host_name
        metric_num = key_val[2]
        gauge = Gauge(key_val[0], key_val[0], label.keys(), registry=registry)
        label_values = label.values()
        gauge.labels(*label_values).set(metric_num)
        metric = generate_latest(registry=registry)
        metrics.append(metric.decode('utf-8'))
    
    return metrics
