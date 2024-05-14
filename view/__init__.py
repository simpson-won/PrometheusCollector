from view.allview import about
from view.allview import get_mysql
from view.allview import get_redis
from view.allview import get_mongodb
from view.allview import view_docker_ps_cnt
from view.allview import view_containerd_cnt
from view.allview import view_docker_ps_abnormal_cnt
from view.allview import view_process_cnt
from view.allview import view_fd, view_fd_default
from view.allview import view_cpu, view_disk, view_memory

from collector import app


app.add_url_rule('/about', view_func=about)
app.add_url_rule('/metric/mysql/<str:db_name>/<str:table_name>', 'get_mysql', view_func=get_mysql)
app.add_url_rule('/metric/redis', view_func=get_redis)
app.add_url_rule('/metric/mongodb', view_func=get_mongodb)
app.add_url_rule('/metric/docker', view_func=view_docker_ps_cnt)
app.add_url_rule('/metric/containerd', view_func=view_containerd_cnt)
app.add_url_rule('/metric/docker-abnormal', view_func=view_docker_ps_abnormal_cnt)
app.add_url_rule('/metric/process', view_func=view_process_cnt)
app.add_url_rule('/metric/fd/<cmd_type>', view_func=view_fd)
app.add_url_rule('/metric/fd', view_func=view_fd_default)
app.add_url_rule('/metric/cpu', view_func=view_cpu)
app.add_url_rule('/metric/disk', view_func=view_disk)
app.add_url_rule('/metric/memory', view_func=view_memory)
