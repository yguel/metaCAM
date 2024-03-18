extends Node

var ai_box_ip_address : String = ""

# Returns True if the box address if of the form ip:port or ip, False otherwise.
static func check_box_address(addr : String) -> bool:
	var valid = false
	var l = addr.split(":")
	if 2 == l.size():
		var ip = l[0]
		var port = l[1]
		if port.to_int() >= 0 and port.to_int() <= 65535:
			return check_ip_address(ip)
	elif 1 == l.size():
		return check_ip_address(l[0])
	return false

# Returns True if the IP address is valid, False otherwise.
static func check_ip_address(ip : String) -> bool:
	var valid = false
	var octets = ip.split(".")
	if 4 == octets.size() or 6 == octets.size():
		# Check for IPV4 and IPV6 address
		for octet in octets:
			if octet.to_int() < 0 or octet.to_int() > 255:
				return false
	else:
		return false
	return true

# Returns True if the mac address is valid, False otherwise.
static func check_mac_address(mac : String) -> bool:
	var valid = false
	var octets = mac.split(":")
	if 6 == octets.size():
		for octet in octets:
			# Check if octet is composed of hex digits
			for c in octet:
				if not c in "0123456789abcdefABCDEF":
					return false
			if octet.to_int() < 0 or octet.to_int() > 255:
				return false
	else:
		return false
	return true
	
