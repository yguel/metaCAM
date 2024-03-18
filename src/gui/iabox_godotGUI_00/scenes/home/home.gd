extends Control

func _on_launch_detect_button_pressed():
	print("Launch detection button pressed")
	get_tree().change_scene_to_file("res://scenes/detection/detection.tscn")
	pass

func _on_add_camera_button_pressed():
	print("Add camera button pressed")
	get_tree().change_scene_to_file("res://scenes/add_camera/add_camera.tscn")
	pass
	
func _on_config_button_pressed():
	print("Config button pressed")
	get_tree().change_scene_to_file("res://scenes/config/config.tscn")
	pass

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass
