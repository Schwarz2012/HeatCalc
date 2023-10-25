from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QTableWidgetItem
import Calculation as calc
import cap_stdy as cs
from Collect_data import collect

#Results
#Calculation
def results(self):    
    self.settings_label.setText('Calculate...')     
    QCoreApplication.processEvents()
    self.Calcresult = 0
    #Calculation
    try:
        self.user_data = collect(self)
        if self.result['RS_number'] == False:
            self.settings_label.setText('Please add at least one Radiant surface')
            return
        else:
            del self.result['RS_number']
            del self.result['temp_box']
            del self.result['unit_box']
            self.Calcresult = calc.calculation(self, self.user_data)

        #Water calc
        self.water_temp_result = {}
        self.water_temp_mask_result = {}
        for current_name in self.construct_list:
            if self.water_switch[current_name] == True:
                geo_list = self.user_data[current_name]['Water_calc'][0].copy()
                float_list = []
                layer_list  =[]
                geo = []
                for lists in geo_list:
                    float_list = []
                    float_list.append(float(lists[1]))
                    float_list.append(float(lists[2]))
                    if isinstance(lists[3], list):
                        layer_list  =[]
                        for value in lists[3]:
                            layer_list.append(float(value))
                        float_list.append(layer_list)
                    geo.append(float_list) 

                width = float(self.mat_step_box[current_name].currentText())/2
                t_to_fit = float(self.user_data[current_name]['RS'][list(self.user_data[current_name]['RS'].keys())[0]]['RS_T'])        
                q = float(self.Calcresult['Heat']['RS flux'][current_name])
                t_top = float(self.Calcresult['TemperaturesOut'][current_name])
                if self.out_condiition_box[current_name].currentText() == 'Temperature':
                    l_top = None
                else:
                    l_top = float(self.out_condiition_value[current_name].text())
                self.water_temp_result[current_name]  = round(cs.fit_water_t(self, geo, width, t_to_fit, q, t_top, l_top), 1)
    except (ValueError, KeyError, IndexError, AttributeError, TypeError, ZeroDivisionError, UnboundLocalError):
        self.settings_label.setText('Set all data in parametres')
        return() 
    #Clear data
    self.result_table.clearContents()
    self.result_table.setRowCount(0)
    self.result_table.setColumnCount(0)
    #New data
    row_num = 0
    self.result_table.setColumnCount(3)
    self.result_table.setRowCount(len(self.Calcresult['Temperatures']))          
    self.result_table.verticalHeader().setVisible(False)
    header_labels = ['Structure', 'Internal temperatures, \u00b0C', 'External temperatures, \u00b0C']
    self.result_table.setHorizontalHeaderLabels(header_labels)
    for key in self.Calcresult['Temperatures']:
        self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
        self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Temperatures'][key])))           
        if key != 'Air room temperature':
            self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['TemperaturesOut'][key])))
        row_num +=1
    self.result_table.resizeColumnsToContents()
    self.settings_label.setText('Last calculation time: ' + self.Calcresult['Solution time'] + ' sec') 

#Temperature results
def temp_results(self):
    try:
        if (self.Calcresult != 0):
            #Clear data
            self.result_table.clearContents()
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            #New data
            row_num = 0
            self.result_table.setColumnCount(3)
            self.result_table.setRowCount(len(self.Calcresult['Temperatures']))          
            self.result_table.verticalHeader().setVisible(False)
            header_labels = ['Structure', 'Internal temperatures, \u00b0C', 'External temperatures, \u00b0C']
            self.result_table.setHorizontalHeaderLabels(header_labels)
            for key in self.Calcresult['Temperatures']:
                self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Temperatures'][key])))
                if key != 'Air room temperature':
                    self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['TemperaturesOut'][key])))
                row_num +=1
            self.result_table.resizeColumnsToContents()
    except AttributeError:
        return()    
#Heat balance results

def HB_results(self):
    try:
        if (self.Calcresult != 0):
            #Clear data
            self.result_table.clearContents()
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            #New data
            row_num = 0
            self.result_table.setColumnCount(9)
            self.result_table.setRowCount(len(self.Calcresult['Heat']['RS flux']))          
            self.result_table.verticalHeader().setVisible(False)
            header_labels = ['Structure', 'Radiant source, W', 'Radiant source flux, W/m\u00b2', 'Heat transfer source, W', 'Heat transfer flux, W', 'Additional source, W', 'Total source, W', 'Total flux, W', 'Heat losses, W']
            self.result_table.setHorizontalHeaderLabels(header_labels)
            for key in self.Calcresult['Heat']['RS flux']:
                self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                self.result_table.setItem(row_num, 1, QTableWidgetItem(str(self.Calcresult['Heat']['RS power'][key])))
                self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.Calcresult['Heat']['RS flux'][key])))               
                self.result_table.setItem(row_num, 3, QTableWidgetItem(str(self.Calcresult['Heat']['Conv power'][key])))
                self.result_table.setItem(row_num, 4, QTableWidgetItem(str(self.Calcresult['Heat']['Conv flux'][key])))
                self.result_table.setItem(row_num, 5, QTableWidgetItem(str(self.Calcresult['Heat']['Add power'][key])))
                self.result_table.setItem(row_num, 6, QTableWidgetItem(str(self.Calcresult['Heat']['Total power'][key])))
                self.result_table.setItem(row_num, 7, QTableWidgetItem(str(self.Calcresult['Heat']['Total flux'][key])))
                self.result_table.setItem(row_num, 8, QTableWidgetItem(str(self.Calcresult['Losses'][key])))
                row_num +=1
            self.result_table.resizeColumnsToContents()
    except AttributeError:
        return()  

#Water temperature
def WT_results(self):
    try:
        if self.water_temp_result != 0:
            #Clear data
            self.result_table.clearContents()
            self.result_table.setRowCount(0)
            self.result_table.setColumnCount(0)
            #New data
            row_num = 0
            self.result_table.setColumnCount(3)               
            self.result_table.setRowCount(len(self.water_temp_result))          
            self.result_table.verticalHeader().setVisible(False)
            header_labels = ['Mat position','Surface temperature, \u00b0C' , 'Water temperature, \u00b0C']
            self.result_table.setHorizontalHeaderLabels(header_labels)
            for key in self.water_temp_result:
                self.result_table.setItem(row_num, 0, QTableWidgetItem(key))
                self.result_table.setItem(row_num, 1, QTableWidgetItem(self.user_data[key]['RS'][list(self.user_data[key]['RS'].keys())[0]]['RS_T']))
                self.result_table.setItem(row_num, 2, QTableWidgetItem(str(self.water_temp_result[key])))
                row_num +=1
            self.result_table.resizeColumnsToContents()
    except AttributeError:
        return()  
