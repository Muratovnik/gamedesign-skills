extends Node2D

const SOURCE_PATHS := ["project.godot", "episode.tscn", "episode.gd", "player.gd"]
var fixture: Dictionary
var fixture_path: String = "res://fixtures/candidate.json"
var output_path: String = ""
var save_path: String = ""
var run_id: String = "interactive"
var automatic: bool = true
var run_tick: int = 0
var world_tick: int = 0
var events: Array[Dictionary] = []
var witnesses: Array[Dictionary] = []
var resolved: Array[String] = []
var warned: Array[String] = []
var history: Array[String] = ["archive-message"]
var knowledge: Dictionary = {"bo": ["winch-procedure"], "keeper-ivo": []}
var right_owners: Dictionary = {"winch": "bo", "archive-pass": "ava"}
var save_snapshot: Dictionary = {}
var restored_equal: bool = false
var final_line: String = ""
var completed: bool = false
var first_physics_frame: int = 0
@onready var player: CharacterBody2D = $Player
@onready var camera: Camera2D = $Camera


func _ready() -> void:
	for arg: String in OS.get_cmdline_user_args():
		if arg.begins_with("--fixture="):
			fixture_path = arg.trim_prefix("--fixture=")
		elif arg.begins_with("--output="):
			output_path = arg.trim_prefix("--output=")
		elif arg.begins_with("--run-id="):
			run_id = arg.trim_prefix("--run-id=")
		elif arg == "--interactive":
			automatic = false
	var parsed := JSON.new()
	var error := parsed.parse(FileAccess.get_file_as_string(fixture_path))
	if error != OK or not parsed.data is Dictionary:
		push_error("Fixture JSON could not be parsed.")
		get_tree().quit(2)
		return
	fixture = parsed.data
	if int(fixture.units.tick_rate_hz) != Engine.physics_ticks_per_second:
		push_error("Fixture and engine physics clocks differ.")
		get_tree().quit(2)
		return
	if output_path.is_empty():
		save_path = "user://gate-episode-save.json"
	else:
		save_path = output_path + ".save.json"
	var key_codes := {"attack": KEY_SPACE, "dodge": KEY_D, "interact": KEY_E, "save": KEY_F5, "load": KEY_F9, "reset": KEY_R}
	for action: String in key_codes:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		var key := InputEventKey.new()
		key.physical_keycode = key_codes[action]
		InputMap.action_add_event(action, key)
	player.observed.connect(record)
	player.control_requested.connect(control_action)
	player.configure(self, fixture.actor)
	camera.position = vector(fixture.camera.center_px)
	camera.make_current()
	var gap: Dictionary = fixture.gap
	var top: float = float(gap.center_y_px) - float(gap.height_px) / 2.0
	var bottom: float = float(gap.center_y_px) + float(gap.height_px) / 2.0
	make_wall("UpperBarrier", Rect2(float(gap.barrier_x_px) - float(gap.thickness_px) / 2.0, 0, float(gap.thickness_px), top))
	make_wall("LowerBarrier", Rect2(float(gap.barrier_x_px) - float(gap.thickness_px) / 2.0, bottom, float(gap.thickness_px), 180 - bottom))
	record("fixture_loaded", {"case_id": fixture.case_id, "fixture_sha256": FileAccess.get_sha256(fixture_path)})


func vector(values: Array) -> Vector2:
	return Vector2(float(values[0]), float(values[1]))


func make_wall(wall_name: String, rect: Rect2) -> void:
	var wall := StaticBody2D.new()
	wall.name = wall_name
	wall.position = rect.get_center()
	wall.collision_layer = 1
	wall.collision_mask = 2
	var collider := CollisionShape2D.new()
	var shape := RectangleShape2D.new()
	shape.size = rect.size
	collider.shape = shape
	wall.add_child(collider)
	add_child(wall)


func record(kind: String, detail: Dictionary = {}) -> void:
	var entry := {"sequence": events.size(), "kind": kind, "run_tick": run_tick, "world_tick": world_tick,
		"game_time_s": world_tick / 60.0, "engine_physics_frame": Engine.get_physics_frames(),
		"monotonic_us": Time.get_ticks_usec(), "detail": detail.duplicate(true)}
	events.append(entry)


