from Front_calculations import U_calc_layer_data


def collect(self):
        geomunits = self.unit_box.currentText()
        if geomunits == 'm':
            correct = 1
        elif geomunits == 'cm':
            correct = 0.01
        elif geomunits == 'mm':
            correct = 0.001
        tempunits = self.temp_box.currentText()   
        #Collect data
        self.result = {}
        #Room
        self.result['Room'] = {'RL': (self.main_data['Room']['RL'].text()), 'RW': (self.main_data['Room']['RW'].text()), 'RH': (self.main_data['Room']['RH'].text())}
        #Constructions
        self.result['RS_number'] = False
        #Doors
        #Collecting
        for name in self.construct_list:
            self.result[name] = {}
            for data in self.main_data[name]:
                if data == 'alpha': 
                    if self.convection_box.currentIndex() == 1:
                        self.result['Room']['Adsource'] = (self.Adsource.text())
                        self.result[name][data] = self.main_data[name][data].text()
                elif (data == 'RS') or (data == 'door'):
                    self.result[name][data] = {}
                    for num in self.main_data[name][data]:
                        self.result['RS_number'] = True
                        self.result[name][data][num] = {}
                        for value in self.main_data[name][data][num]:
                            if value != 'coord':
                                self.result[name][data][num][value] = self.main_data[name][data][num][value].text()
                            else:
                                self.result[name][data][num][value] = {}
                                for coord in self.main_data[name][data][num][value]:
                                    if self.main_data[name][data][num][value][coord].text() != '':
                                        self.result[name][data][num][value][coord] = str(float(self.main_data[name][data][num][value][coord].text())*correct)
                                    else:
                                        self.result[name][data][num][value][coord] = self.main_data[name][data][num][value][coord].text()
                else:
                    if (data == 'U') and (self.water_switch[name] == True):
                        self.result[name][data] = U_calc_layer_data(self, name)
                        
                    else:
                        self.result[name][data] = self.main_data[name][data].text()

        for current_name in self.construct_list:
            if self.water_switch[current_name] == True:
                geo = []
                table_name = self.water_table[current_name]
                self.result[current_name]['Water_calc'] = {}
                for current_row in range(table_name.rowCount()):
                    layer_list = []
                    cap_mat_list = []
                    for col_num in range(0,4,1):
                        item = table_name.item(current_row, col_num).text()
                        if (col_num == 3) and (item != ''):
                            cap_mat_list.append(str(float(self.mat_diam_box[current_name].currentText())  / 2 - 0.2))
                            cap_mat_list.append(str(float(self.mat_diam_box[current_name].currentText()) / 2))
                            cap_mat_list.append((item))
                            cap_mat_list.append('0.22')
                            layer_list.append(cap_mat_list)
                        else:
                            layer_list.append((item))
                    geo.append(layer_list)  
                    

                self.result[current_name]['Water_calc'] = [geo, (self.mat_step_box[current_name].currentIndex()), self.out_condiition_box[current_name].currentIndex(), self.out_condiition_value_box[current_name].currentIndex(), self.out_condiition_value[current_name].text(), self.mat_diam_box[current_name].currentIndex()]      
        self.result['unit_box'] = self.unit_box.currentIndex()
        self.result['temp_box'] = self.temp_box.currentIndex()
        return(self.result)