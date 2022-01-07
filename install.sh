cp -r sense.server.service /etc/systemd/system/
sudo chmod 744 start-service.sh
sudo chmod 664 /etc/systemd/system/sense.server.service

sudo systemctl stop sense.server.service
systemctl disable sense.server.service

systemctl daemon-reload
systemctl enable sense.server.service

sudo systemctl start sense.server.service
sudo systemctl status sense.server.service
