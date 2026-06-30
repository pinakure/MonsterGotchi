class Action:

    IDLE    = 0
    WALK    = 1
    ATTACK  = 2
    SPECIAL = 3
    HURT    = 4
    
    INDEX = {
        "idle"      : IDLE,
        "walk"      : WALK,
        "attack"    : ATTACK,
        "special"   : SPECIAL,
        "hurt"      : HURT
    }    
    NAME = {
        IDLE        : "idle",
        WALK        : "walk",
        ATTACK      : "attack",
        SPECIAL     : "special",
        HURT        : "hurt"
    }
    def __init__(self, parent, action):
        self.nombre = Action.NAME[action]
        self.type   = action
        self.parent = parent
        self.sprites_db = {}  # Guarda las poses (direcciones) de esta acción específica
        parent.monster.load_and_process_sprites( f"{ parent.monster.name }-{ Action.NAME[action] }.png", self )

class ActionSet:

    def __init__(self, monster):
        self.monster = monster
        self.idle    = Action(self, Action.IDLE)
        self.walk    = Action(self, Action.WALK)
        self.attack  = Action(self, Action.ATTACK)
        self.special = Action(self, Action.SPECIAL)
        self.hurt    = Action(self, Action.HURT)

