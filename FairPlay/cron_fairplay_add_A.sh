#!/bin/bash
(crontab -r)
(crontab -l;echo '0 0 * * * /bin/find /var/log/httpd/ -name "*log*" -mtime +14 -exec gzip -9 {} \;') | crontab -
(crontab -l;echo '0 0 * * * /bin/find /var/log/httpd/ -mtime +90 -exec rm -rf {} \;') | crontab -
(crontab -l;echo '25 1 * * * /opt/googleapis/bin/prepare_chk.sh') | crontab -
(crontab -l;echo '30 1 * * * /opt/googleapis/bin/start_chk.sh') | crontab -
(crontab -l;echo '40 1 * * * /opt/googleapis/bin/sum_total.sh') | crontab -
(crontab -l;echo '50 1 * * * /opt/googleapis/bin/total_start.sh') | crontab -
