from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidget, QMainWindow, QComboBox, QGraphicsScene, QTableWidget, QGridLayout, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidgetItem
from PyQt5.QtGui import  QIcon
from Top_buttons_commands import water_create, Door_create, RS_create, Delete, construct_layers
from Classes_list import FloatLineEdit, MyLabel, MyLabel2, MyButton, CustomGraphicsView
from Results_functions import results, temp_results, HB_results, WT_results
from Draw_function import graph_build
from Treeview_click import click
from Table_functions import add_empty_row, move_row_up, move_row_down, delete_rows
from Front_calculations import U_calc_layer_data, adsource_enable, alpha_value, zero_alpha_control, water_out_condition_status, top_U_control
from load_save_functions import export_results, save_project, load_project, confirm_exit_dialog, info_function, new_project
from sys import exit, argv
from os.path import dirname, join, abspath


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.dark_theme = """
        #    QMainWindow {

        #        background-color: #292929;
        #    }           
        #    QTreeWidget {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #    }
        #    QPushButton {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #        border-radius: 5px;
        #        padding: 10px;
        #    }
        #    QComboBox {
        #        color: #ffffff;
        #        background-color: #292929;
        #        border: #000000;
        #        border-radius: 5px;
        #        padding: 10px;
        #    }
        #    QLabel {
        #        color: #ffffff;
        #        background-color: #292929;
        #    }
        #    QPushButton:hover {
        #        background-color: #454545;
        #    }
        #"""
        self.light_theme = """
            QMainWindow {
                background-color: #ffffff;
            }
            #QTreeWidget {
            #    color: #000000;
            #    background-color: #ffffff;
            #    border: #ffffff;
            #QPushButton {
            #    color: #000000;
            #    background-color: #ffffff;
            #    border: none;
            #    border-radius: 5px;
            #    padding: 10px;
            #}
            #QLabel {
            #    border: none;
            #    background-color: white;
            #    color: black;
            #QPushButton:hover {
            #    background-color: #eeeeee;
            #}
        """
        QApplication.instance().setStyleSheet(self.light_theme)
        self.initUI()

    def initUI(self):
        self.border_style = "border: 0.5px solid gray;"
        #Generate layouts
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.top_menu_widget = QWidget()
        self.top_menu_widget.setFixedHeight(100)       
        self.top_menu_widget.setStyleSheet(self.border_style)
        self.top_menu_layout = QHBoxLayout()
        self.top_menu_widget.setLayout(self.top_menu_layout)
        self.top_menu_layout.setContentsMargins(5, 0, 0, 0)
        self.top_menu_layout.setSpacing(0)
        self.top_menu_layout.setAlignment(Qt.AlignLeft)
        self.model_layout = QHBoxLayout()
        #Left
        self.left_window_widget = QWidget()
        self.left_window_widget.setStyleSheet(self.border_style)
        self.left_window_layout = QVBoxLayout()
        self.left_window_layout.setAlignment(Qt.AlignTop)
        self.left_window_widget.setLayout(self.left_window_layout)
        #Central
        self.central_window_widget = QWidget()
        self.central_window_widget.setStyleSheet(self.border_style)
        self.center_window_layout = QVBoxLayout()
        self.center_window_layout.setAlignment(Qt.AlignTop)
        self.central_window_widget.setLayout(self.center_window_layout)
        self.central_grid = QGridLayout()
        self.central_grid.setAlignment(Qt.AlignLeft)
        self.central_water_button_layout = QHBoxLayout()
        #Right
        self.right_window_widget = QWidget()
        self.right_window_widget.setStyleSheet(self.border_style)
        self.right_window_layout = QVBoxLayout()
        self.right_window_layout.setAlignment(Qt.AlignTop)
        self.right_window_widget.setLayout(self.right_window_layout)
        self.right_graph_layout = QVBoxLayout()
        self.right_graph_layout.setAlignment(Qt.AlignTop)
        self.right_graph_layout.setAlignment(Qt.AlignLeft)
        #Results
        self.right_results_layout = QVBoxLayout()
        self.right_results_buttons_layout = QHBoxLayout()
        self.right_results_buttons_layout.setAlignment(Qt.AlignLeft)
        self.right_results_layout.setAlignment(Qt.AlignTop)
        self.right_results_widget = QWidget()
        self.right_results_widget.setStyleSheet(self.border_style)
        self.right_window_layout.addLayout(self.right_graph_layout, 60)
        self.right_window_layout.addLayout(self.right_results_layout, 40)
        #Add layouts to main 
        self.main_layout.addWidget(self.top_menu_widget)
        self.main_layout.addLayout(self.model_layout)
        #Add layouts to model_layout
        self.model_layout.addWidget(self.left_window_widget, 20)
        self.model_layout.addWidget(self.central_window_widget, 20)
        self.model_layout.addWidget(self.right_window_widget, 60)
        #Add main to window
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        #Filling 3 windows
        #Top window


        current_dir = dirname(abspath(__file__))
        icons_dir = join(current_dir, 'Icons')
        self.RS_button = MyButton('Radiant\nSurface')
        self.RS_button.setFixedSize(90, 80)
        self.RS_button.clicked.connect(lambda: RS_create(self, self.tree))
        RS_icon = QIcon(join(icons_dir, 'RS_icon.png'))
        self.RS_button.setIcon(RS_icon)
        self.RS_button.setIconSize(self.RS_button.rect().size()/2.1)
        self.Door_button = MyButton('Door\nWindow')
        self.Door_button.setFixedSize(90, 80)
        self.Door_button.clicked.connect(lambda: Door_create(self, self.tree))
        door_icon = QIcon(join(icons_dir, 'door_icon.png'))
        self.Door_button.setIcon(door_icon)
        self.Door_button.setIconSize(self.Door_button.rect().size()/2.1)
        self.Water_button = MyButton('Calculate\nwater\ntemperature')
        self.Water_button.setFixedSize(120,80)
        self.Water_button.clicked.connect(lambda: water_create(self, self.tree))
        water_temp_icon = QIcon(join(icons_dir, 'water_temp_icon.png'))
        self.Water_button.setIcon(water_temp_icon)
        self.Water_button.setIconSize(self.Water_button.rect().size()/2)
        self.Del_button = MyButton('Delete')
        self.Del_button.setFixedSize(90, 80)
        self.Del_button.clicked.connect(lambda: Delete(self, self.tree, None))
        delete_icon = QIcon(join(icons_dir, 'delete_icon.png'))
        self.Del_button.setIcon(delete_icon)
        self.Del_button.setIconSize(self.Del_button.rect().size()/2)
        self.results_button = MyButton('Calculate')
        self.results_button.setFixedSize(90, 80)
        self.results_button.clicked.connect(lambda: results(self))
        calc_icon = QIcon(join(icons_dir, 'calc_icon.png'))
        self.results_button.setIcon(calc_icon)
        self.results_button.setIconSize(self.results_button.rect().size()/2.5)
        self.construct_button = MyButton('Build layers')
        self.construct_button.setFixedSize(110, 80)
        self.construct_button.clicked.connect(lambda: construct_layers(self))
        construct_icon = QIcon(join(icons_dir, 'construct_icon.png'))
        self.construct_button.setIcon(construct_icon)
        self.construct_button.setIconSize(self.construct_button.rect().size()/2.1)
        self.temp_results_button = MyButton('Temperature')
        self.temp_results_button.setFixedSize(100, 30)
        self.temp_results_button.clicked.connect(lambda: temp_results(self))
        temp_icon = QIcon(join(icons_dir, 'ht_icon.png'))
        self.temp_results_button.setIcon(temp_icon)
        self.temp_results_button.setIconSize(self.temp_results_button.rect().size()/1.4)
        self.heat_balance_results_button = MyButton('Heat balance')
        self.heat_balance_results_button.setFixedSize(100, 30)
        self.heat_balance_results_button.clicked.connect(lambda: HB_results(self))
        HB_icon = QIcon(join(icons_dir, 'HB_icon.png'))
        self.heat_balance_results_button.setIcon(HB_icon)
        self.heat_balance_results_button.setIconSize(self.heat_balance_results_button.rect().size()/1.5)        
        self.water_temperature_results_button = MyButton('Water temperature')
        self.water_temperature_results_button.setFixedSize(130, 30)
        self.water_temperature_results_button.clicked.connect(lambda: WT_results(self))
        wt_icon = QIcon(join(icons_dir, 'wt_icon.png'))
        self.water_temperature_results_button.setIcon(wt_icon)
        self.water_temperature_results_button.setIconSize(self.water_temperature_results_button.rect().size()/1.5)
        self.export_results_button = MyButton('Export results')
        self.export_results_button.setFixedSize(130, 30)
        self.export_results_button.clicked.connect(lambda: export_results(self))
        export_results_icon = QIcon(join(icons_dir, 'export_results.png'))
        self.export_results_button.setIcon(export_results_icon)
        self.export_results_button.setIconSize(self.export_results_button.rect().size())
        self.new_button = MyButton('New Project')
        self.new_button.setFixedSize(130, 30)
        self.new_button.clicked.connect(lambda: new_project(self, self.tree))
        new_icon = QIcon(join(icons_dir, 'new_icon.png'))
        self.new_button.setIcon(new_icon)
        self.new_button.setIconSize(self.new_button.rect().size())
        self.save_button = MyButton('Save Project')
        self.save_button.setFixedSize(130, 30)
        self.save_button.clicked.connect(lambda: save_project(self))
        save_icon = QIcon(join(icons_dir, 'save_icon.png'))
        self.save_button.setIcon(save_icon)
        self.save_button.setIconSize(self.save_button.rect().size())
        self.load_button = MyButton('Load Project')
        self.load_button.setFixedSize(130, 30)
        self.load_button.clicked.connect(lambda: load_project(self, self.tree))
        load_icon = QIcon(join(icons_dir, 'load_icon.png'))
        self.load_button.setIcon(load_icon)
        self.load_button.setIconSize(self.load_button.rect().size())
        self.info_button = MyButton('Info')
        self.info_button.setFixedSize(80, 30)
        self.info_button.clicked.connect(lambda: info_function(self))
        info_icon = QIcon(join(icons_dir, 'info_icon.png'))
        self.info_button.setIcon(info_icon)
        self.info_button.setIconSize(self.info_button.rect().size())
        #Left window
        #Name
        self.left_label = MyLabel('Model builder')
        #Generate treeview
        self.tree = QTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.node = {}
        self.node['Model_tree_node'] = QTreeWidgetItem(self.tree, ['Model tree'])
        self.node['Model_tree_node'].setExpanded(True)
        self.tree.addTopLevelItem(self.node['Model_tree_node'])
        self.node['Room'] = QTreeWidgetItem(self.node['Model_tree_node'], ['Room'])
        self.node['Room'].setExpanded(True)
        self.node['Ceiling'] = QTreeWidgetItem(self.node['Room'], ['Ceiling'])
        self.node['Floor'] = QTreeWidgetItem(self.node['Room'], ['Floor'])
        self.node['Wall 1'] = QTreeWidgetItem(self.node['Room'], ['Wall 1'])
        self.node['Wall 2'] = QTreeWidgetItem(self.node['Room'], ['Wall 2'])
        self.node['Wall 3'] = QTreeWidgetItem(self.node['Room'], ['Wall 3'])
        self.node['Wall 4'] = QTreeWidgetItem(self.node['Room'], ['Wall 4'])
        self.results_node = QTreeWidgetItem(self.node['Model_tree_node'], ['Results'])
        self.tree.selectionModel().selectionChanged.connect(lambda: click(self, self.tree))
        self.tree.selectionModel().selectionChanged.connect(lambda: graph_build(self))
        self.tree.selectionModel().selectionChanged.connect(lambda: U_calc_layer_data(self, None))
        self.tree.selectionModel().selectionChanged.connect(lambda: water_out_condition_status(self))
        
        #Set items to left window
        self.left_window_layout.addWidget(self.left_label)       
        self.left_window_layout.addWidget(self.tree)
        #Central window
        #Name
        self.central_label = MyLabel('Settings')
        self.settings_label = MyLabel2('')
        #Inputs
        #Model tree
        self.unit_box = QComboBox()
        self.unit_box.addItem('m')
        self.unit_box.addItem('cm')
        self.unit_box.addItem('mm')
        self.unit_box.setFixedWidth(60)
        self.temp_box = QComboBox()
        self.temp_box.addItem('\u00b0C')
        self.temp_box.addItem('K')
        self.temp_box.setFixedWidth(60)
        #Room size
        self.room = {}

        #Room convection and source
        self.convection_box = QComboBox()
        self.convection_box.addItem('No air heat transfer')
        self.convection_box.addItem('With air heat transfer')
        self.convection_box.currentIndexChanged.connect(lambda: adsource_enable(self))
        self.Adsource_label = MyLabel2('Additional source')
        self.Adsource = FloatLineEdit()
        self.Adsource_unit = MyLabel2('W')
        self.Adsource.setText('0')
        #Central windows
        #Phys parametres


        #Set items to central window
        self.center_window_layout.addWidget(self.central_label)
        #Water table buttons
        self.button_up = MyButton("")
        self.button_up.setEnabled(False)
        self.button_up.setFixedSize(30, 30)
        up_icon = QIcon(join(icons_dir, '_up_icon.png'))
        self.button_up.setIcon(up_icon)
        self.button_up.setIconSize(self.button_up.rect().size())
        self.button_up.clicked.connect(lambda: move_row_up(self))
        self.button_down = MyButton("")
        self.button_down.setEnabled(False)
        self.button_down.setFixedSize(30, 30)
        down_icon = QIcon(join(icons_dir, 'down_icon.png'))
        self.button_down.setIcon(down_icon)
        self.button_down.setIconSize(self.button_down.rect().size())
        self.button_down.clicked.connect(lambda: move_row_down(self))
        self.button_delete = MyButton("")
        self.button_delete.setEnabled(False)
        self.button_delete.setFixedSize(30, 30)
        delete_row_icon = QIcon(join(icons_dir, 'delete_row_icon.png'))
        self.button_delete.setIcon(delete_row_icon)
        self.button_delete.setIconSize(self.button_delete.rect().size())
        self.button_delete.clicked.connect(lambda: delete_rows(self))
        self.add_button = MyButton("")
        self.add_button.setFixedSize(30, 30)
        row_add_icon = QIcon(join(icons_dir, '_row_add_icon.png'))
        self.add_button.setIcon(row_add_icon)
        self.add_button.setIconSize(self.add_button.rect().size())
        self.add_button.clicked.connect(lambda: add_empty_row(self))              
        #Right window items
        #Names
        self.result_label = MyLabel('Results')
        self.graph_label = MyLabel('Graphics')
        #Set items to right window
        self.right_graph_layout.addWidget(self.graph_label)
        self.right_results_layout.addWidget(self.result_label)
        self.right_results_layout.addLayout(self.right_results_buttons_layout)
        self.right_results_buttons_layout.addWidget(self.temp_results_button)
        self.right_results_buttons_layout.addWidget(self.heat_balance_results_button)
        self.right_results_buttons_layout.addWidget(self.water_temperature_results_button)
        #Inputs
        #Graphics
        self.right_graphics_view = CustomGraphicsView(self)
        self.scene = QGraphicsScene()
        self.right_graphics_view.setScene(self.scene)
        self.right_graph_layout.addWidget(self.right_graphics_view)

        #Results
        self.result_table = QTableWidget()
        self.right_results_layout.addWidget(self.result_table)
        #Variables
        #All
        self.coord_list = ['x', 'y', 'W', 'L']
        #Water
        self.water_switch = {'Ceiling': False, 'Floor': False, 'Wall 1': False, 'Wall 2': False, 'Wall 3': False, 'Wall 4': False}
        self.water_table = {}
        self.node['water'] = {}
        self.mat_diam_box = {}
        self.mat_step_box = {}
        self.out_condiition_box = {}
        self.out_condiition_value_box = {}
        self.out_condiition_value = {}
        self.out_condiition_label = {}
        self.out_condiition_unit = {}
        self.last_alfa_water = {}


        self.construct_list = ['Ceiling', 'Floor', 'Wall 1', 'Wall 2', 'Wall 3', 'Wall 4']

        self.main_data = {'Room':{}, 'Ceiling':{}, 'Floor':{}, 'Wall 1':{}, 'Wall 2':{}, 'Wall 3': {}, 'Wall 4': {}}
        self.alpha_box = {}
        self.main_data['Room']['RL'] = FloatLineEdit()
        self.main_data['Room']['RW'] = FloatLineEdit()
        self.main_data['Room']['RH'] = FloatLineEdit()
        for name in self.construct_list:
            self.main_data[name]['eps'] = FloatLineEdit()
            self.main_data[name]['eps'].setText('0.9')
            self.main_data[name]['U'] = FloatLineEdit()
            self.main_data[name]['U'].textEdited.connect(lambda: top_U_control(self))
            self.main_data[name]['Tout'] = FloatLineEdit()
            self.main_data[name]['alpha'] = FloatLineEdit()
            self.main_data[name]['alpha'].setToolTip("REsistance must be >0")
            self.main_data[name]['alpha'].textEdited.connect(lambda: zero_alpha_control(self))
            if ('Wall' in name) == True:
                self.main_data[name]['alpha'].setText('0.13')
            elif ('Floor' in name) == True:
                self.main_data[name]['alpha'].setText('0.1')
            elif ('Ceiling' in name) == True:
                self.main_data[name]['alpha'].setText('0.17')
            self.main_data[name]['alpha'].setReadOnly(True)
            self.alpha_box[name] = QComboBox()
            self.alpha_box[name].addItem('Physics control')
            self.alpha_box[name].addItem('User defined')
            self.alpha_box[name].currentIndexChanged.connect(lambda: alpha_value(self))
            self.main_data[name]['RS'] = {}
            self.main_data[name]['door'] = {}
        #Radiant surfaces
        self.RS_data_list = ['RS_eps', 'RS_T', 'area', 'coord']
        self.RS_num = {'Ceiling': 0, 'Floor': 0, 'Wall 1': 0, 'Wall 2': 0, 'Wall 3': 0, 'Wall 4': 0}
        self.node['RS'] = {'Ceiling': {}, 'Floor': {}, 'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.RS_data = {'Ceiling': [], 'Floor': [], 'Wall 1': [], 'Wall 2': [], 'Wall 3': [], 'Wall 4': []}
        self.RS_data_collect = {}
        for data in self.RS_data_list:
            self.RS_data_collect[data] = {}
            for name in self.construct_list:
                self.RS_data_collect[data][name] = {}
        #Door
        self.door_data_list = ['door_eps', 'door_U', 'area', 'coord']
        self.door_num = {'Wall 1': 0, 'Wall 2': 0, 'Wall 3': 0, 'Wall 4': 0}
        self.node['door'] = {'Wall 1': {}, 'Wall 2': {}, 'Wall 3': {}, 'Wall 4': {}}
        self.door_data = {'Wall 1': [], 'Wall 2': [], 'Wall 3': [], 'Wall 4': []}

        self.door_data_collect = {}
        for data in self.door_data_list:
            self.door_data_collect[data] = {}
            for name in self.construct_list:
                self.door_data_collect[data][name] = {}
        self.wall_num_list = ['1', '2', '3', '4']
        #Saveload
        self.switch = False
        self.tree.setCurrentItem(self.node['Model_tree_node'], False)
        self.click = -1


        self.check_project = {
    "Room": {
        "RL": "",
        "RW": "",
        "RH": ""
    },
    "RS_number": False,
    "Ceiling": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "Floor": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "Wall 1": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "Wall 2": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "Wall 3": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "Wall 4": {
        "eps": "0.9",
        "U": "",
        "Tout": "",
        "RS": {},
        "door": {}
    },
    "unit_box": 0,
    "temp_box": 0
}
        self.initial_project = self.check_project.copy()
        

    def closeEvent(self, event):
        result = confirm_exit_dialog(self)
        if result == True:
            event.accept() 
        else:
            event.ignore()



            
def main():
    app = QApplication(argv)
    window = MainWindow()
    window.showMaximized()
    exit(app.exec_())

if __name__ == '__main__':
    main()



    #pyinstaller --onefile --windowed --add-data "Icons;Icons" Main.py