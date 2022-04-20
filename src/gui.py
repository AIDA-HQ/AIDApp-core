from qtpy.QtWidgets import (
    QLabel,
    QDoubleSpinBox,
    QFormLayout,
    QFileDialog,
)
from qtpy import QtCore
from main import AIDApp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtCore, QtWidgets

aidapp = AIDApp()

class Gui_Methods:
    def add_output_line(self, string, layout):
        label = QLabel()
        label.setText(str(string))
        label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        layout.addRow(label)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.main_scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.main_scrollArea.setWidgetResizable(True)
        self.main_scrollArea.setObjectName("main_scrollArea")
        self.main_scroll_widget = QtWidgets.QWidget()
        self.main_scroll_widget.setGeometry(QtCore.QRect(0, 0, 774, 550))
        self.main_scroll_widget.setObjectName("main_scroll_widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.main_scroll_widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Input Box
        self.input_box = QtWidgets.QGroupBox(self.main_scroll_widget)
        self.input_box.setMinimumSize(QtCore.QSize(330, 500))
        self.input_box.setMaximumSize(QtCore.QSize(330, 1000))
        self.input_box.setAutoFillBackground(False)
        self.input_box.setFlat(False)
        self.input_box.setCheckable(False)
        self.input_box.setObjectName("input_box")
        self.input_box_layout = QtWidgets.QVBoxLayout(self.input_box)
        self.input_box_layout.setObjectName("input_box_layout")

        # Pushover coord buttons
        self.file_upload_layout = QtWidgets.QHBoxLayout()
        self.file_upload_layout.setObjectName("file_upload_layout")
        self.file_x_button = QtWidgets.QPushButton(self.input_box)
        self.file_x_button.setEnabled(True)
        self.file_x_button.setAutoDefault(False)
        self.file_x_button.setObjectName("file_x_button")
        self.file_upload_layout.addWidget(self.file_x_button)
        self.file_y_button = QtWidgets.QPushButton(self.input_box)
        self.file_y_button.setEnabled(True)
        self.file_y_button.setAutoDefault(False)
        self.file_y_button.setObjectName("file_y_button")
        self.file_upload_layout.addWidget(self.file_y_button)
        self.input_box_layout.addLayout(self.file_upload_layout)
        self.file_x_button.clicked.connect(self.open_x)
        self.file_y_button.clicked.connect(self.open_y)

        # Input value area
        self.input_scroll_area = QtWidgets.QScrollArea(self.input_box)
        self.input_scroll_area.setWidgetResizable(True)
        self.input_scroll_area.setObjectName("input_scroll_area")
        self.input_scroll_widget = QtWidgets.QWidget()
        self.input_scroll_widget.setGeometry(QtCore.QRect(0, 0, 283, 391))
        self.input_scroll_widget.setObjectName("input_scroll_widget")
        self.input_scroll_layout = QtWidgets.QVBoxLayout(self.input_scroll_widget)
        self.input_scroll_layout.setObjectName("input_scroll_layout")

        # dp
        self.dp_layout = QtWidgets.QHBoxLayout()
        self.dp_layout.setObjectName("dp_layout")
        self.dp_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.dp_label.setObjectName("dp_label")
        self.dp_layout.addWidget(self.dp_label)
        self.dp_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.dp_SpinBox.setDecimals(10)
        self.dp_SpinBox.setMaximum(99.0)
        self.dp_SpinBox.setObjectName("dp_SpinBox")
        self.dp_layout.addWidget(self.dp_SpinBox)
        self.input_scroll_layout.addLayout(self.dp_layout)

        # u_DB
        self.u_DB_layout = QtWidgets.QHBoxLayout()
        self.u_DB_layout.setObjectName("u_DB_layout")
        self.u_DB_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.u_DB_label.setObjectName("u_DB_label")
        self.u_DB_layout.addWidget(self.u_DB_label)
        self.u_DB_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.u_DB_SpinBox.setObjectName("u_DB_SpinBox")
        self.u_DB_layout.addWidget(self.u_DB_SpinBox)
        self.input_scroll_layout.addLayout(self.u_DB_layout)

        # k_DB
        self.k_DB_layout = QtWidgets.QHBoxLayout()
        self.k_DB_layout.setObjectName("k_DB_layout")
        self.k_DB_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.k_DB_label.setObjectName("k_DB_label")
        self.k_DB_layout.addWidget(self.k_DB_label)
        self.k_DB_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.k_DB_SpinBox.setObjectName("k_DB_SpinBox")
        self.k_DB_layout.addWidget(self.k_DB_SpinBox)
        self.input_scroll_layout.addLayout(self.k_DB_layout)

        # kf
        self.kf_layout = QtWidgets.QHBoxLayout()
        self.kf_layout.setObjectName("kf_layout")
        self.kf_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.kf_label.setObjectName("kf_label")
        self.kf_layout.addWidget(self.kf_label)
        self.kf_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.kf_SpinBox.setObjectName("kf_SpinBox")
        self.kf_layout.addWidget(self.kf_SpinBox)
        self.input_scroll_layout.addLayout(self.kf_layout)

        # Span length
        self.span_length_layout = QtWidgets.QHBoxLayout()
        self.span_length_layout.setObjectName("span_length_layout")
        self.span_length_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.span_length_label.setObjectName("span_length_label")
        self.span_length_layout.addWidget(self.span_length_label)
        self.span_length_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.span_length_SpinBox.setObjectName("span_length_SpinBox")
        self.span_length_layout.addWidget(self.span_length_SpinBox)
        self.input_scroll_layout.addLayout(self.span_length_layout)

        # Interfloor height
        self.interfloor_height_layout = QtWidgets.QHBoxLayout()
        self.interfloor_height_layout.setObjectName("interfloor_height_layout")
        self.interfloor_height_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.interfloor_height_label.setObjectName("interfloor_height_label")
        self.interfloor_height_layout.addWidget(self.interfloor_height_label)
        self.interfloor_height_SpinBox = QtWidgets.QDoubleSpinBox(self.input_scroll_widget)
        self.interfloor_height_SpinBox.setObjectName("interfloor_height_SpinBox")
        self.interfloor_height_layout.addWidget(self.interfloor_height_SpinBox)
        self.input_scroll_layout.addLayout(self.interfloor_height_layout)

        # Line
        self.line = QtWidgets.QFrame(self.input_scroll_widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.input_scroll_layout.addWidget(self.line)

        # Storey number
        self.storey_number_layout = QtWidgets.QHBoxLayout()
        self.storey_number_layout.setObjectName("storey_number_layout")
        self.storey_number_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.storey_number_label.setObjectName("storey_number_label")
        self.storey_number_layout.addWidget(self.storey_number_label)
        self.storey_number_SpinBox = QtWidgets.QSpinBox(self.input_scroll_widget)
        self.storey_number_SpinBox.setObjectName("storey_number_SpinBox")
        self.storey_number_layout.addWidget(self.storey_number_SpinBox)

        # Send button
        self.send_button = QtWidgets.QPushButton(self.input_scroll_widget)
        self.send_button.setAutoDefault(False)
        self.send_button.setDefault(False)
        self.send_button.setObjectName("send_button")
        self.storey_number_layout.addWidget(self.send_button)
        self.input_scroll_layout.addLayout(self.storey_number_layout)
        self.send_button.clicked.connect(self.count_storey_boxes)


        self.storey_layout = QtWidgets.QFormLayout()
        self.storey_layout.setObjectName("storey_layout")
        self.input_scroll_layout.addLayout(self.storey_layout)
        self.input_scroll_area.setWidget(self.input_scroll_widget)
        self.input_box_layout.addWidget(self.input_scroll_area)

        # Ok button
        self.buttonBox = QtWidgets.QHBoxLayout()
        self.buttonBox.setObjectName("buttonBox")
        self.ok_button = QtWidgets.QPushButton(self.input_box)
        self.ok_button.setObjectName("ok_button")
        self.buttonBox.addWidget(self.ok_button)
        self.input_box_layout.addLayout(self.buttonBox)
        self.ok_button.clicked.connect(self.getInfo)
        self.horizontalLayout.addWidget(self.input_box)

        # Output box
        self.output_box = QtWidgets.QGroupBox(self.main_scroll_widget)
        self.output_box.setObjectName("output_box")
        self.output_box_layout = QtWidgets.QVBoxLayout(self.output_box)
        self.output_box_layout.setObjectName("output_box_layout")
        self.output_scroll_area = QtWidgets.QScrollArea(self.output_box)
        self.output_scroll_area.setWidgetResizable(True)
        self.output_scroll_area.setObjectName("output_scroll_area")
        self.output_scroll_widget = QtWidgets.QWidget()
        self.output_scroll_widget.setGeometry(QtCore.QRect(0, 0, 385, 475))
        self.output_scroll_widget.setObjectName("output_scroll_widget")
        self.output_scroll_layout = QtWidgets.QVBoxLayout(self.output_scroll_widget)
        self.output_scroll_layout.setObjectName("output_scroll_layout")

        self.output_layout = QtWidgets.QFormLayout()
        self.output_layout.setObjectName("output_layout")
        self.output_scroll_layout.addLayout(self.output_layout)
        self.output_scroll_area.setWidget(self.output_scroll_widget)
        self.output_box_layout.addWidget(self.output_scroll_area)
        self.horizontalLayout.addWidget(self.output_box)

        # Graph Box
        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Update layout
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.main_scrollArea.setWidget(self.main_scroll_widget)
        self.verticalLayout_8.addWidget(self.main_scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AIDApp"))
        self.input_box.setTitle(_translate("MainWindow", "Input Values"))
        self.file_x_button.setText(_translate("MainWindow", "X Pushover"))
        self.file_y_button.setText(_translate("MainWindow", "Y Pushover"))
        self.dp_label.setText(_translate("MainWindow", "dp [m]"))
        self.u_DB_label.setText(_translate("MainWindow", "\u03BC_DB"))
        self.k_DB_label.setText(_translate("MainWindow", "\u03BA_DB"))
        self.kf_label.setText(_translate("MainWindow", "\u03BA(F)"))
        self.span_length_label.setText(_translate("MainWindow", "Span Length [m]"))
        self.interfloor_height_label.setText(_translate("MainWindow", "Inter-floor Height [m]"))
        self.storey_number_label.setText(_translate("MainWindow", "# of storeys:"))
        self.send_button.setText(_translate("MainWindow", "Send"))
        self.ok_button.setText(_translate("MainWindow", "Ok"))
        self.output_box.setTitle(_translate("MainWindow", "Output Values"))

    def open_x(self):
        path = QFileDialog.getOpenFileName()
        if path != ("", ""):
            print(path[0])
        self.path_x = path[0]

    def open_y(self):
        path = QFileDialog.getOpenFileName()
        if path != ("", ""):
            print(path[0])
        self.path_y = path[0]

    def getInfo(self):
        storey_masses = []
        for element in self.mass_dict.values():
            storey_masses.append(element.value())
        eigenvalues = []
        for element in self.eigenvalue_dict.values():
            eigenvalues.append(element.value())
        brace_number = []
        for element in self.brace_number_dict.values():
            brace_number.append(element.value())
        # Feed the values to the main program
        output = aidapp.main(
            self.dp_SpinBox.value(),
            self.u_DB_SpinBox.value(),
            self.k_DB_SpinBox.value(),
            self.kf_SpinBox.value(),
            storey_masses,
            eigenvalues,
            brace_number,
            self.path_x,
            self.path_y,
            self.span_length_SpinBox.value(),
            self.interfloor_height_SpinBox.value(),
        )

        self.output_field(output)

    def count_storey_boxes(self):
        self.send_button.setEnabled(False)
        self.show_storey_boxes(self.storey_number_SpinBox.value())


    def show_storey_boxes(self, i):
        self.mass_dict = {}
        self.eigenvalue_dict = {}
        self.brace_number_dict = {}

        k = 1
        while k < (i+1):
            # dynamically create key
            mass_key = k
            eigenvalue_key = k
            brace_number_key = k
            mass_value = QDoubleSpinBox()
            mass_value.setDecimals(3)
            mass_value.setMaximum(10000)
            self.mass_dict[mass_key] = mass_value
            eigenvalue_value = QDoubleSpinBox()
            eigenvalue_value.setDecimals(10)
            self.eigenvalue_dict[eigenvalue_key] = eigenvalue_value
            brace_number_value = QDoubleSpinBox()
            brace_number_value.setDecimals(0)
            self.brace_number_dict[brace_number_key] = brace_number_value

            self.storey_layout.addRow(
                QLabel(f"Storey #{k} mass [ton]"), self.mass_dict[mass_key]
            )
            self.storey_layout.addRow(
                QLabel(f"Storey #{k} eigenvalue"),
                self.eigenvalue_dict[eigenvalue_key],
            )
            self.storey_layout.addRow(
                QLabel(f"Storey #{k} brace #"),
                self.brace_number_dict[brace_number_key],
            )
            k += 1

    def output_field(self, output_values):
        (
            Vy_DB,
            Fy_n_DB_array,
            dy_DB_final,
            Vy_DB_array,
            dy_n_array,
            K_storey_n_array,
            K_n_DB_array,
            kc_n_s_array,
            Fc_n_s_array,
            i,
            x_bilinear,
            y_bilinear_ms2,
            sd_meters,
            sa_ms2,
            kn_eff_list,
            sd_meters_0,
            sa_ms2_0,
        ) = output_values
        i_string = f"Iteration #{i}"
        self.outputLayout = QFormLayout()

        methods = Gui_Methods()
        methods.add_output_line(i_string, self.outputLayout)

        Vy_DB_string = f" \nVy(DB) = {Vy_DB} kN"
        methods.add_output_line(Vy_DB_string, self.outputLayout)

        methods.add_output_line("\nFy,i(DB) array:", self.outputLayout)
        n=1
        for element in Fy_n_DB_array:
            label = "Fy," + str(n) + "(DB)" + " = " + str(element) + " kN"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        methods.add_output_line("\nVy,i(DB) array:", self.outputLayout)
        n=1
        for element in Vy_DB_array:
            label = "Vy," + str(n) + "(DB)" + " = " + str(element) + " kN"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        dy_DB_final_string = f"\ndy(DB) = {dy_DB_final} m"
        methods.add_output_line(dy_DB_final_string, self.outputLayout)

        methods.add_output_line("\ndy,i array:", self.outputLayout)
        n=1
        for element in dy_n_array:
            label = "dy," + str(n) + " = " + str(element) + " m"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        methods.add_output_line("\nKstorey,i array:", self.outputLayout)
        n=1
        for element in K_storey_n_array:
            label = "Kstorey," + str(n) + " = " + str(element) + " kN/m"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        methods.add_output_line("\nKi(DB) array:", self.outputLayout)
        n=1
        for element in K_n_DB_array:
            label = "K" + str(n) + "," + "(DB)" + " = " + str(element) + " kN/m"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        methods.add_output_line("\nkc,i,s array:", self.outputLayout)
        n=1
        for element in kc_n_s_array:
            label = "kc" + str(n) + "," + "(s)" + " = " + str(element) + " kN"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        methods.add_output_line("\nFc,i,s array:", self.outputLayout)
        n=1
        for element in Fc_n_s_array:
            label = "Fc," + str(n) + "," + "(s)" + " = " + str(element) + " kN"
            methods.add_output_line(label, self.outputLayout)
            n = n+1

        # Disable the buttons and SpinBoxes: as of now to user  
        # has to reload the program in order to get new values
        self.file_x_button.setEnabled(False)
        self.file_y_button.setEnabled(False)
        self.ok_button.setEnabled(False)

        self.dp_SpinBox.setEnabled(False)
        self.u_DB_SpinBox.setEnabled(False)
        self.k_DB_SpinBox.setEnabled(False)
        self.kf_SpinBox.setEnabled(False)
        self.span_length_SpinBox.setEnabled(False)
        self.interfloor_height_SpinBox.setEnabled(False)
        self.storey_number_SpinBox.setEnabled(False)

        self.graphLayout = QFormLayout()

        self.plot_final(
            x_bilinear,
            y_bilinear_ms2,
            sd_meters,
            sa_ms2,
            kn_eff_list,
            i,
            sd_meters_0,
            sa_ms2_0,
        )

        self.graph_box = QtWidgets.QGroupBox(self.main_scroll_widget)
        self.graph_box.setObjectName("graph_box")
        self.graph_box.setTitle("Graph")

        self.graph_box_layout = QtWidgets.QVBoxLayout(self.graph_box)
        self.graph_box_layout.setObjectName("graph_box_layout")
        self.graph_scroll_area = QtWidgets.QScrollArea(self.graph_box)
        self.graph_scroll_area.setWidgetResizable(True)
        self.graph_scroll_area.setObjectName("graph_scroll_area")
        self.graph_scroll_widget = QtWidgets.QWidget()
        self.graph_scroll_widget.setObjectName("graph_scroll_widget")
        self.graph_scroll_layout = QtWidgets.QHBoxLayout(self.graph_scroll_widget)
        self.graph_scroll_layout.setObjectName("graph_scroll_layout")

        self.graph_layout = QtWidgets.QFormLayout()
        self.graph_layout.setObjectName("graph_layout")
        self.graph_box.setMinimumSize(QtCore.QSize(500, 500))
        self.graph_scroll_layout.addLayout(self.graphLayout)
        self.graph_scroll_area.setWidget(self.graph_scroll_widget)
        self.graph_box_layout.addWidget(self.graph_scroll_area)
        self.verticalLayout.addWidget(self.graph_box)
        self.graphLayout.addWidget(self.canvas)

        # Display output values
        self.output_scroll_layout.addLayout(self.outputLayout)

    def plot_final(
        self,
        x_bilinear,
        y_bilinear_ms2,
        sd_meters,
        sa_ms2,
        kn_eff_list,
        i,
        sd_meters_0,
        sa_ms2_0,
    ):
        """
        Function to plot the final graph, meant to be displayed when
        all the curves are calculated in the final iteration.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.plot(sd_meters, sa_ms2, color="#002260", label="xi=5%")
        ax.plot(x_bilinear, y_bilinear_ms2, color="#FF0000", label="Bare Frame")
        ax.plot(
            sd_meters,
            kn_eff_list,
            color="#00B050",
            label=("K" + str(i) + "eff"),
        )
        ax.plot(sd_meters_0, sa_ms2_0, color="#FFC000", label="Sa(5%)")

        ax.set_xlabel("Sd [m]", fontsize="large")
        ax.set_ylabel("Sa [m/s^2]", fontsize="large")
        self.canvas.draw()



if __name__ == "__main__":
    from sys import argv, exit

    app = QtWidgets.QApplication(argv)
    Dialog = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()

    exit(app.exec_())
