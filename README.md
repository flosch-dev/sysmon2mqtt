# sysmon2mqtt
simple python3 script to publish system data via MQTT
python3 module required:
```bash
# apt install python3-paho-mqtt
```

to run every 5 min via cron, add the following cronjob:
```bash
*/5 * * * * /<path-to-file>/sysmon2mqtt.py
```
