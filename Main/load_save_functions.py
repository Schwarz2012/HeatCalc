from pandas import ExcelWriter, DataFrame
from PyQt5.QtWidgets import QPushButton, QFileDialog, QTableWidgetItem, QMessageBox, QDialog, QVBoxLayout, QDesktopWidget, QLabel
from PyQt5.QtGui import QFont
from Collect_data import collect
from json import dump, load
from Top_buttons_commands import RS_generate, Delete, water_create, Door_generate
from Classes_list import MyLabel, MyLabel2


def export_results(self):
    try:
        if self.Calcresult != 0:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_dialog = QFileDialog()
            file_dialog.setOptions(options)
            file_dialog.setWindowTitle("Save File")
            initial_directory = self.last_path if self.switch else 'sfsrs'
            file_dialog.setDirectory(initial_directory)
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setNameFilter("Excel Files (*.xlsx)")
            file_dialog.setDefaultSuffix(".xlsx")
            if file_dialog.exec_() == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                file_name = file_dialog.selectedFiles()[0].split("/")[-1]
                if '.' in file_name:
                    clear_file_name = file_name.split('.')[0]
                    splited_file_path = file_path.split('/')
                    removed_item = splited_file_path.pop()
                    file_path = '\\'.join(splited_file_path) + '\\' + clear_file_name

                excel_writer = ExcelWriter(file_path  + ".xlsx", engine="xlsxwriter")

                results = self.Calcresult
                #Temperatures
                #Name dictionary
                temp_name_dict = {'Name': {}}
                for key in results['Temperatures']:
                    temp_name_dict['Name'][key] = key
                temp_data = {'Name' : temp_name_dict['Name'], 'Inner temperatures, \u00b0C': results['Temperatures'],'Outer temperatures, \u00b0C': results['TemperaturesOut']}
                #Data_frame
                temp_df = DataFrame(temp_data)

                #HB
                #Name dictionary
                hb_name_dict = {'Name': {}}
                for key in results['Heat']['RS power']:
                    hb_name_dict['Name'][key] = key
                hb_data = {'Name' : hb_name_dict['Name'], 'RS power, W': results['Heat']['RS power'], 'RS flux, W/m2': results['Heat']['RS flux'], 'Conv power, W': results['Heat']['Conv power'], 'Conv flux, W/m2': results['Heat']['Conv flux'], 'Additional power, W': results['Heat']['Add power'], 'Total power, W': results['Heat']['Total power'], 'Total flux, W/m2': results['Heat']['Total flux'], 'Losses, W': results['Losses']}                       
                #Data_frame
                hb_df = DataFrame(hb_data)
                temp_df.to_excel(excel_writer, sheet_name='Temperatures', index=False)
                hb_df.to_excel(excel_writer, sheet_name='Heat balance', index=False)

                water_name_dict = {'Name': {}}
                surface_temp_dict = {}
                if len(self.water_temp_result) != 0:
                    for key in self.water_temp_result:
                        water_name_dict['Name'][key] = key
                        surface_temp_dict[key] = self.user_data[key]['RS'][list(self.user_data[key]['RS'].keys())[0]]['RS_T']
                    water_data = {'Name' : water_name_dict['Name'], 'Surface temperatures': surface_temp_dict, 'Water temperatures': self.water_temp_result}
                    water_df = DataFrame(water_data)
                    water_df.to_excel(excel_writer, sheet_name='Water temperature', index=False)

                excel_writer.save()
                self.settings_label.setText('Export complete')
                self.switch = True
                self.last_path = file_path

    except AttributeError:
        self.settings_label.setText('No results to export')
        return()

