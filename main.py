import sys
from PyQt5.QtWidgets         import QLabel
from monstergotchi.monster   import Monster
from monstergotchi.direction import Direction
from monstergotchi.gui       import Gui

class MonsterGotchi(QLabel):
        
    def __init__(self, name=None, random=False):
        super().__init__()
        self.gui     = Gui(self)
        self.monster = Monster( self, name=name, random=random )
        self.gui.interval( 75, self.monster.update_animation ) # Temporizador para la animación
        self.gui.update( self.monster )
        self.show()
        print(f"Spawned { self.monster.name }")
     
    def mousePressEvent(self, event):
        self.gui.handleMouseEvent(event)

if __name__ == "__main__":
    app = Gui.start(sys.argv)
    pet = MonsterGotchi(random=True)
    gible    = MonsterGotchi('gible')
    garchomp = MonsterGotchi('garchomp')
    gabite   = MonsterGotchi('gabite')
    sys.exit(app.exec_())