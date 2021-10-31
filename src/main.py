
import web_server as ws
import tcp_server as ts
import settings as s

import subprocess

def launch_server_process(server, host, port):
    cmd = f"python {server}.py '{host}' '{port}'"
    return subprocess.Popen(cmd, shell=True, executable='/bin/bash', start_new_session=True)

if __name__ == "__main__":
    launch_server_process(
        "tcp_server", s.get_host_tcp_server(), s.get_port_tcp_server())
    # launch_server_process(
    #     "web_server", s.get_host_web_server(), s.get_port_web_server())