def save_project(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_dialog = QFileDialog()
    file_dialog.setOptions(options)
    file_dialog.setWindowTitle("Save File")
    initial_directory = self.last_path if self.switch else 'sfsrs'
    file_dialog.setDirectory(initial_directory)
    file_dialog.setAcceptMode(QFileDialog.AcceptSave)
    file_dialog.setNameFilter("Custom Project Files (*.cmproj)")
    file_dialog.setDefaultSuffix(".cmproj")

    if file_dialog.exec_() == QFileDialog.Accepted:
        file_path = file_dialog.selectedFiles()[0]
        file_name = file_dialog.selectedFiles()[0].split("/")[-1]
        if '.' in file_name:
            clear_file_name = file_name.split('.')[0]
            splited_file_path = file_path.split('/')
            removed_item = splited_file_path.pop()
            file_path = '\\'.join(splited_file_path) + '\\' + clear_file_name

        save_data = collect(self)
        with open(file_path + ".cmproj", 'w') as json_file:
            dump(save_data, json_file, indent=4)
        self.check_project = save_data.copy()
        self.switch = True
        self.last_path = file_path


def load_project(self, tree):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    file_dialog = QFileDialog()
    file_dialog.setOptions(options)
    file_dialog.setWindowTitle("Load File")
    initial_directory = self.last_path if self.switch else 'sfsrs'
    file_dialog.setDirectory(initial_directory)
    file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
    file_dialog.setNameFilter("Custom Project Files (*.cmproj)")
    file_dialog.setDefaultSuffix(".cmproj")

    if file_dialog.exec_() == QFileDialog.Accepted:
        file_path = file_dialog.selectedFiles()[0]
        file_name = file_dialog.selectedFiles()[0].split("/")[-1]
        if '.' in file_name:
            clear_file_name = file_name.split('.')[0]
            splited_file_path = file_path.split('/')
            removed_item = splited_file_path.pop()
            file_path = '\\'.join(splited_file_path) + '\\' + clear_file_name
        with open(file_path + ".cmproj", 'r') as json_file:
            load_data = load(json_file)
        self.check_project = load_data.copy()
        load_data_to_project(self, load_data, tree)              
        self.switch = True
        self.last_path = file_path



def load_data_to_project(self, load_data, tree):
    self.convection_box.setCurrentIndex(0)
    self.Adsource.setText('0') 
    del load_data['RS_number']
    self.unit_box.setCurrentIndex(load_data['unit_box']) 
    self.temp_box.setCurrentIndex(load_data['temp_box'])
    del load_data['temp_box']
    del load_data['unit_box']
    for name in self.construct_list:
        child_count = self.node[name].childCount()
        for i in range(child_count):
            Delete(self, tree, self.node[name].child(0))
    for name in load_data:
        for nod in load_data[name]:
            if nod == 'RS':
                if len(load_data[name][nod]) != 0:
                    self.RS_num[name] = 0
                    for num in load_data[name][nod]:                                            
                        RS_generate(self, tree, name, num)
                        for value in load_data[name][nod][num]:
                            if value != 'coord':
                                self.main_data[name][nod][num][value].setText(load_data[name][nod][num][value])
                            else:
                                for coord in load_data[name][nod][num][value]:
                                    self.main_data[name][nod][num][value][coord].setText(load_data[name][nod][num][value][coord])
                    self.RS_num[name] += int(self.RS_data[name][-1])
            elif nod == 'door':
                if len(load_data[name][nod]) != 0:
                    self.door_num[name] = 0
                    for num in load_data[name][nod]:                                           
                        Door_generate(self, tree, name, num)
                        for value in load_data[name][nod][num]:
                            if value != 'coord':
                                self.main_data[name][nod][num][value].setText(load_data[name][nod][num][value])
                            else:
                                for coord in load_data[name][nod][num][value]:
                                    self.main_data[name][nod][num][value][coord].setText(load_data[name][nod][num][value][coord])
            elif nod == 'Adsource':
                self.convection_box.setCurrentIndex(1)
                self.Adsource.setText(load_data[name][nod]) 
            elif nod == 'Water_calc':
                self.tree.setCurrentItem(self.node[name].child(0), False)
                water_create(self, tree)
                table_name = self.water_table[name]
                self.mat_step_box[name].setCurrentIndex(load_data[name]['Water_calc'][1])
                self.mat_diam_box[name].setCurrentIndex(load_data[name]['Water_calc'][5])
                self.out_condiition_box[name].setCurrentIndex(load_data[name]['Water_calc'][2])
                if load_data[name]['Water_calc'][3] == 1:
                    self.out_condiition_value_box[name].setCurrentIndex(1)
                    self.out_condiition_value[name].setText(load_data[name]['Water_calc'][4])
                for data_list in load_data[name]['Water_calc'][0]:
                    row_count = table_name.rowCount()
                    table_name.setRowCount(row_count + 1)
                    col = 0
                    for value in data_list:
                        if type(value) != list:
                            item = QTableWidgetItem(value)
                            table_name.setItem(row_count, col, item)
                            col +=1
                        else:
                            item = QTableWidgetItem(value[2])
                            table_name.setItem(row_count, col, item)  
        
            else:
                self.main_data[name][nod].setText(load_data[name][nod])

def confirm_exit_dialog(self):
    reply = False
    if (self.check_project == collect(self)) == False:
        click = QMessageBox.question(
            self, 'Exit', 'Save changes in Project?',
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if click == QMessageBox.Yes:
            save_project(self)
            if self.switch == True:
                reply = True
            else:
                return
        elif click == QMessageBox.No:
            reply = True
        else:
            return
    else:
        reply = True
    return reply



def info_function(self):
    self.about_dialog = QDialog()
    self.about_dialog.setWindowTitle("About")
    center_point = QDesktopWidget().availableGeometry().center()
    self.about_dialog.setGeometry(center_point.x() - 300, center_point.y() - 150, 300, 150)
    self.layout = QVBoxLayout()
    top_label = MyLabel('Calculator for heating and cooling capillary system')
    label_main_text = MyLabel2('Version: 1.0 \nDevelopers: Kirill Bolotin, Ansis Ziemelis \nE-mail: BolotinKE@gmail.com\n\nDeveloped with the financial support of ERDF project \n“Development and approbation of complex solutions for optimal inclusion of CHE \nin nearly zero energy building systems and reduction of primary energy consumption for heating and cooling” \n(1.1.1.1./19/A/102).') 
    font = QFont()
    font.setPointSize(13)  
    label_main_text.setFont(font)
    self.layout.addWidget(top_label)
    self.layout.addWidget(label_main_text)
    ok_button = QPushButton("OK")
    ok_button.clicked.connect(self.about_dialog.accept)
    self.layout.addWidget(ok_button)
    self.about_dialog.setLayout(self.layout)
    self.about_dialog.setStyleSheet("background-color: white;")
    self.about_dialog.exec_()

def new_project(self, tree):
    confirm_exit_dialog(self)
    load_data_to_project(self, self.initial_project.copy(), tree)
    self.check_project = self.initial_project.copy()