extends CharacterBody2D

signal observed(kind: String, detail: Dictionary)
signal control_requested(action: String)

var episode: Node2D
var settings: Dictionary
var pending: Array[String] = []
var recovery_until: int = 0
var dash_until: int = 0
var health: int = 2
var input_received_count: int = 0
var collision_ticks: int = 0


func configure(owner_episode: Node2D, actor_settings: Dictionary) -> void:
	episode = owner_episode
	settings = actor_settings
	var shape := CircleShape2D.new()
	shape.radius = float(settings.radius_px)
	var collider := CollisionShape2D.new()
	collider.shape = shape
	add_child(collider)
	reset_actor()


func reset_actor() -> void:
	position = Vector2(float(settings.start_px[0]), float(settings.start_px[1]))
	velocity = Vector2.ZERO
	recovery_until = 0
	dash_until = 0
	health = 2


func _input(event: InputEvent) -> void:
	for action: String in ["attack", "dodge", "save", "reset", "load", "interact"]:
		if event.is_action_pressed(action) and not event.is_echo():
			input_received_count += 1
			pending.append(action)
			observed.emit("input_received", {"action": action, "pipeline": "Node._input"})


func _physics_process(delta: float) -> void:
	if episode == null:
		return
	for action: String in pending:
		if action in ["save", "reset", "load", "interact"]:
			control_requested.emit(action)
		elif health <= 0:
			observed.emit("action_rejected", {"action": action, "reason": "incapacitated"})
		elif episode.world_tick < recovery_until:
			observed.emit("action_rejected", {"action": action, "reason": "committed_recovery", "recovery_until": recovery_until})
		elif action == "attack":
			recovery_until = episode.world_tick + int(settings.recovery_ticks)
			observed.emit("attack_started", {"recovery_until": recovery_until, "cancellable": false})
		elif action == "dodge":
			dash_until = episode.world_tick + int(settings.dash_ticks)
			observed.emit("dodge_started", {"dash_until": dash_until})
	pending.clear()
	velocity = Vector2(float(settings.dash_speed_px_per_s), 0) if episode.world_tick < dash_until and health > 0 else Vector2.ZERO
	move_and_slide()
	if get_slide_collision_count() > 0:
		collision_ticks += 1
		var hit := get_slide_collision(0)
		observed.emit("body_collision", {"collider": str(hit.get_collider().name), "x_px": position.x, "y_px": position.y})
	episode.after_player_step(delta)
	queue_redraw()


func snapshot() -> Dictionary:
	return {"id": settings.id, "position_px": [position.x, position.y], "health": health,
		"recovery_until": recovery_until, "dash_until": dash_until}


func restore(data: Dictionary) -> void:
	position = Vector2(float(data.position_px[0]), float(data.position_px[1]))
	health = int(data.health)
	recovery_until = int(data.recovery_until)
	dash_until = int(data.dash_until)
	velocity = Vector2.ZERO


func _draw() -> void:
	if not settings.is_empty():
		draw_circle(Vector2.ZERO, float(settings.radius_px), Color(0.4, 0.9, 0.8) if health > 0 else Color(0.7, 0.2, 0.3))
