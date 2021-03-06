extends KinematicBody2D

export(Vector2) var _Gravity = Vector2(0,900)
export(int) var Jump_Speed = 400
onready var pPos = get_position()
signal Score_Changed(Score)

var score = 0

var force_on_player = Vector2()

func _ready():
	set_physics_process(false)

func _process(delta):
	#if Input.is_action_just_pressed("Player_Jump"):
	if Input.is_mouse_button_pressed(BUTTON_LEFT):
		set_physics_process(true)
		get_parent().get_node("Spawn")._on_Timer_timeout()
		get_parent().get_node("Spawn").start()
		set_process(false)

func _physics_process(delta):
	force_on_player += delta * _Gravity
	#if Input.is_action_just_pressed("Player_Jump"): # and is_Falling():
	if Input.is_mouse_button_pressed(BUTTON_LEFT):
		force_on_player.y = -Jump_Speed
	
	force_on_player = move_and_slide(force_on_player)
	
	pPos = get_position()
	pPos.x = max(0, min(get_viewport_rect().size.x, pPos.x))
	pPos.y = max(0, min(get_viewport_rect().size.y, pPos.y))
	set_position(pPos)

func _on_Tracker_body_exited(body):
	#TODO
	#*bug Can Triger Twice
	if body == self:
		score += 1
		emit_signal("Score_Changed",score)

func is_Falling():
	return pPos.y < get_position().y

