"""
configuration
"""
resource_name = "eimmo-batch-vms"
service_name = "eimmo-batch-vms-worker3"
zombi_name = "containerd-shim-runc-v2"
check_interval_sec = 120
zombi_log_file = "zombi_kill.log"
mongodb_uri = "mongodb://test:tester@localhost:37027"
one_minute_task = "redis_metrics"
redis_hosts = ":tester:20.41.87.218:6379"
redis_use_ssl = False
