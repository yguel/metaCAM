extends Node

func _on_home_button_pressed():
	print("Home button pressed")
	get_tree().change_scene_to_file("res://scenes/home/home.tscn")

func _on_modify_ip_button_pressed():
	var addr = %NewIPboxLineEdit.text
	if Global.check_box_address(addr):
		Global.ai_box_ip_address = addr
		%IPboxStatusLabel.text = "Adresse IP courante de la box IA: " + Global.ai_box_ip_address
	pass

# Called when the node enters the scene tree for the first time.
func _ready():
	if "" == Global.ai_box_ip_address :
		%IPboxStatusLabel.text = "Adresse IP de la box IA INCONNUE"
	else:
		%IPboxStatusLabel.text = "Adresse IP courante de la box IA: " + Global.ai_box_ip_address
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
