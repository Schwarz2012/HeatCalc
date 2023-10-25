from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QComboBox, QTreeWidgetItem, QAbstractItemView
from PyQt5.QtGui import  QPen, QBrush
from Classes_list import FloatLineEdit, MyLabel2, FloatDelegate
from Front_calculations import area_calc
from Draw_function import graph_build
from Table_functions import update_button_states, offset_check
from Front_calculations import water_out_condition_status, water_alfa_last_value


def Door_create(self, tree):            
    current_name = tree.currentIndex().data()  
    if len(self.door_data[current_name]) == 0:
        self.door_num[current_name] = 0
    self.door_num[current_name] +=1
    num = str(self.door_num[current_name])
    Door_generate(self, tree, current_name, num)


def Door_generate(self, tree, current_name, num):            
    self.node['door'][current_name][num] = QTreeWidgetItem(self.node[current_name], ['Door/window ' + num])
    self.node[current_name].setExpanded(True)
    self.main_data[current_name]['door'][num] = {}
    self.main_data[current_name]['door'][num]['coord'] = {}
    for coord in self.coord_list:  
        self.main_data[current_name]['door'][num]['coord'][coord] = FloatLineEdit()
        self.main_data[current_name]['door'][num]['coord'][coord].textEdited.connect(lambda: area_calc(self, tree))
        self.main_data[current_name]['door'][num]['coord'][coord].textEdited.connect(lambda: graph_build(self))
    self.main_data[current_name]['door'][num]['area'] = MyLabel2('')
    self.main_data[current_name]['door'][num]['door_eps'] = FloatLineEdit()
    self.main_data[current_name]['door'][num]['door_eps'].setText('0.9')
    self.main_data[current_name]['door'][num]['door_U'] = FloatLineEdit()
    self.door_data[current_name].append(num)

def RS_create(self, tree): 
    current_name = self.tree.currentIndex().data()  
    if len(self.RS_data[current_name]) == 0:
        self.RS_num[current_name] = 0
    self.RS_num[current_name] +=1
    num = str(self.RS_num[current_name])
    RS_generate(self, tree, current_name, num)

def RS_generate(self, tree, current_name, num): 
    self.node['RS'][current_name][num] = QTreeWidgetItem(self.node[current_name], ['Radiant Surface ' + num])
    self.node[current_name].setExpanded(True)
    self.main_data[current_name]['RS'][num] = {}
    self.main_data[current_name]['RS'][num]['coord'] = {}
    for coord in self.coord_list:  
        self.main_data[current_name]['RS'][num]['coord'][coord] = FloatLineEdit()
        self.main_data[current_name]['RS'][num]['coord'][coord].textEdited.connect(lambda: area_calc(self, tree))
        self.main_data[current_name]['RS'][num]['coord'][coord].textEdited.connect(lambda: graph_build(self))
    self.main_data[current_name]['RS'][num]['area'] = MyLabel2('')
    self.main_data[current_name]['RS'][num]['RS_eps'] = FloatLineEdit()
    self.main_data[current_name]['RS'][num]['RS_eps'].setText('0.9')
    self.main_data[current_name]['RS'][num]['RS_T'] = FloatLineEdit()
    self.RS_data[current_name].append(num)
    if self.water_switch[current_name] == True:
        num = self.RS_data[current_name][-1]
        self.node['water'][current_name].parent().takeChild(self.node['water'][current_name].parent().indexOfChild(self.node['water'][current_name]))
        self.node['water'][current_name] = QTreeWidgetItem(self.node['RS'][current_name][num], ['Calculate water temperature'])
        self.node['RS'][current_name][num].setExpanded(True)   


def Delete(self, tree, curent_item):
    if curent_item == None:
        child = tree.currentItem()
        current_name = tree.currentIndex().data()
        parent_name = tree.currentIndex().parent().data()  
    else:
        child = curent_item
        current_name = child.text(0)
        parent_name = child.parent().text(0)

    num = current_name[-1]
    parent = child.parent()
    index = parent.indexOfChild(child)

    if ('Radiant' in current_name) == True:
        self.RS_data[parent_name].remove(num)
        del self.main_data[parent_name]['RS'][str(num)]
        if (len(self.RS_data[parent_name]) == 0) and (self.water_switch[parent_name] == True):
            self.water_switch[parent_name] = False
            parent.takeChild(parent.indexOfChild(self.node['water'][parent_name]))
        elif (len(self.RS_data[parent_name]) != 0) and (self.water_switch[parent_name] == True):
            num = self.RS_data[parent_name][-1]
            self.node['water'][parent_name].parent().takeChild(self.node['water'][parent_name].parent().indexOfChild(self.node['water'][parent_name]))
            self.node['water'][parent_name] = QTreeWidgetItem(self.node['RS'][parent_name][num], ['Calculate water temperature'])
            self.node['RS'][parent_name][num].setExpanded(True)
    elif ('Door' in current_name) == True:
        self.door_data[parent_name].remove(current_name[-1])
        del self.main_data[parent_name]['door'][str(num)]
    elif ('Water' in current_name) == True:
        self.water_switch[tree.currentIndex().parent().parent().data()] = False
    parent.takeChild(index)




