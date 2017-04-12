# This is where you build your AI for the Stumped game.

from joueur.base_ai import BaseAI
from math import floor, ceil
from random import random


class AI(BaseAI):
	""" The basic AI functions that are the same between games. """

	def get_name(self):
		return "Hillary\'s Deleted Beavers I mean Email"

	def start(self):
		""" This is called once the game starts and your AI knows its playerID and game. You can initialize your AI here.
		"""
		self.tree_tiles = self.get_all_trees_spawners()
		self.food_tiles = self.get_all_food_spawners()

	def game_updated(self):
		""" This is called every time the game's state updates, so if you are tracking anything you can update it here.
		"""
		# replace with your game updated logic

	def end(self, won, reason):
		""" This is called when the game ends, you can clean up your data and dump files here if need be.

		Args:
						won (bool): True means you won, False means you lost.
						reason (str): The human readable string explaining why you won or lost.
		"""
		# replace with your end logic

	def get_all_trees_spawners(self):
		tree_tiles = []
		for tile in self.game.tiles:
			if tile.spawner:
				if tile.spawner.type == 'branches':
					tree_tiles.append(tile)
		return tree_tiles

	def get_all_food_spawners(self):
		food_tiles = []
		for tile in self.game.tiles:
			if tile.spawner:
				if tile.spawner.type == 'food':
					food_tiles.append(tile)
		return food_tiles

	def calculate_distance(self, tile_1, tile_2):
		"""
		calculates the manhattan distance between 2 tiles
		"""
		return abs(tile_1.x - tile_2.x) + abs(tile_1.y - tile_2.y)

	def find_closest_tree(self, tile):
		"""
		finds the closest tree to the current tile
		tile: current tile
		best tile is the nearest tree tile
		returns the closest tree tile
		"""
		best_dist = 1000000
		best_tile = tile
		for tree_tile in self.tree_tiles:
			dist = self.calculate_distance(tile, tree_tile)
			if dist < best_dist and self.find_path(tile, tree_tile):
				best_dist = dist
				best_tile = tree_tile
		return best_tile

	def is_adjacent_wood(self, beaver):
		for tile in beaver.tile.get_neighbors:
			if tile.spawner.type == 'branches':
				return True

	def is_adjacent_food(self, beaver):
		for tile in beaver.tile.get_neighbors:
			if tile.spawner.type == 'food':
				return True

	def is_adjacent_lodge(self, beaver):
		for tile in beaver.tile.get_neighbors:
			if tile.lodge_owner == self.player:
				return "friendly"
			elif tile.lodge_owner == self.player.opponent:
				return "hostile"
			else:
				return None

	def get_beavers(self):
		my_beavers = []
		opp_beavers = []
		for beaver in self.game.beavers:
			if beaver.health > 0:
				if beaver.owner == self.game.current_player:
					my_beavers.append(beaver)
				else:
					opp_beavers.append(beaver)
		return my_beavers, opp_beavers

	def decide_job(self):
		builder_count, fighter_count, hungry_count = 0, 0 ,0
		for beaver in self.my_beavers:
			if beaver.job.title == 'Fighter':
				fighter_count += 1
			elif beaver.job.title == 'Builder':
				builder_count += 1
			elif beaver.job.title == 'Hungry':
				hungry_count += 1

			print(builder_count)
			if builder_count < 5:
				print(self.game.jobs[1].title)
				return self.game.jobs[1]
			elif hungry_count < 5:
				return self.game.jobs[5]
			else:
				return self.game.jobs[6]

	def spawn_logic(self, lodge):
		if lodge and not lodge.beaver:
			# We need to know how many beavers we have to see if they are free
			# to spawn
			alive_beavers = len(
				[beaver for beaver in self.player.beavers if beaver.health > 0])

			job = self.decide_job()

			# if we have less beavers than the freeBeavers count, it is free to spawn
			# otherwise if that lodge has enough food on it to cover the job's
			# cost
			if alive_beavers < self.game.free_beavers_count or lodge.food >= job.cost:
				# then spawn a new beaver of that job!
				print('Recruiting {} to {}'.format(job, lodge))
				job.recruit(lodge)
				alive_beavers += 1

	def is_adjacent_wood(self, beaver):
		for tile in beaver.tile.get_neighbors():
			if tile.spawner and tile.spawner.type == 'branches':
				return True

	def is_adjacent_food(self, beaver):
		for tile in beaver.tile.get_neighbors:
			if tile.spawner.type == 'food':
				return True

	def is_adjacent_lodge(self, beaver):
		for tile in beaver.tile.get_neighbors:
			if tile.lodge_owner == self.player:
				return "friendly"
			elif tile.lodge_owner == self.player.opponent:
				return "hostile"
			else:
				return None

	def get_off_lodge(self, beaver):
		"""
		checks if the beaver is on a lodge and moves it off required
		"""
		# If the beaver is standing on a lodge, get off to make room
		if beaver.moves and beaver.tile.lodge_owner:
			for tile in beaver.tile.get_neighbors():
				if tile.is_pathable():
					beaver.move(tile)

	def builder_logic(self, my_beaver):
		if not self.is_adjacent_wood(my_beaver):
			if my_beaver.moves > 0:
				try:
					target = self.find_closest_tree(my_beaver.tile)
					path = self.find_path(my_beaver.tile, target)
					while my_beaver.moves:
						my_beaver.move(path.pop(0))
				except:
					pass

		# if it's carrying too much wood, drop it off if it's near a source of
		# wood
		if my_beaver.branches >= 3 and my_beaver.actions > 0 and self.is_adjacent_wood(my_beaver):
			my_beaver.drop(my_beaver.tile, 'branch', -1)

		# if it's near some wood, harvest as much wood as possible
		if self.is_adjacent_wood(my_beaver):
			if my_beaver.actions > 0:
				for tile in my_beaver.tile.get_neighbors():
					if tile.spawner and tile.spawner.type == 'branches':
						target = tile.spawner
				my_beaver.harvest(target)


	def run_turn(self):
		""" This is called every time it is this AI.player's turn.

		Returns:
						bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
		"""
		# each turn get my beavers and opponent beavers that are still alive
		self.my_beavers, self.opp_beavers = self.get_beavers()
		print(self.my_beavers)

		for lodge in self.player.lodges:
			self.spawn_logic(lodge)

		for beaver in self.my_beavers:
			# if the beaver is on a lodge get him off
			self.get_off_lodge(beaver)

			# If the beaver has enough wood to make a lodge, do so
			if beaver.branches + beaver.tile.branches >= self.player.branches_to_build_lodge:
				beaver.build_lodge()

			if beaver.job.title == 'Basic':
				self.builder_logic(beaver)
			if beaver.job.title == 'Builder':
				self.builder_logic(beaver)

		return True  # to signify that we are truly done with this turn

	def find_path(self, start, goal):
		"""A very basic path finding algorithm (Breadth First Search) that when given a starting Tile, will return a valid path to the goal Tile.
		Args:
						start (Tile): the starting Tile
						goal (Tile): the goal Tile
		Returns:
						list[Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
		"""

		if start == goal:
			# no need to make a path to here...
			return []

		# queue of the tiles that will have their neighbors searched for 'goal'
		fringe = []

		# How we got to each tile that went into the fringe.
		came_from = {}

		# Enqueue start as the first tile to have its neighbors searched.
		fringe.append(start)

		# keep exploring neighbors of neighbors... until there are no more.
		while len(fringe) > 0:
			# the tile we are currently exploring.
			inspect = fringe.pop(0)

			# cycle through the tile's neighbors.
			for neighbor in inspect.get_neighbors():
				# if we found the goal, we have the path!
				if neighbor == goal:
					# Follow the path backward to the start from the goal and
					# return it.
					path = [goal]

					# Starting at the tile we are currently at, insert them
					# retracing our steps till we get to the starting tile
					while inspect != start:
						path.insert(0, inspect)
						inspect = came_from[inspect.id]
					return path
				# else we did not find the goal, so enqueue this tile's
				# neighbors to be inspected

				# if the tile exists, has not been explored or added to the
				# fringe yet, and it is pathable
				if neighbor and neighbor.id not in came_from and neighbor.is_pathable():
					# add it to the tiles to be explored and add where it came
					# from for path reconstruction.
					fringe.append(neighbor)
					came_from[neighbor.id] = inspect

		# if you're here, that means that there was not a path to get to where you want to go.
		#   in that case, we'll just return an empty path.
		return []
