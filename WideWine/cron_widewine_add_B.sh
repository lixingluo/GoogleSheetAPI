#!/bin/bash
(crontab -r)
echo '0 0 * * * /bin/find /var/log/tomcat8/ -name "*.log" -mtime +14 -exec gzip -9 {} \;' >> /var/spool/cron/root
echo '0 0 * * * /bin/find /var/log/tomcat8/ -name "*.txt" -mtime +14 -exec gzip -9 {} \;' >> /var/spool/cron/root
echo '0 0 * * * /bin/find /var/log/tomcat8/ -mtime +90 -exec rm -rf {} \;' >> /var/spool/cron/root
echo '35 1 * * * /opt/googleapis/bin/start_chk.sh' >> /var/spool/cron/root

