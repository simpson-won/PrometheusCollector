from multiprocessing.managers import SyncManager

from prometheus_client import CollectorRegistry, Gauge, generate_latest

sync_manager: SyncManager = None

mongo_metric_dict = {}


class SyncManager(SyncManager):
    pass


syncdict = {}


def get_dict():
    return syncdict


def init_redis_cron_lock():
    global sync_manager
    from lib.syncmanager import init_redis_cron_lock_4_server
    sync_manager = init_redis_cron_lock_4_server(name="syncdict", get_dict=get_dict)


def fint_redis_cron_lock():
    from lib.syncmanager import fint_redis_cron_lock
    fint_redis_cron_lock()


decimal_degree = {
    'K': 3,
    'M': 6,
    'G': 9,
    'T': 12,
    'P': 15,
    'E': 18,
    'Z': 21,
    'Y': 24,
}


def text_to_num(text):
    if len(text) == 0 or text == " ":
        return 0
    elif text[-1] =="B":
        return int(text[:-1])
    elif text[-1] in decimal_degree:
        num, magnitude = text[:-1], text[-1]
        return float(num) * 10 ** decimal_degree[magnitude]
    elif text[-1] == "%":
        return float(text[:-1])
    else:
        if text[0].isalpha() and text[-1].isalpha():
            return None
        if "." in text:
            return float(text)
        else:
            return int(text)


