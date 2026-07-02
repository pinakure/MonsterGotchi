from .position          import Position
from .direction         import Direction
from PyQt5.QtWidgets    import QApplication, QLabel
from PyQt5.QtCore       import Qt, QTimer
from PyQt5.QtGui        import QPixmap, QImage, QFontDatabase, QFont
 
class Gui:

    SCALE_FACTOR    = 2
    TASKBAR_HEIGHT  = 30

    def start(argv):
        return QApplication(argv)
    
    def __init__(self, app):
        self.app            = app        
        self.app.fps        = 30
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
        
    def createMonitorWindow(app):
        app.setWindowFlags(
            app.windowFlags() | 
            Qt.FramelessWindowHint #| 
            #Qt.WindowStaysOnTopHint | 
            # Qt.Tool |
            #Qt.WindowType.WindowStaysOnTopHint
        )
        # app.setAttribute(Qt.WA_TranslucentBackground)
        font_id   = QFontDatabase.addApplicationFont("monstergotchi/gfx/unifont.ttf")
        if font_id == -1:
            print("Error: No se pudo cargar la fuente.")
            font_name = "Arial" # Fuente de respaldo por si falla
        else:
            familias  = QFontDatabase.applicationFontFamilies(font_id)
            font_name = familias[0]
        font = QFont( font_name, 12) 
        app.lines = [
            QLabel('╔══════════════════╗', app),
            QLabel('║                  ║', app),
            QLabel('╟─────────┬────────╢', app),
            QLabel('║         ┆        ║', app),
            QLabel('║         ┆        ║', app),
            QLabel('║         ┆        ║', app),
            QLabel('║         ┆        ║', app),
            QLabel('║         ┆        ║', app),
            QLabel('║         ┆        ║', app),
            QLabel('╟─────────┴────────╢', app),
            QLabel('║                  ║', app),
            QLabel('╚══════════════════╝', app),
        ]
        [x.setGeometry(-1,-1+(i*12), 161, 12) for i,x in enumerate(app.lines)]
        [x.setFont(font) for x in app.lines]
        # app.lines[0].setBack

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
    
    def filter_pink(self, frame_img):
        # Filtrar tu máscara fucsia exacta (255, 0, 255) a transparencia total
        datas = frame_img.getdata()
        new_data = []
        for item in datas:
            if item[0] == 255 and item[1] == 0 and item[2] == 255:
                new_data.append((0, 0, 0, 0))  # Transparente real
            else:
                new_data.append(item)
        frame_img.putdata(new_data)
        return frame_img

    def handleKeyboardEvent(self, event):
        pass

    def handleMouseEvent(self, event):
        # Detecta si el clic fue con el botón izquierdo del ratón
        if event.button() == Qt.LeftButton:
            print("¡Has hecho clic en el pokémon!")
            # Aquí puedes añadir más lógica, como reproducir un sonido o cambiar de acción
        
    def interval(rate, callback):
        timer = QTimer()
        timer.timeout.connect( callback )
        timer.start( rate )  
        return timer
    
    def update(self, monster):
        # Renderiza el frame actual en pantalla buscando en la acción actual
        pixmap = monster.action.sprites_db[ Direction.NAME[monster.direction] ][ int(monster.current_frame) ]
        self.app.setPixmap( pixmap )
        
