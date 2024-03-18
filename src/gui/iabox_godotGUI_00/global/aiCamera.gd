extends Node

class_name AIcamera
var global = preload("res://global/global.gd")

var device_name = null : set = _set_device_name, get = _get_device_name
var device_location = null : set = _set_device_location, get = _get_device_location
var mac_address = null : set = _set_mac_address, get = _get_mac_address
var ip_address = null : set = _set_ip_address, get = _get_ip_address

func _set_device_name(name : String):
	device_name = name

func _get_device_name():
	return device_name

func _set_device_location(location : String):
	device_location = location

func _get_device_location():
	return device_location

func _set_mac_address(mac : String):
	#Check if mac address is valid
	if false == global.check_mac_address(mac):
		print("Invalid MAC address")
		return
	else:
		mac_address = mac

func _get_mac_address():
	return mac_address

func _set_ip_address(ip : String):
	var valid = false
	#Check if ip address is valid
	valid = global.check_ip_address(ip)
	if valid == false:
		print("Invalid IP address")
		return
	else:
		ip_address = ip

func _get_ip_address():
	return ip_address

func to_dict():
	var dict = {}
	dict["name"] = device_name
	dict["place"] = device_location
	dict["mac_addr"] = mac_address
	dict["ip_addr"] = ip_address
	return dict

#Class Constructor
func _init(d_name : String, location : String, mac : String, ip : String):
	device_name = d_name
	device_location = location
	mac_address = mac
	ip_address = ip

	
