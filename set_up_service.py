#!/usr/bin/env python3

import os
import sys

def create_service_file(service_name, working_directory, username="root"):
    service_content = f"""[Unit]
Description={service_name} service
Requires=docker.service
After=docker.service

[Service]
User={username}
Group={username}
Restart=always
WorkingDirectory={working_directory}
ExecStartPre=-/usr/bin/docker compose down
ExecStart=/usr/bin/docker compose up --build
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
"""

    with open(f"/etc/systemd/system/{service_name}.service", "w") as f:
        f.write(service_content)

    print(f"Service file for {service_name} has been created!")

    os.system(f"systemctl daemon-reload")
    os.system(f"systemctl start {service_name}")
    os.system(f"systemctl enable {service_name}")
    os.system(f"systemctl status {service_name}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: set_up_service.py <service_name> <working_directory> [username]")
        sys.exit(1)

    service_name = sys.argv[1]
    working_directory = sys.argv[2]
    username = sys.argv[3] if len(sys.argv) > 3 else "root"

    create_service_file(service_name, working_directory, username)
