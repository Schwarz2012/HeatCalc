from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtGui import   QColor, QPen, QBrush
from Classes_list import MyQGraphicsTextItem

#Graphics drawing
#Drawing RS and door position on wall
def graph_build(self):
    current_item = self.tree.currentIndex()
    parent_name = current_item.parent()
    self.coord_start = QGraphicsEllipseItem(-7, self.right_graphics_view.size().height()-10, 15, 15)
    self.coord_start.setBrush(QColor(255, 0, 0))
    try:
        if ('Room' in current_item.data()) == True:
            for item in self.scene.items():
                self.scene.removeItem(item)
            self.graph_text1 = MyQGraphicsTextItem('Wall 1 (Room length)')
            self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
            self.graph_text1.setRotation(270)
            self.scene.addItem(self.graph_text1)
            self.graph_text2 = MyQGraphicsTextItem('Wall 2')
            self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
            self.scene.addItem(self.graph_text2) 
            self.graph_text3 = MyQGraphicsTextItem('Wall 3')
            self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
            self.graph_text3.setRotation(90)
            self.scene.addItem(self.graph_text3)
            self.graph_text4 = MyQGraphicsTextItem('Wall 4 (Room width)')
            self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
            self.scene.addItem(self.graph_text4)

        if ('Ceiling' in parent_name.data()) == True:
            for item in self.scene.items():
                self.scene.removeItem(item)
            for num in self.RS_data[parent_name.data()]:
                self.graph_text1 = MyQGraphicsTextItem('Wall 1 (length)')
                self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                self.graph_text1.setRotation(270)
                self.scene.addItem(self.graph_text1)
                self.graph_text2 = MyQGraphicsTextItem('Wall 2')
                self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                self.scene.addItem(self.graph_text2) 
                self.graph_text3 = MyQGraphicsTextItem('Wall 3')
                self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                self.graph_text3.setRotation(90)
                self.scene.addItem(self.graph_text3)
                self.graph_text4 = MyQGraphicsTextItem('Wall 4 (Width)')
                self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                self.scene.addItem(self.graph_text4)
                self.scene.addItem(self.coord_start)
                W = float(self.main_data[parent_name.data()]['RS'][num]['coord']['W'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room']['RW'].text()))
                L = float(self.main_data[parent_name.data()]['RS'][num]['coord']['L'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RL'].text()))
                x = float(self.main_data[parent_name.data()]['RS'][num]['coord']['x'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room']['RW'].text()))
                y = self.right_graphics_view.size().height() - float(self.main_data[parent_name.data()]['RS'][num]['coord']['y'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RL'].text())) - L
                self.scene.addRect(x, y, W, L, QPen(Qt.black), QBrush(Qt.red))
        if ('Floor' in parent_name.data()) == True:
            for item in self.scene.items():
                self.scene.removeItem(item)
            for num in self.RS_data[parent_name.data()]:
                self.graph_text1 = MyQGraphicsTextItem('Wall 1 (length)')
                self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
                self.graph_text1.setRotation(270)
                self.scene.addItem(self.graph_text1)
                self.graph_text2 = MyQGraphicsTextItem('Wall 2')
                self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
                self.scene.addItem(self.graph_text2) 
                self.graph_text3 = MyQGraphicsTextItem('Wall 3')
                self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                self.graph_text3.setRotation(90)
                self.scene.addItem(self.graph_text3)
                self.graph_text4 = MyQGraphicsTextItem('Wall 4 (Width)')
                self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
                self.scene.addItem(self.graph_text4)
                self.scene.addItem(self.coord_start)
                W = float(self.main_data[parent_name.data()]['RS'][num]['coord']['W'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room']['RW'].text()))
                L = float(self.main_data[parent_name.data()]['RS'][num]['coord']['L'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RL'].text()))
                x = float(self.main_data[parent_name.data()]['RS'][num]['coord']['x'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room']['RW'].text()))
                y = self.right_graphics_view.size().height() - float(self.main_data[parent_name.data()]['RS'][num]['coord']['y'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RL'].text())) - L
                self.scene.addRect(x, y, W, L, QPen(Qt.black), QBrush(Qt.red))
        if ('Wall' in parent_name.data()) == True:
            for item in self.scene.items():
                self.scene.removeItem(item)
            R = 0
            if (int(parent_name.data()[-1])%2 == 0):
                R = 'RW'
            else: 
                R = 'RL'
            wall_num =  int(parent_name.data()[-1]) - 1
            self.graph_text1 = MyQGraphicsTextItem('Wall ' + self.wall_num_list[wall_num - 1] + ' (length)')
            self.graph_text1.setPos(0, self.right_graphics_view.size().height()/2)
            self.graph_text1.setRotation(270)
            self.scene.addItem(self.graph_text1)
            if wall_num != 3:
                self.graph_text3 = MyQGraphicsTextItem('Wall ' + self.wall_num_list[wall_num + 1])
                self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                self.graph_text3.setRotation(90)
                self.scene.addItem(self.graph_text3)
            else:
                self.graph_text3 = MyQGraphicsTextItem('Wall 1')
                self.graph_text3.setPos(self.right_graphics_view.size().width(), self.right_graphics_view.size().height()/2-25)
                self.graph_text3.setRotation(90)
                self.scene.addItem(self.graph_text3)
            self.graph_text2 = MyQGraphicsTextItem('Ceiling')
            self.graph_text2.setPos(self.right_graphics_view.size().width()/2, 0)
            self.scene.addItem(self.graph_text2) 
            self.graph_text4 = MyQGraphicsTextItem('Floor (Width)')
            self.graph_text4.setPos(self.right_graphics_view.size().width()/2, self.right_graphics_view.size().height()-30)                    
            self.scene.addItem(self.graph_text4)
            self.scene.addItem(self.coord_start)
            try:
                for num in self.RS_data[parent_name.data()]:
                    W = float(self.main_data[parent_name.data()]['RS'][num]['coord']['W'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room'][R].text()))
                    H = float(self.main_data[parent_name.data()]['RS'][num]['coord']['L'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RH'].text()))
                    x = float(self.main_data[parent_name.data()]['RS'][num]['coord']['x'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room'][R].text()))
                    y = self.right_graphics_view.size().height() - float(self.main_data[parent_name.data()]['RS'][num]['coord']['y'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RH'].text())) - H
                    self.scene.addRect(x, y, W, H, QPen(Qt.black), QBrush(Qt.red))
            except ValueError:
                next
            for num in self.door_data[parent_name.data()]:
                    W = float(self.main_data[parent_name.data()]['door'][num]['coord']['W'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room'][R].text()))
                    H = float(self.main_data[parent_name.data()]['door'][num]['coord']['L'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RH'].text()))
                    x = float(self.main_data[parent_name.data()]['door'][num]['coord']['x'].text())*(self.right_graphics_view.size().width()/float(self.main_data['Room'][R].text()))
                    y = self.right_graphics_view.size().height() - float(self.main_data[parent_name.data()]['door'][num]['coord']['y'].text())*(self.right_graphics_view.size().height()/float(self.main_data['Room']['RH'].text())) - H
                    self.scene.addRect(x, y, W, H, QPen(Qt.black), QBrush(Qt.blue))
    except (ValueError, TypeError):
        return() 
