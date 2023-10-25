from PyQt5.QtCore import QRectF, QRegExp
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QGraphicsView, QGraphicsTextItem, QStyledItemDelegate
from PyQt5.QtGui import   QFont, QRegExpValidator


   

class FloatLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        regex = QRegExp("^-?[0-9]*(\.?[0-9]*)?$")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

class MyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                border: none;
                background-color: white;
                color: #0076c0;
                font-size: 22px;
            }
        """)
class MyLabel2(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QLabel {
                border: none;
                background-color: white;
                color: black;
            }
        """)
class MyButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: white;
                color: black;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #b3dcfd;
            }
        """)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
    def resizeEvent(self, event):
        super().resizeEvent(event)        
        new_size = event.size()
        scene = self.scene()
        scene.setSceneRect(QRectF(0, 0, new_size.width(), new_size.height()))

class MyQGraphicsTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__()
        self.setPlainText(text)
        font = QFont("Arial", 12)
        self.setFont(font)
        self.setZValue(3)

class FloatDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        if index.column() != 0:  
            editor = QLineEdit(parent)
            regex = QRegExp("^[0-9]*(\.?[0-9]*)?$")
            validator = QRegExpValidator(regex)
            #validator.setNotation(QDoubleValidator.StandardNotation)
            #validator.setLocale(QLocale("en_US"))
            #validator.setDecimals(2)
            editor.setValidator(validator)
            return editor
        else:
            return super().createEditor(parent, option, index)




#Classes for all structurers, radiant surfaces and oppenings. Include main phys parametres and coordinates to calculate view factors


class Ceiling:
    def __init__(self, results, correct, tempcorrect):
        self.eps = float(results['Ceiling']['eps'])
        self.U = float(results['Ceiling']['U'])/(1-float(results['Ceiling']['U'])*0.17)
        self.Tex = float(results['Ceiling']['Tout']) + 273.15 - tempcorrect
        RL = float(results['Room']['RL']) *correct
        RW = float(results['Room']['RW']) *correct
        self.area = RL*RW
        self.coord1 = [0, RL, 0, RW]
        self.coord2 = [0, RW, 0, RL]
        self.coord3 = [0, RL, 0, RW]
        self.coord4 = [0, RW, 0, RL]

class CeilingRS:
    def __init__(self, results, num, correct, tempcorrect):
        self.eps = float(results['Ceiling']['RS'][num]['RS_eps'])
        self.TRS = float(results['Ceiling']['RS'][num]['RS_T']) + 273.15 - tempcorrect
        self.area = float(results['Ceiling']['RS'][num]['area']) * correct**2
        # F - floor, 1,2,3,4 - walls number 
        coord = {'x':float(results['Ceiling']['RS'][num]['coord']['x']) * correct, 'y':float(results['Ceiling']['RS'][num]['coord']['y']) * correct, 'W':float(results['Ceiling']['RS'][num]['coord']['W']) * correct, 'L':float(results['Ceiling']['RS'][num]['coord']['L']) * correct}
        RL = float(results['Room']['RL']) * correct
        RW = float(results['Room']['RW']) * correct
        self.coordF = [coord['x'], coord['W'] + coord['x'], coord['y'], coord['L'] + coord['y']]
        self.coord1 = [coord['y'], coord['y'] + coord['L'], coord['x'], coord['W'] + coord['x']]
        self.coord2 = [coord['x'], coord['W'] + coord['x'], RL - coord['y'] - coord['L'], RL - coord['y']]
        self.coord3 = [RL - coord['y'] - coord['L'], RL - coord['y'], RW - coord['x'] - coord['W'], RW - coord['x']]
        self.coord4 = [RW - coord['x'] - coord['W'], RW - coord['x'], coord['y'], coord['L'] + coord['y']]

class Floor:
    def __init__(self, results, correct, tempcorrect):
        self.eps = float(results['Floor']['eps'])
        self.U = float(results['Floor']['U'])/(1-float(results['Floor']['U'])*0.1)
        self.Tex = float(results['Floor']['Tout']) + 273.15 - tempcorrect
        RL = float(results['Room']['RL'])
        RW = float(results['Room']['RW'])
        self.area = RL*RW 
        self.coord1 = [0, RL, 0, RW]
        self.coord2 = [0, RW, 0, RL]
        self.coord3 = [0, RL, 0, RW]
        self.coord4 = [0, RW, 0, RL]

class FloorRS:
    def __init__(self, results, num, correct, tempcorrect):
        self.eps = float(results['Floor']['RS'][num]['RS_eps'])
        self.TRS = float(results['Floor']['RS'][num]['RS_T']) + 273.15 - tempcorrect
        self.area = float(results['Floor']['RS'][num]['area'])
        # F - floor, 1,2,3,4 - walls number 
        coord = {'x':float(results['Floor']['RS'][num]['coord']['x']) * correct, 'y':float(results['Floor']['RS'][num]['coord']['y']) * correct, 'W':float(results['Floor']['RS'][num]['coord']['W']) * correct, 'L':float(results['Floor']['RS'][num]['coord']['L']) * correct}
        RL = float(results['Room']['RL'])
        RW = float(results['Room']['RW'])
        self.coordF = [coord['x'], coord['W'] + coord['x'], coord['y'], coord['L'] + coord['y']]
        self.coord1 = [coord['y'], coord['y'] + coord['L'], coord['x'], coord['W'] + coord['x']]
        self.coord2 = [coord['x'], coord['W'] + coord['x'], RL - coord['y'] - coord['L'], RL - coord['y']]
        self.coord3 = [RL - coord['y'] - coord['L'], RL - coord['y'], RW - coord['x'] - coord['W'], RW - coord['x']]
        self.coord4 = [RW - coord['x'] - coord['W'], RW - coord['x'], coord['y'], coord['L'] + coord['y']]

class Walls:
    def __init__(self, results, name, R, correct, tempcorrect):
        self.eps = float(results[name]['eps'])
        self.U = float(results[name]['U'])/(1-float(results[name]['U'])*0.13)
        self.Tex = float(results[name]['Tout']) + 273.15 - tempcorrect
        RH = float(results['Room']['RH'])
        self.area = RH*R 
        self.coord = [0, RH, 0, R]
        self.coordCF = [0, R, 0, RH]

class WallRS:
    def __init__(self, results, name, num, R, correct, tempcorrect):
        self.eps = float(results[name]['RS'][num]['RS_eps'])
        self.TRS = float(results[name]['RS'][num]['RS_T']) + 273.15 - tempcorrect
        self.area = float(results[name]['RS'][num]['area'])
        # UP - to ceiling, L - to left wall, R - to right wall, D - to floor, OP - opposite, OPrev - reverse opposit
        # 0 - x, 1 - W, 2 - y, 3 - L
        coord = {'x':float(results[name]['RS'][num]['coord']['x']) * correct, 'y':float(results[name]['RS'][num]['coord']['y']) * correct, 'W':float(results[name]['RS'][num]['coord']['W']) * correct, 'L':float(results[name]['RS'][num]['coord']['L']) * correct}
        RH = float(results['Room']['RH'])
        self.coordUP = [coord['x'], coord['x'] + coord['W'], RH - coord['y'] - coord['L'], RH - coord['y']]
        self.coordL = [coord['y'], coord['y'] + coord['L'], coord['x'], coord['W'] + coord['x']]        
        self.coordR = [coord['y'], coord['y'] + coord['L'], R - coord['x'] - coord['W'], R - coord['x']]
        self.coordD = [coord['x'], coord['x'] + coord['W'], coord['y'], coord['y'] + coord['L']]
        self.coordOP = [coord['x'], coord['x'] + coord['W'], coord['y'], coord['y'] + coord['L']]
        self.coordOPrev = [R - coord['x'] - coord['W'], R - coord['x'], coord['y'], coord['y'] + coord['L']]

class WallOp:
    def __init__(self, results, name, num, R, correct, tempcorrect):
        self.eps =  float(results[name]['door'][num]['door_eps'])
        self.Tex = float(results[name]['Tout']) + 273.15 - tempcorrect
        self.U = float(results[name]['door'][num]['door_U'])/(1-float(results[name]['door'][num]['door_U'])*0.13)
        self.area = float(results[name]['door'][num]['area'])
        # UP - to ceiling, L - to left wall, R - to right wall, D - to floor, OP - opposite, OPrev - reverse opposit 
        RH = float(results['Room']['RH'])
        coord = {'x':float(results[name]['door'][num]['coord']['x']) * correct, 'y':float(results[name]['door'][num]['coord']['y']) * correct, 'W':float(results[name]['door'][num]['coord']['W']) * correct, 'L':float(results[name]['door'][num]['coord']['L']) * correct}
        self.coordUP = [coord['x'], coord['x'] + coord['W'], RH - coord['y'] - coord['L'], RH - coord['y']]
        self.coordL = [coord['y'], coord['y'] + coord['L'], coord['x'], coord['W'] + coord['x']]        
        self.coordR = [coord['y'], coord['y'] + coord['L'], R - coord['x'] - coord['W'], R - coord['x']]
        self.coordD = [coord['x'], coord['x'] + coord['W'], coord['y'], coord['y'] + coord['L']]
        self.coordOP = [coord['x'], coord['x'] + coord['W'], coord['y'], coord['y'] + coord['L']]
        self.coordOPrev = [R - coord['x'] - coord['W'], R - coord['x'], coord['y'], coord['y'] + coord['L']]