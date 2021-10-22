#!/bin/bash

echo "[Unit]
Description=PyPiManager
Wants=network-online.target
After=network-online.target

[Service]
User=root
Group=root
Restart=on-failure
ExecStart=/usr/local/bin/python /home/pypimanager_backend/manager.py

[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/pypimanager.service

systemctl daemon-reload
systemctl enable pypimanager
systemctl start pypimanager
