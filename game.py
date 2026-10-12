from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
import random  # Ajout de l'import random qui manquait pour random.randint
changer = 100
chance_fer_place = 2
blocks = []
block_data = {}
block_by_position = {}
NEIGHBOR_OFFSETS = (
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1),
)
app = Ursina()
nb = 0
def changer_mode(mode):
    if mode == "jour":
        sky_jour.enabled = True
        sky_nuit.enabled = False
        # Optionnel : Ajuster la lumière ambiante globale si besoin
    elif mode == "nuit":
        sky_jour.enabled = False
        sky_nuit.enabled = True
class SkyBoxNuit(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=night_bg,
            scale=150,
            double_sided=True,
        )


class SkyBoxJour(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_bg,
            scale=150,
            double_sided=True,
        )



chance_place_coal = random.randint(1,3)

def update():
    global block_pick
    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i
            break
    if held_keys["escape"]:
        application.quit()
    if player.y <= -15:
        player.position = (10,10,10) # Correction syntaxe position

# load all asset
textures = {
    1: load_texture("Assets/Textures/grass.png"),
    2: load_texture("Assets/Textures/Dirt.png"),
    3: load_texture("Assets/Textures/Brick.png"),
    4: load_texture("Assets/Textures/Wood.png"),
    5: load_texture("Assets/Textures/Stone.png"),
    6: load_texture("Assets/Textures/Coal.png"),
    7: load_texture("Assets/Textures/Iron.png"),
}

block_pick = 1

sky_bg = load_texture("Assets/Textures/Sky.png")
night_bg = load_texture("Assets/Textures/Night.png")

sky_jour = SkyBoxJour()
sky_nuit = SkyBoxNuit()
changer_mode("jour")

build_sound = Audio("Assets/SFX/Build_Sound.wav", loop=False, autoplay=False)


for _ in range(changer) :
    print(f"{nb}")
    nb += 1 
    if nb == changer -1 : 
        changer_mode("nuit")
    
class Block(Button):
    def __init__(self, position=(0, 0, 0), texture=textures[1], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj",
            origin_y=0.5,
            texture=texture,
            color=color.white,
            highlighting_color=color.light_gray,
            scale=0.5,
        )
        self.breakable = breakable
        blocks.append(self)

class coal(Button): 
    def __init__(self, position=(0, 5, 0), texture=textures[6], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj",
            origin_y=0.5,
            texture=texture,
            color=color.white,
            highlighting_color=color.light_gray,
            scale=0.5,
        )
        self.breakable = breakable
        blocks.append(self)

class Iron(Button):
    def __init__(self, position=(0, 10, 0), texture=textures[7], breakable=True):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj",
            origin_y=0.5,
            texture=texture,
            color=color.white,
            highlighting_color=color.light_gray,
            scale=0.5,
        )
        self.breakable = breakable
        blocks.append(self)

def adjacent_positions(position):
    return [
        (position[0] + dx, position[1] + dy, position[2] + dz)
        for dx, dy, dz in NEIGHBOR_OFFSETS
    ]


def refresh_block_visibility(positions=None):
    if positions is None:
        positions = tuple(block_data)

    for position in positions:
        block_info = block_data.get(position)
        exposed = block_info is not None and any(
            neighbor not in block_data
            for neighbor in adjacent_positions(position)
        )
        existing_block = block_by_position.get(position)
        if exposed and existing_block is None:
            block_class, texture, breakable = block_info
            block_by_position[position] = block_class(
                position=position,
                texture=texture,
                breakable=breakable,
            )
        elif not exposed and existing_block is not None:
            block_by_position.pop(position)
            if existing_block in blocks:
                blocks.remove(existing_block)
            destroy(existing_block)





def input(key):
    global block_pick
    
    # Touches pour sélectionner les classes de ciel
    if key == 'j':
        changer_mode("jour")
    if key == 'n':
        changer_mode("nuit")

    if key == "left mouse down":
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "breakable"):
            block = mouse.hovered_entity
            if block.breakable:
                build_sound.play()
                position = tuple(round(value) for value in block.position)
                block_data.pop(position, None)
                block_by_position.pop(position, None)
                if block in blocks:
                    blocks.remove(block)
                destroy(block)
                refresh_block_visibility(adjacent_positions(position))

    elif key == "right mouse down":
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "breakable"):
            target = mouse.hovered_entity.position + mouse.normal
            if mouse.hovered_entity.breakable:
                build_sound.play()
                position = tuple(round(value) for value in target)
                if position not in block_data:
                    block_data[position] = (Block, textures[block_pick], True)
                    refresh_block_visibility(
                        [position, *adjacent_positions(position)]
                    )

# Génération de la map

for z in range(30):
    for x in range(30):
        surface_y = random.randint(0, 2)
        position = (x, surface_y, z)
        block_data[position] = (Block, textures[1], True)

        for depth in range(1, 8):
            position = (x, surface_y - depth, z)
            if depth >= 5 and random.random() < 0.08:
                block_data[position] = (Iron, textures[7], True)
            elif depth >= 3 and random.random() < 0.15:
                block_data[position] = (coal, textures[6], True)
            else:
                texture = textures[2] if depth <= 2 else textures[5]
                block_data[position] = (Block, texture, True)

refresh_block_visibility()
        
player = FirstPersonController(position=(10, 10, 10))
player.cursor.visible = True

# Instanciation unique des deux ciels

# Mode par défaut au lancement (Jour actif, Nuit inactive)


if __name__ == "__main__":
    app.run()
    