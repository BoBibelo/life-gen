import sys
import time

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

class MainWindow(QtWidgets.QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.init_window()

    def init_window(self):
        """Init the main window"""

        self.setFixedSize(900, 500)
        self.setWindowTitle("Life-Gen")

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        self.size_box()

        main_grid = QtWidgets.QHBoxLayout()
        self.create_label_grid()
        self.create_cmd_grid()

        main_grid.addLayout(self.label_grid)
        main_grid.addLayout(self.cmd_grid)
        self.central_widget.setLayout(main_grid)
        self.show()
    
    def manage_evolution(self):
        """Launch evolution for x generations"""

        gen_nbr = self.gen_nbr.value()
        for i in range(gen_nbr):
            time.sleep(0.2)
            self.evolution()
            QtWidgets.QApplication.processEvents()

    def evolution(self):
        """Launch evolution for 1 generation"""

        tmp_cell_list = [[False for y in range(self.nbr_rows)] for x in range(self.nbr_columns)]

        for x in range(self.nbr_columns):
            for y in range(self.nbr_rows):
                neighbours = self.number_neighbours(y, x)

                if self.cell_list[y][x]:
                    if neighbours < 2 or neighbours > 3:
                        tmp_cell_list[y][x] = False
                    else:
                        tmp_cell_list[y][x] = True
                elif neighbours == 3:
                    tmp_cell_list[y][x] = True
                else:
                    tmp_cell_list[y][x] = False

        self.cell_list = tmp_cell_list
        self.update_cell()

    def update_cell(self):
        """Update cells"""

        for x in range(self.nbr_columns):
            for y in range(self.nbr_rows):
                if self.cell_list[y][x]:
                    self.make_alive(y, x)
                else:
                    self.make_dead(y, x)

    def number_neighbours(self, y, x):
        """Number of neighbours alive for cell in pos [row][column]"""

        neighbours = 0
        if x >= 1 and y >= 1 and self.cell_list[y - 1][x - 1]: # Up - Left
            neighbours += 1
        if x >= 1 and self.cell_list[y][x - 1]: # Left
            neighbours += 1
        if x >= 1 and y <= self.nbr_rows - 2 and self.cell_list[y + 1][x - 1]: # Down - Left
            neighbours += 1
        if y <= self.nbr_rows - 2 and self.cell_list[y + 1][x]: # Down
            neighbours += 1
        if x <= self.nbr_columns - 2 and y <= self.nbr_rows - 2 and self.cell_list[y + 1][x + 1]: # Down - Right
            neighbours += 1
        if x <= self.nbr_columns - 2 and self.cell_list[y][x + 1]: # Right
            neighbours += 1
        if x <=  self.nbr_columns - 2 and y >= 1 and self.cell_list[y - 1][x + 1]: # Up - Right
            neighbours += 1
        if y >= 1 and self.cell_list[y - 1][x]: # Up
            neighbours += 1
        return neighbours

    def create_cmd_grid(self):
        """Create the command grid"""

        self.cmd_grid = QtWidgets.QVBoxLayout()
        self.new_but = QtWidgets.QPushButton("New")
        self.new_but.clicked.connect(self.size_box)
        label = QtWidgets.QLabel("Number of Generation:")
        self.gen_nbr = QtWidgets.QSpinBox()
        self.gen_nbr.setRange(1, 100)
        self.go_but = QtWidgets.QPushButton("Evolve!")
        self.go_but.clicked.connect(self.manage_evolution)
        self.cmd_grid.addWidget(label)
        self.cmd_grid.addWidget(self.gen_nbr)
        self.cmd_grid.addWidget(self.go_but)

    def map_generation(self):
        """Generate the cells list with their state"""

        self.cell_list = [[ False for y in range(self.nbr_rows)] for x in range(self.nbr_columns)]
        for x in range(self.nbr_columns):
            for y in range(self.nbr_rows):
                if self.grid_checkbox.itemAtPosition(y, x).widget().isChecked():
                    self.cell_list[y][x] = True

        self.life_box.close()

    def life_box(self):
        """QDialog asking state of cells"""

        self.nbr_rows = self.input_row.value()
        self.nbr_columns = self.input_column.value()
        self.size_dialog.close()

        self.life_box = QtWidgets.QDialog(self)
        self.life_box.setFixedSize(900, 500)
        self.life_box.setModal(True)

        grid = QtWidgets.QVBoxLayout()
        self.grid_checkbox = QtWidgets.QGridLayout()
        for x in range(self.nbr_columns):
            for y in range(self.nbr_rows):
                self.grid_checkbox.addWidget(QtWidgets.QCheckBox(), y, x)
        ok_but = QtWidgets.QPushButton("Generate map.")
        ok_but.clicked.connect(self.map_generation)

        grid.addLayout(self.grid_checkbox)
        grid.addWidget(ok_but)
        self.life_box.setLayout(grid)
        self.life_box.exec_()

    def size_box(self):
        """QDialog asking for map size"""

        self.size_dialog = QtWidgets.QDialog(self)
        self.size_dialog.setFixedSize(900, 500)
        self.size_dialog.setModal(True)

        grid = QtWidgets.QVBoxLayout()
        label_row = QtWidgets.QLabel("Number of rows:")
        self.input_row = QtWidgets.QSpinBox()
        self.input_row.setRange(2, 100)
        label_column = QtWidgets.QLabel("Number of columns:")
        self.input_column = QtWidgets.QSpinBox()
        self.input_column.setRange(2, 100)
        ok_but = QtWidgets.QPushButton("Ok")
        ok_but.clicked.connect(self.life_box)

        grid.addWidget(label_row)
        grid.addWidget(self.input_row)
        grid.addWidget(label_column)
        grid.addWidget(self.input_column)
        grid.addWidget(ok_but)
        self.size_dialog.setLayout(grid)
        self.size_dialog.exec_()

    def create_label_grid(self):
        """Create the grid where cells are displayed"""

        self.label_grid = QtWidgets.QGridLayout()
        self.label_grid.setSpacing(5)

        for x in range(self.nbr_columns): # columns
            for y in range(self.nbr_rows): # rows
                self.label_grid.addWidget(self.create_label_clickable(y, x), y, x)
                if self.cell_list[y][x]:
                    self.make_alive(y, x)

    def make_alive(self, row, column):
        """Make a cell alive"""

        pixmap = QtGui.QPixmap(30, 30)
        pixmap.fill(QtGui.QColor(QtCore.Qt.cyan))
        self.label_grid.itemAtPosition(row, column).widget().setPixmap(pixmap)
        self.cell_list[row][column] = True

    def make_dead(self, row, column):
        """Make a cell dead"""

        pixmap = QtGui.QPixmap(30, 30)
        pixmap.fill(QtGui.QColor(QtCore.Qt.darkBlue))
        self.label_grid.itemAtPosition(row, column).widget().setPixmap(pixmap)
        self.cell_list[row][column] = False

    def create_label_clickable(self, row, column):
        """Return a white clickable label"""

        label = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(30, 30)
        pixmap.fill(QtGui.QColor(QtCore.Qt.darkBlue))
        label.setPixmap(pixmap)
        return label


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
