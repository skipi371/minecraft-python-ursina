from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random  # Ajout de l'import random qui manquait pour random.randint
changer = 100
chance_fer_place = 2
visibility_timer = 0.0
render_distance = 5
blocks = []
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
    global block_pick, visibility_timer
    for i in range(1,6):
        if held_keys[str(i)]:
            block_pick = i
            break
    if held_keys["escape"]:
        application.quit()
    if player.y <= -15:
        player.position = (10,10,10) # Correction syntaxe position

    visibility_timer += time.dt
    if visibility_timer >= 0.2:
        visibility_timer = 0.0
        max_distance_squared = render_distance ** 2

        for block in blocks:
            dx = player.x - block.x
            dy = player.y - block.y
            dz = player.z - block.z
            block.enabled = dx * dx + dy * dy + dz * dz <= max_distance_squared

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
    def __init__(self, position=(0, 10, 0), texture=textures[7], breakable=False):
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

# --- CORRECTION DES CLASSES SKYBOX ---



class tree(Entity):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model="Asset/Models/Lowpoly_tree_sample.obj",
            scale=(0.5, 0.5, 0.5),
            collider="mesh"
        )

def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size - 1)
        y = 0
        z = random.randint(0, terrain_size - 1)
        tree(position=(x, y, z)) # Instanciation du pixel de l'arbre manquante

# --- FONCTION DE SÉLECTION ---

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
                if block in blocks:
                    blocks.remove(block)
                destroy(block)

    elif key == "right mouse down":
        if mouse.hovered_entity and hasattr(mouse.hovered_entity, "breakable"):
            target = mouse.hovered_entity.position + mouse.normal
            if mouse.hovered_entity.breakable:
                build_sound.play()
                Block(position=target, texture=textures[block_pick])

# Génération de la map
generate_trees()
for z in range(30):
    chance_fer_place = random.randint(0, 10)
    for x in range(30):
        block = Block(position=(x, random.randint(0, 2), z))
        bedrock = Block(position=(x, random.randint(-3, -1), z), texture=textures[5], breakable=True)
        charbon = coal(position=(x, random.randint(-3, -1), z))  
        fer = Iron(position=(x, random.randint(-7, -5), z), texture=textures[7], breakable=False)

player = FirstPersonController(position=(10, 10, 10))
player.cursor.visible = True

# Instanciation unique des deux ciels

# Mode par défaut au lancement (Jour actif, Nuit inactive)


if __name__ == "__main__":
    app.run()
