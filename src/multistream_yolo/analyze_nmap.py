# coding=utf-8
import camera_database

def extract_ip_from_file(mac_address):
    with open('nmap_output.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if mac_address in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    return parts[0]
    return None

if __name__ == "__main__":
    mac_list = camera_database.get_all_mac_address()
    
    for mac in mac_list:
        #Adresse MAC sans majuscule
        ip = extract_ip_from_file(mac.lower())
        if ip is None:
            camera_database.set_camera_offline(mac)
            continue
        camera_database.update_mac_ip_address(mac,ip)