def get_redis_metric(resource_name: str, host_name: str) -> list:
    metrics = []
    ayncdict_local = sync_manager.syncdict()

    for key in ayncdict_local.keys():
        metric = ayncdict_local.get(key)
        key_vals = {
            "redis_info":
                [{"instance": "", "metric": "io_threads_active", "resource": resource_name, "service": key}, metric['io_threads_active']],
            "redis_info": [
                {"instance": "", "metric": "connected_clients", "resource": resource_name, "service": key}, metric['connected_clients']],
            "redis_info": [
                {"instance": "", "metric": "maxclients", "resource": resource_name, "service": key}, metric['maxclients']],
            "redis_info": [
                {"instance": "", "metric": "client_recent_max_input_buffer", "resource": resource_name, "service": key}, metric['client_recent_max_input_buffer']],
            "redis_info": [
                {"instance": "", "metric": "client_recent_max_output_buffer", "resource": resource_name, "service": key}, metric['client_recent_max_output_buffer']],
            "redis_info": [
                {"instance": "", "metric": "blocked_clients", "resource": resource_name, "service": key}, metric['blocked_clients']],
            "redis_info": [
                {"instance": "", "metric": "tracking_clients", "resource": resource_name, "service": key}, metric['tracking_clients']],
            "redis_info": [
                {"instance": "", "metric": "clients_in_timeout_table", "resource": resource_name, "service": key}, metric['clients_in_timeout_table']],
            "redis_info": [
                {"instance": "", "metric": "used_memory", "resource": resource_name, "service": key}, metric['used_memory']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_human", "resource": resource_name, "service": key}, metric['used_memory_human']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_rss", "resource": resource_name, "service": key}, metric['used_memory_rss']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_rss_human", "resource": resource_name, "service": key}, metric['used_memory_rss_human']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_peak", "resource": resource_name, "service": key}, metric['used_memory_peak']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_peak_human", "resource": resource_name, "service": key}, metric['used_memory_peak_human']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_peak_perc", "resource": resource_name, "service": key}, metric['used_memory_peak_perc']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_overhead", "resource": resource_name, "service": key}, metric['used_memory_overhead']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_dataset", "resource": resource_name, "service": key}, metric['used_memory_dataset']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_dataset_perc", "resource": resource_name, "service": key}, metric['used_memory_dataset_perc']],
            "redis_info": [
                {"instance": "", "metric": "allocator_allocated", "resource": resource_name, "service": key}, metric['allocator_allocated']],
            "redis_info": [{"instance": "", "metric": "allocator_active", "resource": resource_name, "service": key}, metric['allocator_active']],
            "redis_info": [{"instance": "", "metric": "allocator_resident", "resource": resource_name, "service": key}, metric['allocator_resident']],
            "redis_info": [
                {"instance": "", "metric": "total_system_memory", "resource": resource_name, "service": key}, metric['total_system_memory']],
            "redis_info": [
                {"instance": "", "metric": "total_system_memory_human", "resource": resource_name, "service": key}, metric['total_system_memory_human']],
            "redis_info": [
                {"instance": "", "metric": "used_memory_lua", "resource": resource_name, "service": key}, metric['used_memory_lua']],
            "redis_info": [
                {"instance": "", "metric": "maxmemory", "resource": resource_name, "service": key}, metric['maxmemory']],
            "redis_info": [
                {"instance": "", "metric": "maxmemory_human", "resource": resource_name, "service": key}, metric['maxmemory_human']],
            "redis_info": [
                {"instance": "", "metric": "active_defrag_running", "resource": resource_name, "service": key}, metric['active_defrag_running']],
            "redis_info": [
                {"instance": "", "metric": "lazyfree_pending_objects", "resource": resource_name, "service": key}, metric['lazyfree_pending_objects']],
            "redis_info": [
                {"instance": "", "metric": "loading", "resource": resource_name, "service": key}, metric['loading']],
            "redis_info": [
                {"instance": "", "metric": "current_fork_perc", "resource": resource_name, "service": key}, metric['current_fork_perc']],
            "redis_info":
                [{"instance": "", "metric": "current_save_keys_processed", "resource": resource_name, "service": key}, metric['current_save_keys_processed']],
            "redis_info":
                [{"instance": "", "metric": "current_save_keys_total", "resource": resource_name, "service": key}, metric['current_save_keys_total']],
            "redis_info":
                [{"instance": "", "metric": "total_connections_received", "resource": resource_name, "service": key}, metric['total_connections_received']],
            "redis_info":
                [{"instance": "", "metric": "total_commands_processed", "resource": resource_name, "service": key}, metric['total_commands_processed']],
            "redis_info":
                [{"instance": "", "metric": "total_net_input_bytes", "resource": resource_name, "service": key}, metric['total_net_input_bytes']],
            "redis_info":
                [{"instance": "", "metric": "total_net_output_bytes", "resource": resource_name, "service": key}, metric['total_net_output_bytes']],
            "redis_info":
                [{"instance": "", "metric": "instantaneous_input_kbps", "resource": resource_name, "service": key}, metric['instantaneous_input_kbps']],
            "redis_info":
                [{"instance": "", "metric": "instantaneous_output_kbps", "resource": resource_name, "service": key}, metric['instantaneous_output_kbps']],
            "redis_info":
                [{"instance": "", "metric": "expired_keys", "resource": resource_name, "service": key}, metric['expired_keys']],
            "redis_info":
                [{"instance": "", "metric": "keyspace_hits", "resource": resource_name, "service": key}, metric['keyspace_hits']],
            "redis_info":
                [{"instance": "", "metric": "keyspace_misses", "resource": resource_name, "service": key}, metric['keyspace_misses']],
            "redis_info":
                [{"instance": "", "metric": "latest_fork_usec", "resource": resource_name, "service": key}, metric['latest_fork_usec']],
            "redis_info":
                [{"instance": "", "metric": "total_forks", "resource": resource_name, "service": key}, metric['total_forks']],
            "redis_info":
                [{"instance": "", "metric": "total_reads_processed", "resource": resource_name, "service": key}, metric['total_reads_processed']],
            "redis_info":
                [{"instance": "", "metric": "total_writes_processed", "resource": resource_name, "service": key}, metric['total_writes_processed']],
            "redis_info":
                [{"instance": "", "metric": "reply_buffer_shrinks", "resource": resource_name, "service": key}, metric['reply_buffer_shrinks']],
            "redis_info":
                [{"instance": "", "metric": "role", "resource": resource_name, "service": key}, metric['role']=='master'],
            "redis_info":
                [{"instance": "", "metric": "repl_backlog_size", "resource": resource_name, "service": key}, metric['repl_backlog_size']],
            "redis_info":
                [{"instance": "", "metric": "used_cpu_sys", "resource": resource_name, "service": key}, metric['used_cpu_sys']],
            "redis_info":
                [{"instance": "", "metric": "used_cpu_user", "resource": resource_name, "service": key}, metric['used_cpu_user']],
            "redis_info":
                [{"instance": "", "metric": "used_cpu_sys_children", "resource": resource_name, "service": key}, metric['used_cpu_sys_children']],
            "redis_info":
                [{"instance": "", "metric": "used_cpu_user_children", "resource": resource_name, "service": key}, metric['used_cpu_user_children']],
            "redis_info":
                [{"instance": "", "metric": "used_cpu_sys_children", "resource": resource_name, "service": key}, metric['used_cpu_sys_children']],
        }
        for metric_key in key_vals.keys():
            registry = CollectorRegistry()
    
            label = key_vals[metric_key][0]
            label["instance"] = host_name
            metric_num = key_vals[metric_key][1]
            gauge = Gauge(metric_key, metric_key, label.keys(), registry=registry)
            label_values = label.values()
            
            if type(metric_num) == str:
                metric_num = text_to_num(metric_num)

            gauge.labels(*label_values).set(metric_num)
            metric = generate_latest(registry=registry)
            metrics.append(metric.decode('utf-8'))
    
    return metrics
