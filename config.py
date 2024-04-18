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
half_minute_task = "els_alarm"
redis_hosts = ":tester:20.41.87.218:6379"
redis_use_ssl = False
els_address = "http://localhost:9200"
slack_token = "xoxb-48801426293-6967870596406-uoCVZxYd6h45xw97IgYnf0RG"
slack_channel_name = "alpha-eimmo"
