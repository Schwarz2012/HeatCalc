from PyQt5.QtCore import Qt



def area_calc(self, tree):
    try:
        current_name = tree.currentIndex().parent().data()
        if ('Radiant' in tree.currentIndex().data()) == True:
            node = 'RS'
        else:
            node = 'door'
        num = tree.currentIndex().data()[-1]
        W = self.main_data[current_name][node][num]['coord']['W'].text()
        H = self.main_data[current_name][node][num]['coord']['L'].text()
        self.main_data[current_name][node][num]['area'].setText(str(round(float(W)*float(H), 2)))      
    except ValueError:
        return()

#U calculation from layers table data
def U_calc_layer_data(self, name):
    try:
        if name == None:
            current_name = self.tree.currentIndex().data()
        else:
            current_name = name
        R_in_surf_coef = {'Ceiling': 0.17, 'Floor': 0.1, 'Wall 1': 0.13, 'Wall 2': 0.13, 'Wall 3': 0.13, 'Wall 4': 0.13}
        R_ex_surf_coef = {'Ceiling': 0.1, 'Floor': 0.17, 'Wall 1': 0.13, 'Wall 2': 0.13, 'Wall 3': 0.13, 'Wall 4': 0.13} #?
        if self.out_condiition_box[current_name].currentIndex() == 0:           
            out_alfa = R_ex_surf_coef[current_name]
        else:
            out_alfa = float(self.out_condiition_value[current_name].text())
        if self.water_switch[current_name] == True:
            self.main_data[current_name]['U'].setReadOnly(True)
            self.table_name = self.water_table[current_name]
            total_R = 0
            layers_list = []
            for current_row in range(self.table_name.rowCount()):
                layers_par_list = []
                item = self.table_name.item(current_row, 1).text()
                layers_par_list.append(float(item))
                item = self.table_name.item(current_row, 2).text()
                layers_par_list.append(float(item))
                layers_list.append(layers_par_list)
            for parameter in layers_list:
                total_R += (parameter[0]/1000)/parameter[1]
            U_water = str(round(1/(total_R + out_alfa + R_in_surf_coef[current_name]), 3))
            self.main_data[current_name]['U'].setText(U_water)
            return U_water
        else:
            self.main_data[current_name]['U'].setReadOnly(False)
    except (KeyError, ZeroDivisionError, ValueError):
        return()


def adsource_enable(self):
    if (self.convection_box.currentIndex() == 1) and (self.tree.currentIndex().data() == 'Room'): 
        self.central_grid.addWidget(self.Adsource_label, 4,0)
        self.central_grid.addWidget(self.Adsource, 4,1)
        self.central_grid.addWidget(self.Adsource_unit, 4,2)
    else:
        self.Adsource_label.setParent(None)
        self.Adsource.setParent(None)
        self.Adsource_unit.setParent(None)

def water_out_condition_status(self):
    try:

        current_name = self.tree.currentIndex()   
        parent_name = current_name.parent()
        base_parent_name = parent_name.parent().data()
        R_surf_coef = {'Ceiling': 0.1, 'Floor': 0.17, 'Wall 1': 0.13, 'Wall 2': 0.13, 'Wall 3': 0.13, 'Wall 4': 0.13}
        self.out_condiition_value[base_parent_name].setReadOnly(True)
        if self.out_condiition_box[base_parent_name].currentIndex() == 0: 
            self.out_condiition_label[base_parent_name].setText('External temperature')
            self.out_condiition_value_box[base_parent_name].setParent(None)
            self.out_condiition_value[base_parent_name].setText(self.main_data[base_parent_name]['Tout'].text())
            self.out_condiition_unit[base_parent_name].setText(self.temp_box.currentText())
        else:
            self.out_condiition_label[base_parent_name].setText('External resistance')
            self.central_grid.addWidget(self.out_condiition_value_box[base_parent_name], 2,2, alignment=Qt.AlignLeft)
            if self.out_condiition_value_box[base_parent_name].currentIndex() == 0:
                self.out_condiition_value[base_parent_name].setText(str(R_surf_coef[base_parent_name]))
            else:   
                self.out_condiition_value[base_parent_name].setReadOnly(False)
                self.out_condiition_value[base_parent_name].setText(self.last_alfa_water[base_parent_name])                  
            self.out_condiition_unit[base_parent_name].setText('(m²*K)/W')
    except (KeyError, ZeroDivisionError):
        return()

def water_alfa_last_value(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent()
    base_parent_name = parent_name.parent().data()
    if self.out_condiition_value_box[base_parent_name].currentText() == 'User defined': 
        self.last_alfa_water[base_parent_name] = self.out_condiition_value[base_parent_name].text()

def alpha_value(self):
    name = self.tree.currentIndex().data()
    if self.alpha_box[name].currentIndex() == 0: 
        if ('Wall' in name) == True:
            self.main_data[name]['alpha'].setText('0.13')
        elif ('Floor' in name) == True:
            self.main_data[name]['alpha'].setText('0.1')
        elif ('Ceiling' in name) == True:
            self.main_data[name]['alpha'].setText('0.17')
        self.main_data[name]['alpha'].setReadOnly(True)
    else:
        self.main_data[name]['alpha'].setReadOnly(False)

def zero_alpha_control(self):
    name = self.tree.currentIndex().data()
    if (self.main_data[name]['alpha'].text() == '0') or (self.main_data[name]['alpha'].text() == '') or (self.main_data[name]['alpha'].text()[-1].isdigit() == False ):
        self.main_data[name]['alpha'].setStyleSheet("background-color: red;")
    else:
        self.main_data[name]['alpha'].setStyleSheet("background-color: white;")

def top_U_control(self):
    name = self.tree.currentIndex().data()
    try:
        if (self.main_data[name]['U'].text() == '') or (float(self.main_data[name]['U'].text()) > 5.5) or (float(self.main_data[name]['U'].text()) < 0):
            self.main_data[name]['U'].setStyleSheet("background-color: red;")
        else:
            self.main_data[name]['U'].setStyleSheet("background-color: white;")
    except ValueError:
        return