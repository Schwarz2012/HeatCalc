from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QBrush, QColor


#Water table actions
#Buttons activation update
def update_button_states(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent().parent().data()
    self.table_name = self.water_table[parent_name]
    current_row = self.table_name.currentRow()
    row_count = self.table_name.rowCount()
    if len(self.table_name.selectedItems()) != 0:
        self.button_delete.setEnabled(True)
    else:
        self.button_delete.setEnabled(False)
    if current_row > 0 :
        self.button_up.setEnabled(True)
    else: 
        self.button_up.setEnabled(False)
    if current_row < row_count-1 and current_row >= 0:
        self.button_down.setEnabled(True)
    else:  
        self.button_down.setEnabled(False)
#Add empty row
def add_empty_row(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent().parent().data()
    self.table_name = self.water_table[parent_name]
    row_count = self.table_name.rowCount()
    self.table_name.setRowCount(row_count + 1)
    for column in range(self.table_name.columnCount()):
        item = QTableWidgetItem("")
        self.table_name.setItem(row_count, column, item)         
#Move row up
def move_row_up(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent().parent().data()
    self.table_name = self.water_table[parent_name]
    source_items = []   
    current_row = self.table_name.currentRow()
    if current_row > 0:
        self.table_name.insertRow(current_row-1)
        for column in range(self.table_name.columnCount()):
            item = self.table_name.item(current_row + 1, column)
            source_items.append(item)
        for column in range(self.table_name.columnCount()):
            item = source_items[column].clone() if source_items[column] else None
            self.table_name.setItem(current_row - 1, column, item)
        self.table_name.removeRow(current_row + 1)
#Move row down
def move_row_down(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent().parent().data()
    self.table_name = self.water_table[parent_name]
    source_items = []
    current_row = self.table_name.currentRow()
    if current_row < self.table_name.rowCount() - 1:
        self.table_name.insertRow(current_row + 2)
        for column in range(self.table_name.columnCount()):
            item = self.table_name.item(current_row, column)
            source_items.append(item)
        for column in range(self.table_name.columnCount()):
            item = source_items[column].clone() if source_items[column] else None
            self.table_name.setItem(current_row + 2, column, item)
        self.table_name.removeRow(current_row)

#Delete selected rows
def delete_rows(self):
    current_name = self.tree.currentIndex()   
    parent_name = current_name.parent().parent().data()
    self.table_name = self.water_table[parent_name]
    selected_rows = sorted(set(index.row() for index in self.table_name.selectedIndexes()), reverse=True)
    for row in selected_rows:
        self.table_name.removeRow(row)


def offset_check(self, name):
    table_name = self.water_table[name]
    try:
        row = table_name.currentRow()
        delta_offset = float(table_name.item(row, 3).text()) + float(self.mat_diam_box[name].currentText())
        layer_size = float(table_name.item(row, 1).text())
        item = table_name.item(row, 3)
        if delta_offset > layer_size:
            brush = QBrush(QColor(255, 0, 0))
            item.setBackground(brush)
        else:
            brush = QBrush(QColor(255, 255, 255))
            item.setBackground(brush)
    except (ValueError, AttributeError, TypeError):
        return