func _physics_process(_delta: float) -> void:
	if fixture.is_empty() or completed:
		return
	run_tick += 1
	world_tick += 1
	if run_tick == 1:
		first_physics_frame = Engine.get_physics_frames()
	if automatic:
		for command: Dictionary in fixture.input_schedule:
			if int(command.tick) == run_tick:
				record("input_injected", {"action": command.action, "pipeline": "Input.parse_input_event"})
				var event := InputEventAction.new()
				event.action = command.action
				event.pressed = true
				Input.parse_input_event(event)
				var release := InputEventAction.new()
				release.action = command.action
				release.pressed = false
				Input.parse_input_event(release)
				# The harness controls delivery time; hardware and render latency remain unmeasured.
				Input.flush_buffered_events()
	for threat: Dictionary in fixture.threats:
		if world_tick == int(threat.warning_tick) and not str(threat.id) in warned:
			warned.append(str(threat.id))
			var screen_position: Vector2 = get_viewport().get_canvas_transform() * vector(threat.source_px)
			record("warning_presented", {"threat_id": threat.id, "source_px": threat.source_px,
				"screen_position_px": [screen_position.x, screen_position.y],
				"inside_camera_rect": get_viewport_rect().has_point(screen_position),
				"resolution_tick": threat.resolve_tick, "recovery_until": player.recovery_until,
				"text": fixture.warning_text, "modality": "scene_geometry_only"})
	queue_redraw()


func after_player_step(_delta: float) -> void:
	if completed:
		return
	if run_tick == 3:
		var ray := PhysicsRayQueryParameters2D.create(vector(fixture.actor.start_px), Vector2(200, 90), 1)
		var hit: Dictionary = get_world_2d().direct_space_state.intersect_ray(ray)
		record("geometry_witness", {"center_ray_clear": hit.is_empty(), "body_diameter_px": float(fixture.actor.radius_px) * 2.0,
			"gap_height_px": fixture.gap.height_px, "collision_mask": player.collision_mask,
			"ray_is_not_body_clearance": true, "viewport_size_px": [get_viewport_rect().size.x, get_viewport_rect().size.y]})
	witnesses.append({"run_tick": run_tick, "world_tick": world_tick, "position_px": [player.position.x, player.position.y], "health": player.health})
	if player.position.x >= 152 and not "gate-crossed" in history:
		history.append("gate-crossed")
		var sight := PhysicsRayQueryParameters2D.create(Vector2(200, 90), player.position, 1)
		if get_world_2d().direct_space_state.intersect_ray(sight).is_empty():
			knowledge["keeper-ivo"].append("gate-crossed")
			record("knowledge_acquired", {"actor_id": "keeper-ivo", "fact_id": "gate-crossed", "channel": "unoccluded_local_sight"})
		record("gate_crossed", {"actor_id": fixture.actor.id, "x_px": player.position.x})
	for threat: Dictionary in fixture.threats:
		if world_tick == int(threat.resolve_tick) and not str(threat.id) in resolved:
			resolved.append(str(threat.id))
			var hit: bool = player.position.x < float(threat.danger_max_x_px)
			if hit:
				player.health -= 1
			record("threat_resolved", {"threat_id": threat.id, "hit": hit, "actor_x_px": player.position.x, "health": player.health})
	if automatic and run_tick >= int(fixture.stop_tick):
		finish()


func snapshot() -> Dictionary:
	return {"game_id": fixture.game_id, "build_id": fixture.build_id, "world_tick": world_tick,
		"actor": player.snapshot(), "history": history.duplicate(true), "knowledge": knowledge.duplicate(true),
		"right_owners": right_owners.duplicate(true), "resolved": resolved.duplicate(), "warned": warned.duplicate()}


