from .position          import Position
from .direction         import Direction
from PyQt5.QtWidgets    import QApplication
from PyQt5.QtCore       import Qt, QTimer
from PyQt5.QtGui        import QPixmap, QImage
 
class Gui:

    SCALE_FACTOR   = 2 
    TASKBAR_HEIGHT  = 30

    def start(argv):
        return QApplication(argv)
    
    def __init__(self, app):
        self.app            = app        
        self.app.fps        = 75
        self.createWindow()
        self.getGeometry()
    
    def createWindow(self):
        self.app.setWindowFlags(
            self.app.windowFlags() | 
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.app.setAttribute(Qt.WA_TranslucentBackground)
        
    
    def getGeometry(self):
        self.screen_size = Position(
            QApplication.primaryScreen().size().width(),
            QApplication.primaryScreen().size().height()
        )

    def pillow_to_qpixmap(self, pil_img, width, height):
        # Transforma el formato binario de Pillow a un búfer de memoria de PyQt sin perder calidad
        bytes_img = pil_img.tobytes("raw", "RGBA")
        qimg = QImage(bytes_img, pil_img.size[0], pil_img.size[1], QImage.Format_RGBA8888)
        # Escalado Point (Nearest Neighbor) para mantener los píxeles nítidos y sin borrosidad
        pixmap = QPixmap.fromImage(qimg).scaled(width, height, Qt.KeepAspectRatio, Qt.FastTransformation)
        return pixmap

    def handleKeyboardEvent(self, event):
        pass

    def handleMouseEvent(self, event):
        # Detecta si el clic fue con el botón izquierdo del ratón
        if event.button() == Qt.LeftButton:
            print("¡Has hecho clic en el pokémon!")
            # Aquí puedes añadir más lógica, como reproducir un sonido o cambiar de acción
        
    def interval(self, rate, callback):
        self.timer = QTimer()
        self.timer.timeout.connect( callback )
        self.timer.start( rate )  

    def update(self, monster):
        # Renderiza el frame actual en pantalla buscando en la acción actual
        pixmap = monster.action.sprites_db[ Direction.NAME[monster.direction] ][ monster.current_frame ]
        self.app.setPixmap( pixmap )
        
