# -*- coding: utf-8 -*-
import netifaces as ni
import ipaddress
import subprocess

#Pour récupérer l'adresse IP de notre Jetson sur la bonne interface
def get_eth0_ip():
    try:
        interfaces = ni.interfaces()
        for interface in interfaces:
            if interface == 'eth0':
                addresses = ni.ifaddresses(interface)
                if ni.AF_INET in addresses:
                    eth0_ip = addresses[ni.AF_INET][0]['addr']
                    return eth0_ip
        return None
    except Exception as e:
        print("Une erreur s'est produite :", e)
        return None

# if __name__ == "__main__":
