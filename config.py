"""
configuration
"""
resource_name = "eimmo-batch-vms"
service_name = "eimmo-batch-vms-worker3"
zombi_name = "containerd-shim-runc-v2"
check_interval_sec = 120
zombi_log_file = "zombi_kill.log"
mongodb_uri = "mongodb://admin1:bluewhale0321!@localhost:37027"