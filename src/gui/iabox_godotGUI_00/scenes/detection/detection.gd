extends Node

var state = "idle"
var http
var image = Image.new()
var success_text = ""

func _on_home_button_pressed():
	print("Home button pressed")
	get_tree().change_scene_to_file("res://scenes/home/home.tscn")

func keys_in_dict(keys,dict) -> bool:
	for key in keys:
		if not dict.has(key):
			return false
	return true
	
func format_time(t:String) -> String:
	var ts = t.split(":")
	if 3==len(ts):
		var hour = int(ts[0])
		var min = int(ts[1])
		var sec = int(float(ts[2]))
		var res = ""
		if 0 != hour:
			res = String(hour)+"h "
		if 0 != min:
			res = res + String(min) + "min "
		if 0 != sec:
			res = res + String(sec) + "s"
		if "" == res:
			res="0s"
		return res
	else:
		return t
			
		
	

func _http_request_completed(result,response_code,headers,body):
	if "Interrogate AI box" == state:
		if response_code == 200:
			# Decode the JSON response
			var json = JSON.parse_string(body.get_string_from_utf8())
			if json != null and keys_in_dict(["name", "path", "place", "time"],json):
				var l_time = format_time(json["time"])
				# To always see a result for dev comment the following line and uncomment the next one
				if "" != json["path"]:
				#if "" == json["path"]:
					success_text = "LUNETTES détectées dans la pièce " + json["place"] + " à " + l_time
					%ErrorSuccessLabel.text = success_text
					# TODO change here to have the image from path
					var url = "http://" + Global.ai_box_ip_address + json["path"] #"/img_found" 
					state = "Get image"
					var response = http.request(url, ['accept: application/json'], HTTPClient.METHOD_GET)
					if response != OK:
						push_error("An error occured in the HTTP request to get the image")
						%ErrorSuccessLabel.text="ERREUR : Impossible de récupérer l'image"
				else:
					%ErrorSuccessLabel.text="ÉCHEC: aucune paire de lunettes détectée !"
					%ImageTextureRect.texture = load("res://scenes/images/no_glasses_360x360.png")
			else:
				print("Error in the JSON response")
				%ErrorSuccessLabel.text="ERREUR : Erreur dans la réponse JSON"
		else:
			push_error("An error occured in the HTTP request to get found detections")
			%ErrorSuccessLabel.text="ERREUR : Impossible de récupérer les détections.\nLa requête HTTP a échouée, vérifier que l'adresse IP de la box IA est correcte\net que le backend est opérationnel."
	elif "Get image" == state:
		if response_code == 200:
			%ErrorSuccessLabel.text="SUCCÈS : Image récupérée"
			var image_error = image.load_jpg_from_buffer(body)
			if OK != image_error:
				print("Error while displaying the image")
				%ErrorSuccessLabel.text="ERREUR : Erreur lors de l'affichage de l'image"
			else:
				print("Image loaded: image size: " + str(image.get_width()) + "x" + str(image.get_height()))
				var max_width = 800
				if max_width < image.get_width():
					print("Resize image")
					var scale = max_width / float(image.get_width())
					var new_height = int(scale*float(image.get_height()))
					print("New image size: " + str(max_width) + "x" + str(new_height))
					image.resize(max_width,new_height,4)
				#image.save_png("/tmp/detection_image.png")
				var new_texture = ImageTexture.create_from_image(image)
				#%ImageTextureRect.texture = load("/tmp/detection_image.png")
				%ImageTextureRect.texture = new_texture
				%ErrorSuccessLabel.text=success_text
		else:
			push_error("An error occured in the HTTP request to get the image")
			%ErrorSuccessLabel.text="ERREUR : Impossible de récupérer l'image"
		state = "idle"

func interrogate_ai_box():
	success_text = ""
	http.request_completed.connect(self._http_request_completed)
	state = "Interrogate AI box"
	%ErrorSuccessLabel.text="Interrogation de la box IA ..."
	%ImageTextureRect.texture = load("res://scenes/images/loading.jpg")
	if "" != Global.ai_box_ip_address:
		var url = "http://" + Global.ai_box_ip_address + "/found"
		var headers = ['Content-Type: application/json', 'Accept: application/json']
		print("Get found detections via api call: " + url)
		var response = http.request(url, headers, HTTPClient.METHOD_GET)
		if response != OK:
			push_error("An error occured in the HTTP request to get found detections")
			%ErrorSuccessLabel.text="ERREUR : Impossible de récupérer les détections.\nLa requête HTTP a échouée, vérifier que l'adresse IP de la box IA est correcte\net que le backend est opérationnel."
	else:
		%ErrorSuccessLabel.text="ERREUR : Adresse IP de la box IA non configurée !"

# Called when the node enters the scene tree for the first time.
func _ready():
	http = HTTPRequest.new()
	add_child(http)
	interrogate_ai_box()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_search_again_button_pressed():
	interrogate_ai_box()
