class Action:

    IDLE    = 0
    WALK    = 1
    ATTACK  = 2
    SPECIAL = 3
    HURT    = 4
    SLEEP   = 5
    EAT     = 6
    RESERVED= 7

    INDEX = {
        "idle"      : IDLE,
        "walk"      : WALK,
        "attack"    : ATTACK,
        "special"   : SPECIAL,
        "hurt"      : HURT,
        "sleep"     : SLEEP,
        "eat"       : EAT,
        "reserved"  : RESERVED,
    }
    NAME = {
        IDLE        : "idle",
        WALK        : "walk",
        ATTACK      : "attack",
        SPECIAL     : "special",
        HURT        : "hurt",
        SLEEP       : "sleep",
        EAT         : "eat",
        RESERVED    : "reserved",
    }
    def __init__(self, parent, action):
        self.nombre = Action.NAME[action]
        self.type   = action
        self.parent = parent
        self.sprites_db = {}  # Guarda las poses (direcciones) de esta acción específica
        # parent.monster.load_and_process_sprites( f"monstergotchi/gfx/{ parent.monster.name }-{ Action.NAME[action] }.png", self )
        parent.monster.load_and_process_sprites( f"monstergotchi/gfx/{ parent.monster.name }.png", self, action )

class ActionSet:
    def __init__(self, monster):
        self.monster = monster
        self.idle    = Action(self, Action.IDLE)
        self.walk    = Action(self, Action.WALK)
        self.attack  = Action(self, Action.ATTACK)
        self.special = Action(self, Action.SPECIAL)
        self.hurt    = Action(self, Action.HURT)
        # self.sleep   = Action(self, Action.SLEEP)
        # self.eat     = Action(self, Action.EAT)
        # self.reserved= Action(self, Action.RESERVED)

