	def spawn_logic:
		for lodge in self.player.lodges:
			if len self.beavers <= 5:
				recruit(lodge
	
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
			if tile.lodge_owner = self.player:
				return "friendly"
			elif tile.lodge_owner = self.player.opponent:
				return "hostile"
			else:
				return None
				
	def beaver_act(self):
		#If the beaver is standing on a lodge, get off to make room
		if my_beaver.moves > 0:
			if my_beaver.tile.lodge_owner:
				try:
					my_beaver.move(my_beaver.tile.tile_east)
				except:
					try:
						my_beaver.move(my_beaver.tile.tile_west)
					except:
						try:
							my_beaver.move(my_beaver.tile.tile_north)
						except:
							try:
								my_beaver.move(my_beaver.tile.tile_south)
								
		#If the beaver has enough wood to make a lodge, do so
		if my_beaver.branches + my_beaver.tile.branches >= self.player.branches_to_build_lodge:
			my_beaver.build_lodge
			
		#builder logic
		if my_beaver.job = 'Builder':
			#move toward a source of wood
			if not is_adjacent_wood(my_beaver):
				if my_beaver.moves > 0:
					# ##########move toward wood via resource_path
					pass
				
			#if it's carrying too much wood, drop it off if it's near a source of wood
			if my_beaver.branches >= 3:
				if my_beaver.actions > 0:
					if is_adjacent_wood(my_beaver):
						my_beaver.drop(my_beaver.tile, 'branch', -1)
				
			# if it's near some wood, harvest as much wood as possible
			if is_adjacent_wood(my_beaver):
				if my_beaver.actions > 0:
					for tile in my_beaver.tile.get_neighbors:
						if tile.spawner.type == 'branches':
							target = tile
					my_beaver.harvest(target)
				
		#hungry beaver logic
		if my_beaver.job = 'Hungry':
			#if it's at carrying capacity, drop it off at the nearest lodge
			if my_beaver.food >= 15:
				if my_beaver.tile.lodge_owner:
					my_beaver.drop(my_beaver.tile, 'food',-1)
				else:
					if my_beaver.moves > 0:
						# ###########move toward friendly lodge via resource_path
						pass
			if not is_adjacent_food(my_beaver):
				# ###### move toward food via resource_path
				pass
			if is_adjacent_food(my_beaver):
				for tile in my_beaver.tile.get_neighbors:
						if tile.spawner.type == 'food':
							target = tile
				my_beaver.harvest(target)
				
		#fighter beaver logic
		if my_beaver.job = 'Fighter':
			for targ_tile in my_beaver.tile.get_neighbors:
				if targ_tile.beaver:
					if targ_tile.beaver.owner = self.player.opponent:
						my_beaver.attack(targ_tile.beaver)
						
			if is_adjacent_lodge(my_beaver) != "hostile":
				# ######## move toward enemy lodge
				pass