def water_create(self, tree):            
    current_name = tree.currentIndex()   
    parent_name = current_name.parent().data()
    if self.water_switch[parent_name] == False:
        self.water_switch[parent_name] = True
        num = self.RS_data[parent_name][-1]
        self.node['water'][parent_name] = QTreeWidgetItem(self.node['RS'][parent_name][num], ['Calculate water temperature'])
        self.node['RS'][parent_name][num].setExpanded(True)    
        self.mat_step_box[parent_name]  = QComboBox()
        for item in range(10, 70, 10):
            self.mat_step_box[parent_name].addItem(str(item))  
        self.mat_step_box[parent_name].setFixedWidth(45)
        self.mat_diam_box[parent_name] = QComboBox()
        self.mat_diam_box[parent_name].addItem('3.4')
        self.mat_diam_box[parent_name].addItem('4.3')
        self.mat_diam_box[parent_name].currentIndexChanged.connect(lambda: offset_check(self, parent_name))
        self.mat_diam_box[parent_name].setFixedWidth(45)
        self.out_condiition_box[parent_name] = QComboBox()
        self.out_condiition_box[parent_name].addItem('Temperature')
        self.out_condiition_box[parent_name].addItem('Convection')
        self.out_condiition_box[parent_name].currentIndexChanged.connect(lambda: water_out_condition_status(self))
        self.out_condiition_box[parent_name].setFixedWidth(90)
        self.out_condiition_value_box[parent_name] = QComboBox()
        self.out_condiition_value_box[parent_name].addItem('Physics control')
        self.out_condiition_value_box[parent_name].addItem('User defined')
        self.out_condiition_value_box[parent_name].currentIndexChanged.connect(lambda: water_out_condition_status(self))
        self.out_condiition_value_box[parent_name].setFixedWidth(80)
        self.out_condiition_label[parent_name] = MyLabel2('')
        self.out_condiition_unit[parent_name] = MyLabel2('')
        self.out_condiition_value[parent_name] = FloatLineEdit()
        self.out_condiition_value[parent_name].setFixedWidth(90)
        self.out_condiition_value[parent_name].textEdited.connect(lambda: water_alfa_last_value(self))
        self.water_table[parent_name] = QTableWidget()
        self.water_table[parent_name].setColumnCount(4)
        self.water_table[parent_name].setItemDelegate(FloatDelegate())
        self.water_table[parent_name].setHorizontalHeaderLabels(["Name", "Thickness, mm", "Lambda, W/mK", "Mat offset, mm"])
        #self.water_table[parent_name].setEditTriggers(QTableWidget.AnyKeyPressed | QTableWidget.DoubleClicked)
        self.water_table[parent_name].setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.water_table[parent_name].verticalHeader().setVisible(False)
        #self.water_table[parent_name].itemChanged.connect(lambda: offset_check(self, parent_name))
        self.water_table[parent_name].itemSelectionChanged.connect(lambda: offset_check(self, parent_name))
        self.water_table[parent_name].itemSelectionChanged.connect(lambda: update_button_states(self))    
        
    else:
        return()


    #Drawing layers in water calculation
def construct_layers(self):  
    for item in self.scene.items():
        self.scene.removeItem(item)
    parent_name = self.tree.currentIndex().parent().parent().data()
    W = self.right_graphics_view.size().width()
    H = self.right_graphics_view.size().height()-10
    try:
        self.table_name = self.water_table[parent_name]
        i = 0
        layers_list = []
        mat_list = []
        r2 = 3.4
        for current_row in range(self.table_name.rowCount()):
            item = self.table_name.item(current_row, 1).text()
            layers_list.append(float(item))
            mat = self.table_name.item(current_row, 3).text()
            mat_list.append(mat)
        construct_thickness = sum(layers_list)
        coefficient = H/construct_thickness
        for layer_thickness in layers_list: 
            self.scene.addRect(W/4, H-layer_thickness*coefficient, W/2, layer_thickness*coefficient, QPen(Qt.black), QBrush(Qt.gray))
            if mat_list[i] !='':
                cap_offset = float(mat_list[i])
                self.scene.addRect(W/4, H-(r2 + cap_offset)*coefficient, W/2, r2*coefficient, QPen(Qt.black), QBrush(Qt.blue))
            H -= layer_thickness*coefficient
            i += 1
    except (ZeroDivisionError, KeyError):
        return()