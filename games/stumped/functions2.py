    def beaver_act(self):
        #if the beaver is standing on a lodge, get off to make room
        if my_beaver.tile.lodge_owner:
            try:
                my_beaver.move(my_beaver.tile.tile_east)
            except:
                try:
                    my_beaver.move(my_beaver.tile.tile_west)
                except:
                    try:
                        my_beaver.move(my_beaver.tile.tile_south)
                    except:
                        try:
                            my_beaver.move(my_beaver.tile.tile_north)
        #if the beaver has enough wood to make a lodge, do so
        if my_beaver.branches + my_beaver.tile.branches >= self.player.branches_to_build_lodge:
            my_beaver.build_lodge
        #builder
        if my_beaver.Job.title == 'Builder':
            #move toward a source of wood
            if not is_adjacent_wood(my_beaver):
                if my_beaver.moves > 0:
                    ##### move toward wood via resource_path
                    pass
            #if it's carrying too much wood, drop it off if it's near a source of wood
            if my_beaver.branches >= 3:
                if my_beaver.actions > 0:
                    if is_adjacent_wood(my_beaver):
                        my_beaver.drop(my_beaver.tile, 'branch', -1)
                    #if it's near some wood, harvest as much as possible
            if is_adjacent_wood(my_beaver):
                if my_beaver.actions > 0:
                    for tile in my_beaver.tile.get_neighbors:
                        if tile.spawner.type == 'branches':
                            target = tile
                    my_beaver.harvest(target)
        #hungry beaver
        if my_beaver.Job.title == 'Hungry':
            #if it's at carrying capacity, drop off food at nearest lodge
            if my_beaver.food >= 15:
                if my_beaver.tile.lodge_owner = self.player:
                    my_beaver.drop(my_beaver.tile, 'food', -1)
                else:
                    if my_beaver.moves > 0:
                        # ###### move toward lodge via resource_path
                        pass
            if not is_adjacent_food(my_beaver):
                # #### move tward food via resource_path
                pass
            if is_adjacent_food(my_beaver):
                for tile in my_beaver.tile.get_neighbors:
                    if tile.spawner.type == 'food':
                        target = tile
                my_beaver.harvest(target)
