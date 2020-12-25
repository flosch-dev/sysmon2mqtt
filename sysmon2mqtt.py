#!/usr/bin/python3
"""
simple python3 script to publish system data via MQTT
python3 module required:
# apt install python3-paho-mqtt

to run every 5 min via cron, add the following cronjob:
*/5 * * * * /<path-to-file>/sysmon2mqtt.py
"""

import time
import os
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

""" ---- config -------- """

MQTT_HOST = ''
MQTT_PORT = 1883
MQTT_CLIENT_ID = os.popen('hostname').read().rstrip() + '-system'

""" ---------------------------------"""

auth = {
  'username':"MQTT_USER",
  'password':"MQTT_PASS"
}

def publish_sysmon(mqttclient):
    mqttclient.publish('SYSMON/CPU/cpu_load5',os.getloadavg()[1])
    mqttclient.publish('SYSMON/CPU/cpu_count',os.cpu_count())
    mqttclient.publish('SYSMON/CPU/cpu_util',round(os.getloadavg()[1] * 100 / os.cpu_count(),2))
    mqttclient.publish('SYSMON/RAM/ram_avail',int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()))
    mqttclient.publish('SYSMON/RAM/ram_total',int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()))
    mqttclient.publish('SYSMON/RAM/ram_used',int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()) - int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()))
    mqttclient.publish('SYSMON/RAM/ram_util',round(100 - int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()) * 100 / int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()),2))
    mqttclient.publish('SYSMON/PROCESS/process_count',int(os.popen('ps aux | grep -v "ps aux" | wc -l').read()))
    mqttclient.publish('SYSMON/SYSTEM/uptime',os.popen('uptime -p').read().rstrip())
    mqttclient.publish('SYSMON/SYSTEM/hostname',os.popen('hostname').read().rstrip())
    mqttclient.publish('SYSMON/SYSTEM/os_version',os.popen('grep PRETTY_NAME /etc/os-release | cut -d "\\"" -f 2').read().rstrip())
    mqttclient.publish('SYSMON/SYSTEM/rpi_model',os.popen('cat /proc/device-tree/model').read().rstrip())

def main():
    mqttclient = mqtt.Client(MQTT_CLIENT_ID)
    try:
        mqttclient.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
    except:
        print("MQTT connection error")
        exit(1)
    mqttclient.loop_start()
    publish_sysmon(mqttclient)
    mqttclient.disconnect()

if __name__=="__main__":
   main()
