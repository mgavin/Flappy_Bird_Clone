from godot import exposed, export
from godot.bindings import *
from godot.node_path import NodePath
from godot.vector2 import Vector2

@exposed
class Player(KinematicBody2D):
	"""Defines Player behavior and mechanics

	Attributes:
		_GRAVITY_VEC (Vector2): Describes the effects of gravity on the Player
		_JUMP_SPEED (int): I... don't know.
		_linear_vel (Vector2): Describes x,y of Player moving
		_current_state: Points to which method holds logic for the current Player state
		_pPos (Vector2): Player position
		_force_on_player (Vector2): A force on the Player?

		_AnimationPlayer: A shorter name for the animation player.
	"""

	def _ready(self):
		self._GRAVITY_VEC = Vector2(100,900) # pix/sec
		self._JUMP_SPEED = -480
		self._linear_vel = Vector2(0,0)
		self._pPos = self.get_position()
		self._force_on_player = Vector2(0,0)
		self._AnimationPlayer = self.get_node(NodePath('AnimationPlayer'))
		self._current_state = self._idle

	def _physics_process(self,delta):
		if self._linear_vel.x >= 300:
			self._linear_vel.x = 300
			self._GRAVITY_VEC.x = 0
		else:
			self._GRAVITY_VEC.x = 100
		self._force_on_player += self._GRAVITY_VEC * delta

		# execute the current state
		self._current_state()

		if Input.is_action_just_pressed('Player_Jump'):
			self._linear_vel.y = self._JUMP_SPEED
			#self._AnimationPlayer.play('Flap',-1,1,False)
			self._current_state = self._flapping

		self._pPos = self.get_position()
		self._force_on_player = self.move_and_slide(self._force_on_player,Vector2(0,-1),0,4,0.78)

		#else:
			#self.get_node(NodePath("AnimationPlayer")).play("Idle",-1,1,False)


	def _on_Area2D_body_entered(self, body):
		if body.get_name() == 'Pipe':
			self._current_state = self._death

	def __repr__(self):
		return f'Player:{self.get_position()}:{self._linear_vel.y}:{self._JUMP_SPEED}'

	# private methods defining various states of the player
	def _idle(self):
		pass

	def _flapping(self):
		#if (self._pPos.y < self.get_position().y): # and \
		 #(self._AnimationPlayer.get_current_animation_position() > .5):
			#self._AnimationPlayer('Flapping')
		self._current_state = self._falling

	def _falling(self):
		#self._AnimationPlayer('Falling')
		self._current_state = self._idle

	def _stagger(self):
		if not(self._AnimationPlayer.is_playing()):
			self._force_on_player.x = 100
			self._force_on_player.y = 0
			self._current_state = self._idle
		else:
			self._force_on_player.x -= 10*delta

		#self._AnimationPlayer.play('Stagger')
		self._force_on_player.x = -200
		self._force_on_player.y = -Jump_Speed

	def _death(self):
		pass
