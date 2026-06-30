import random
from .direction import Direction
from .position  import Position
from .gui       import Gui
from .action    import Action, ActionSet
from PIL        import Image

ROW_MAPPING     = {
    "sur"       : 0,
    "norte"     : 1,
    "oeste"     : 2,
    "suroeste"  : 3,
    "noroeste"  : 4
}

RANDOM_MONSTER  = ['gible', 'gabite', 'garchomp'][int(random.random()*3)]
SPRITE_SIZES    = {
    'gible'     : 24,
    'gabite'    : 32,
    'garchomp'  : 40,
}

class MonsterStats:
    def __init__(self, speed=None, strenght=None, defense=None, special=None, evasion=None, vitality=None, xp=None):
        self.vitality = random.randint(12,25) if not vitality else vitality
        self.speed    = random.randint(4,10) if not speed else speed
        self.evasion  = random.randint(4,10) if not evasion else evasion
        self.strength = random.randint(4,10) if not strenght else strenght
        self.defense  = random.randint(4,10) if not defense else defense
        self.special  = random.randint(4,10) if not special else special
        self.xp       = 0 if not xp else xp

class Monster:
    def __init__(self, app, name=None, random=False):
        if not name and not random: raise Exception('You must specify either a valid name or random=True')
        self.stats          = MonsterStats()
        self.app            = app
        self.name           = RANDOM_MONSTER if random else name
        self.size           = Position( SPRITE_SIZES[ self.name ],SPRITE_SIZES[ self.name ] ) 
        self.render_size    = self.size.getScaled( Gui.SCALE_FACTOR )
        self.sprite_size    = self.render_size.copy()
        self.position       = Position( self.app.gui.screen_size.x / 2, 0)
        self.actions        = ActionSet( self )
        self.action         = self.actions.walk
        self.direction      = Direction.ESTE
        self.current_frame  = 0
        self.update()

    def load_and_process_sprites(self, file_path, accion_obj):
        img = Image.open(file_path).convert("RGBA")
        
        for pose, row in ROW_MAPPING.items():
            accion_obj.sprites_db[pose] = []
            for frame in range(3):
                # Recortar frame
                left = frame * self.size.x
                top = row * self.size.y
                box = (left, top, left + self.size.x, top + self.size.y)
                frame_img = img.crop(box)
                
                # Filtrar tu máscara fucsia exacta (255, 0, 255) a transparencia total
                datas = frame_img.getdata()
                new_data = []
                for item in datas:
                    if item[0] == 255 and item[1] == 0 and item[2] == 255:
                        new_data.append((0, 0, 0, 0))  # Transparente real
                    else:
                        new_data.append(item)
                frame_img.putdata(new_data)
                
                # Convertir la imagen de Pillow a un QPixmap de PyQt compatible
                qpixmap = self.app.gui.pillow_to_qpixmap(frame_img, self.render_size.x, self.render_size.y)
                accion_obj.sprites_db[pose].append(qpixmap)
            accion_obj.sprites_db[pose].append(accion_obj.sprites_db[pose][1])
            
            # Generar automáticamente las poses espejo (Flipped Horizontal)
            if pose in ["oeste", "suroeste", "noroeste"]:
                target_pose = "este" if pose == "oeste" else ("sudeste" if pose == "suroeste" else "nordeste")
                accion_obj.sprites_db[target_pose] = []
                for f_img in [img.crop((f*self.size.x, row*self.size.y, f*self.size.x+self.size.x, row*self.size.y+self.size.y)) for f in range(3)]:
                    mirror_img = f_img.transpose(Image.FLIP_LEFT_RIGHT)
                    # Filtrar fucsia también en el espejo
                    m_datas = mirror_img.getdata()
                    m_new_data = []
                    for item in m_datas:
                        if item[0] == 255 and item[1] == 0 and item[2] == 255:
                            m_new_data.append((0, 0, 0, 0))
                        else:
                            m_new_data.append(item)
                    mirror_img.putdata(m_new_data)
                    accion_obj.sprites_db[target_pose].append(self.app.gui.pillow_to_qpixmap(mirror_img, self.render_size.x, self.render_size.y))
                accion_obj.sprites_db[target_pose].append(accion_obj.sprites_db[target_pose][1])
    
    def randomizeDirection(self):
        r = random.randint(1,100)
        if r > 65:
            self.direction = Direction.ESTE
        if r < 35:
            self.direction = Direction.OESTE

    def randomizeAction(self):
        r = random.randint(1,100)
        if r == 7:
            self.action = self.actions.idle
        if r > 90:
            self.action = self.actions.walk

    def walk(self):
        speed = self.stats.speed * 0.5 * Gui.SCALE_FACTOR
        self.position.x += Direction.DELTA[ self.direction ].x * speed
        if self.position.x > self.app.gui.screen_size.x - (self.render_size.x >> 1 ):
            self.direction = Direction.OESTE
        if self.position.x < (self.render_size.x >> 1 ):
            self.direction = Direction.ESTE
        
    def update_animation(self):
        self.randomizeAction()
        if self.action.type == Action.IDLE: self.randomizeDirection()
        elif self.action.type == Action.WALK: self.walk()
        self.current_frame = (self.current_frame+1)%4
        self.update()
        
    def update(self):
        self.app.setGeometry(
            int(
                self.position.x
                -
                ( self.render_size.x >> 1 )
            ), 
            int(
                ( self.position.y - self.render_size.y ) 
                + 
                ( self.app.gui.screen_size.y - Gui.TASKBAR_HEIGHT )
            ), 
            self.render_size.x, 
            self.render_size.y
        )        
        self.app.gui.update(self)
    
    