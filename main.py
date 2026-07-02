import sys
from PyQt5.QtWidgets         import *
from monstergotchi.monster   import Monster
from monstergotchi.direction import Direction
from monstergotchi.position  import Position
from monstergotchi.gui       import Gui
from monstergotchi.action    import Action

UNDER   = "⁰¹²³⁴⁵⁶⁷⁸⁹"

def under(number):
    text = str(number)
    return "".join([UNDER[int(x)] for x in text])

__BAR_DATA = "▁▂▃▄▅▆▇█" 
def bar(current, max):
    parts = int((current / max)*8)
    return __BAR_DATA[parts & 7]
    
SEXOS = '♀ ♂'

__PROGRESS_DATA = "◗◖◕◔◓◒◑◐"
# __PROGRESS_DATA = "▏▎▍▌▋▊▉█"
def progress(current, max, width=8):
    # Como vamos a dividir cada casilla a lo largo de width(8) en 8 estados de relleno (BLOCKS),
    # calculamos el numero de bloques que necesitamos, junto con el 'resto' y lo redondeamos a entero
    parts = int( (current / max) * width * 8)
    # imprimimos el numero de bloques que toque, añadiendo al final un bloque extra con el bloque parcial
    # ocupando todo como mucho width (8), y sin bordes 
    return padded(__PROGRESS_DATA[ 7 ] * int( parts / 8 ) + __PROGRESS_DATA[parts & 7], width ,'')

class Monitor(QMainWindow):
    def __init__(self, target=None):
        super().__init__()
        Gui.createMonitorWindow(self)
        self.target = None
        self.position = Position(0,0)
        self.size     = Position(160,144)
        self.setGeometry(
            self.position.x, 
            self.position.y,
            self.size.x, 
            self.size.y
        )        
        self.show()
        print("Created Monitor")
        self.timer = Gui.interval( 250, self.update ) 
        if not target: return
        self.select(target.monster)

    
    def update(self):
        if self.target:
            self.select(self.target)
            self.show()
        else:
            self.hide()

    def move(self, x, y):
        self.position.set(x,y)
        self.setGeometry(
            self.position.x, 
            self.position.y,
            self.size.x, 
            self.size.y
        )        
        
    def printLine(self, line_index, text):
        self.lines[line_index].setText(padded(text))
        
    def select(self, monster):
        self.target = monster
        self.setWindowTitle(f'{monster.name} stats')
        self.printLine( 1, f'{monster.name.upper()} {SEXOS[monster.stats.sex+1]} LV.{under(monster.stats.level)}')
        self.printLine( 3, f'{padded(Action.NAME[monster.action.type], 9,'')}┊ VIT { monster.stats.vitality    }')
        self.printLine( 4, f' ☺ ♥ ✓ ☑ ┊ STR { monster.stats.strength    }')
        self.printLine( 5, f' {bar(monster.stats.xp, monster.stats.xp_next)} {bar(monster.stats.xp, monster.stats.xp_next)} {bar(monster.stats.xp, monster.stats.xp_next)}   ┊ DEF { monster.stats.defense     }')
        self.printLine( 6, f' ☹ ☠ ✗ ☐ ┊ SPC { monster.stats.special     }')
        self.printLine( 7, f'▲▼▶◀‣    ┊ SPD { monster.stats.speed       }')
        self.printLine( 8, f'         ┊ EVA { monster.stats.evasion     }')
        # self.printLine(10, f'XP { monster.stats.xp          }/{ monster.stats.xp_next}')
        self.printLine(10, f'XP { progress(monster.stats.xp, monster.stats.xp_next, 15)}')
        self.move(
            monster.app.gui.screen_size.x - 160, 
            monster.app.gui.screen_size.y - ( 144 + Gui.TASKBAR_HEIGHT ), 
        )
    
    def mousePressEvent(self, event):
        pass

def padded(text, count=18, border='║'):
    return f'{border}{text[0:count]}{(count-len(text))*' '}{border}'
    
class MonsterGotchi(QLabel):
        
    def __init__(self, name=None, randomize=False):
        super().__init__()
        global monitor
        self.gui     = Gui(self)
        self.monitor = monitor
        self.monster = Monster( self, name=name, randomize=randomize )
        self.timer   = Gui.interval( self.fps, self.monster.update_animation ) # Temporizador para la animación
        self.gui.update( self.monster )
        self.show()
        print(f"Spawned { self.monster.name }")
     
    def mousePressEvent(self, event):
        self.gui.handleMouseEvent(event)
        monitor.select(self.monster)

if __name__ == "__main__":
    global monitor
    app = Gui.start(sys.argv)
    monitor  = Monitor()
    pet      = MonsterGotchi(randomize=True)
    gible    = MonsterGotchi('gible')
    garchomp = MonsterGotchi('garchomp')
    gabite   = MonsterGotchi('gabite')
    gastly   = MonsterGotchi('gastly')
    gengar   = MonsterGotchi('gengar')
    sys.exit(app.exec_())