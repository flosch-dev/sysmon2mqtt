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


def mqtt_publish(topic,payload):
    """ function to send MQTT message """
    try:
        mqttclient.publish(
                      topic,
                      payload=payload,
                      qos=0,
                      retain=False)
    except:
        print('fehler')

def mqtt_connect():
    mqttclient = mqtt.Client(MQTT_CLIENT_ID)
    try:
        mqttclient.connect(MQTT_HOST, port=MQTT_PORT, keepalive=60)
        mqttclient.loop_start()
        break
    except:
        print("MQTT connection error")
        exit(1)

def publish_sysmon():
    mqtt_publish('SYSMON/CPU/cpu_load5',os.getloadavg()[1])
    mqtt_publish('SYSMON/CPU/cpu_count',os.cpu_count())
    mqtt_publish('SYSMON/CPU/cpu_util',round(os.getloadavg()[1] * 100 / os.cpu_count(),2))
    mqtt_publish('SYSMON/RAM/ram_avail',int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()))
    mqtt_publish('SYSMON/RAM/ram_total',int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()))
    mqtt_publish('SYSMON/RAM/ram_used',int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()) - int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()))
    mqtt_publish('SYSMON/RAM/ram_util',round(100 - int(os.popen('cat /proc/meminfo | grep MemAvailable | awk \'{print $2}\'').read()) * 100 / int(os.popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'').read()),2))
    mqtt_publish('SYSMON/PROCESS/process_count',int(os.popen('ps aux | grep -v "ps aux" | wc -l').read()))
    mqtt_publish('SYSMON/SYSTEM/uptime',os.popen('uptime -p').read().rstrip())
    mqtt_publish('SYSMON/SYSTEM/hostname',os.popen('hostname').read().rstrip())
    mqtt_publish('SYSMON/SYSTEM/os_version',os.popen('grep PRETTY_NAME /etc/os-release | cut -d "\\"" -f 2').read().rstrip())
    mqtt_publish('SYSMON/SYSTEM/rpi_model',os.popen('cat /proc/device-tree/model').read().rstrip())


def main():
    mqtt_connect()
    mqttclient.on_connect = publish_sysmon()
    mqttclient.disconnect()

if __name__=="__main__":
   main()