func control_action(action: String) -> void:
	if action == "save":
		save_snapshot = snapshot()
		var file := FileAccess.open(save_path, FileAccess.WRITE)
		if file == null:
			record("save_failed", {"error": FileAccess.get_open_error()})
			return
		file.store_string(JSON.stringify(save_snapshot))
		file.close()
		record("state_saved", {"sha256": FileAccess.get_sha256(save_path)})
	elif action == "reset":
		player.reset_actor()
		world_tick = 0
		history = ["archive-message"]
		knowledge = {"bo": ["winch-procedure"], "keeper-ivo": []}
		resolved.clear()
		warned.clear()
		record("state_reset", {"actor_x_px": player.position.x})
	elif action == "load":
		var parsed := JSON.new()
		if parsed.parse(FileAccess.get_file_as_string(save_path)) != OK or not parsed.data is Dictionary:
			record("load_failed", {})
			return
		var data: Dictionary = parsed.data
		if data.game_id != fixture.game_id or data.build_id != fixture.build_id:
			record("load_failed", {"reason": "identity_mismatch"})
			return
		world_tick = int(data.world_tick)
		player.restore(data.actor)
		history.assign(data.history)
		knowledge = data.knowledge
		right_owners = data.right_owners
		resolved.assign(data.resolved)
		warned.assign(data.warned)
		restored_equal = snapshot() == save_snapshot
		record("state_restored", {"matches_saved_relations": restored_equal, "world_tick": world_tick, "actor_x_px": player.position.x})
	elif action == "interact":
		final_line = "The winch route is ready." if "gate-crossed" in knowledge["keeper-ivo"] else "I have not seen a crossing."
		record("npc_reply", {"speaker_id": "keeper-ivo", "known_fact_ids": knowledge["keeper-ivo"], "line": final_line})


func finish() -> void:
	completed = true
	var sources := {}
	for path: String in SOURCE_PATHS:
		sources[path] = FileAccess.get_sha256("res://" + path)
	var report := {"status": "consumer_executed", "game_id": fixture.game_id, "build_id": fixture.build_id,
		"case_id": fixture.case_id, "run_id": run_id, "fixture_sha256": FileAccess.get_sha256(fixture_path),
		"source_sha256": sources, "engine": Engine.get_version_info(), "physics_ticks_per_second": Engine.physics_ticks_per_second,
		"first_physics_frame": first_physics_frame, "display_driver": DisplayServer.get_name(),
		"input_received_count": player.input_received_count, "body_collision_ticks": player.collision_ticks,
		"events": events, "trajectory": witnesses, "final_state": snapshot(),
		"saved_state": save_snapshot, "restored_equal": restored_equal, "npc_reply": final_line,
		"limits": ["Synthetic engine events, not hardware input.", "Headless geometry and event clocks do not establish rendered visibility, audio or human perception."]}
	if not output_path.is_empty():
		var file := FileAccess.open(output_path, FileAccess.WRITE)
		if file == null:
			push_error("Could not write report.")
			get_tree().quit(2)
			return
		file.store_string(JSON.stringify(report, "  "))
		file.close()
	print(JSON.stringify({"case_id": fixture.case_id, "operation": "consumer_executed", "input_events": player.input_received_count,
		"health": player.health, "actor_x_px": player.position.x, "restored_equal": restored_equal}))
	get_tree().quit(0)


func _draw() -> void:
	if fixture.is_empty():
		return
	var gap: Dictionary = fixture.gap
	var top: float = float(gap.center_y_px) - float(gap.height_px) / 2.0
	var bottom: float = float(gap.center_y_px) + float(gap.height_px) / 2.0
	draw_rect(Rect2(float(gap.barrier_x_px) - 8, 0, 16, top), Color(0.3, 0.36, 0.42))
	draw_rect(Rect2(float(gap.barrier_x_px) - 8, bottom, 16, 180 - bottom), Color(0.3, 0.36, 0.42))
	draw_circle(Vector2(200, 90), 6, Color(0.75, 0.72, 0.5))
	for threat: Dictionary in fixture.threats:
		if str(threat.id) in warned and not str(threat.id) in resolved:
			draw_arc(vector(threat.source_px), 12, 0, TAU, 32, Color(1.0, 0.62, 0.15), 2)
