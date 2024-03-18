extends Node

var http

func _on_home_button_pressed():
	print("Home button pressed")
	get_tree().change_scene_to_file("res://scenes/home/home.tscn")

func _on_add_camera_button_pressed():
	print("Add camera button pressed")
	%ErrorSuccessLabel.text = ""
	var cam_name = %CameraNameLineEdit.text
	var location = %CameraLocationLineEdit.text
	var mac = %MacAddressLineEdit.text
	var ip = %IpAddressLineEdit.text 
	var cam = AIcamera.new(cam_name,location,mac,ip)
	if "" != Global.ai_box_ip_address:
		var url = "http://" + Global.ai_box_ip_address + "/new_camera"
		var headers = ['Content-Type: application/json', 'Accept: application/json']
		var body = cam.to_dict()
		print("Add camera " + JSON.stringify(body) + " to url: " + url)
		var response = http.request(url, headers, HTTPClient.METHOD_POST, JSON.stringify(body))
		if response != OK:
			push_error("An error occured in the HTTP request to record a new camera")
			%ErrorSuccessLabel.text="ERREUR lors de l'enregistrement de la camera"

func _http_request_completed(result,response_code,headers,body):
	"""
	var json = JSON.new()
	json.parse(body.get_string_from_utf8())
	var response = json.get_data()
	if null == response:
		%ErrorSuccessLabel.text="ERREUR lors de l'enregistrement de la camera"
	elif "User-Agent" in response.headers:
		print(response.headers["User-Agent"])
	"""

	if 200 != response_code:
		%ErrorSuccessLabel.text="ERREUR lors de l'enregistrement de la camera (code "+ String(response_code) + ")"
	else:
		%ErrorSuccessLabel.text="Caméra enregistrée avec SUCCÈS."


# Called when the node enters the scene tree for the first time.
func _ready():
	http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(self._http_request_completed)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass



