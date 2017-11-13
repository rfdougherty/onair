# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import gc
import network
import webrepl
import machine

machine.freq(160000000)
ssid = 'YOUR_SSID'
pwd = 'YOUR PASSWORD'

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    if sta_if.isconnected():
        network.WLAN(network.AP_IF).active(False)
    else:
        network.WLAN(network.AP_IF).active(True)
    print('network config:', sta_if.ifconfig())

do_connect()
webrepl.start()

gc.collect()
