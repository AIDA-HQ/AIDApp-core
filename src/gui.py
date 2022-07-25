from qtpy import QtCore, QtWidgets

from main import AIDApp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from file_handler import InputHandler, ExportHandler

aidapp = AIDApp()
input_handler = InputHandler()
export_handler = ExportHandler()


class HumbleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, *args):
        super(HumbleSpinBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(HumbleSpinBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(HumbleSpinBox, self).focusOutEvent(event)

    @staticmethod
    def wheelEvent(event):
        event.ignore()


class HumbleComboBox(QtWidgets.QComboBox):
    def __init__(self, *args):
        super(HumbleComboBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(HumbleComboBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(HumbleComboBox, self).focusOutEvent(event)

    @staticmethod
    def wheelEvent(event):
        event.ignore()


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 700)
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
        self.input_box.setMinimumSize(QtCore.QSize(325, 500))
        self.input_box.setMaximumSize(QtCore.QSize(380, 1000))
        self.input_box.setAutoFillBackground(False)
        self.input_box.setFlat(False)
        self.input_box.setCheckable(False)
        self.input_box.setObjectName("input_box")
        self.input_box_layout = QtWidgets.QVBoxLayout(self.input_box)
        self.input_box_layout.setObjectName("input_box_layout")

        # File upload boxes layout
        self.file_upload_layout = QtWidgets.QVBoxLayout()
        self.file_upload_layout.setObjectName("file_upload_layout")

        # Zonation button
        self.file_zonation_button = QtWidgets.QPushButton(self.input_box)
        self.file_zonation_button.setEnabled(True)
        self.file_zonation_button.setAutoDefault(False)
        self.file_zonation_button.setObjectName("file_zonation_button")
        self.file_upload_layout.addWidget(self.file_zonation_button)
        self.file_zonation_button.clicked.connect(self.open_zonation)

        # Pushover coord buttons
        self.file_pushover_layout = QtWidgets.QHBoxLayout()
        self.file_pushover_layout.setObjectName("file_pushover_layout")

        # X Coordinates
        self.x_p_coord_layout = QtWidgets.QVBoxLayout()
        self.x_label = QtWidgets.QLabel(self.input_box)
        self.x_label.setObjectName("x_label")
        self.x_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.x_p_coord_layout.addWidget(self.x_label)
        self.x_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.x_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed
        )
        self.x_textBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.x_p_coord_layout.addWidget(self.x_textBox)

        # Y Coordinates
        self.y_p_coord_layout = QtWidgets.QVBoxLayout()
        self.y_label = QtWidgets.QLabel(self.input_box)
        self.y_label.setObjectName("y_label")
        self.y_label.setAlignment(QtCore.Qt.AlignHCenter)

        self.y_p_coord_layout.addWidget(self.y_label)
        self.y_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.y_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed
        )
        self.y_textBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.y_p_coord_layout.addWidget(self.y_textBox)

        # Add Layout
        self.file_upload_layout.addLayout(self.file_pushover_layout)
        self.file_pushover_layout.addLayout(self.x_p_coord_layout)
        self.file_pushover_layout.addLayout(self.y_p_coord_layout)
        self.input_box_layout.addLayout(self.file_upload_layout)

        # Input value area
        self.input_scroll_area = QtWidgets.QScrollArea(self.input_box)
        self.input_scroll_area.setWidgetResizable(True)
        self.input_scroll_area.setObjectName("input_scroll_area")
        self.input_scroll_widget = QtWidgets.QWidget()
        self.input_scroll_widget.setGeometry(QtCore.QRect(0, 0, 283, 391))
        self.input_scroll_widget.setObjectName("input_scroll_widget")
        self.input_scroll_layout = QtWidgets.QVBoxLayout(self.input_scroll_widget)
        self.input_scroll_layout.setObjectName("input_scroll_layout")

        # Damping coefficient
        self.damping_coeff_layout = QtWidgets.QHBoxLayout()
        self.damping_coeff_layout.setObjectName("damping_coeff_layout")
        self.damping_coeff_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.damping_coeff_label.setObjectName("damping_coeff_label")
        self.damping_coeff_layout.addWidget(self.damping_coeff_label)
        self.damping_coeff_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.damping_coeff_SpinBox.setMaximum(100)
        self.damping_coeff_SpinBox.setDecimals(0)
        self.damping_coeff_SpinBox.setObjectName("damping_coeff_SpinBox")
        self.damping_coeff_layout.addWidget(self.damping_coeff_SpinBox)
        self.input_scroll_layout.addLayout(self.damping_coeff_layout)

        # Nominal life
        self.nominal_age_layout = QtWidgets.QHBoxLayout()
        self.nominal_age_layout.setObjectName("nominal_age_layout")
        self.nominal_age_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.nominal_age_label.setObjectName("nominal_age_label")
        self.nominal_age_layout.addWidget(self.nominal_age_label)
        self.nominal_age_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.nominal_age_SpinBox.setMaximum(9999)
        self.nominal_age_SpinBox.setDecimals(0)
        self.nominal_age_SpinBox.setObjectName("nominal_age_SpinBox")
        self.nominal_age_layout.addWidget(self.nominal_age_SpinBox)
        self.input_scroll_layout.addLayout(self.nominal_age_layout)

        # Functional class
        self.functional_class_layout = QtWidgets.QHBoxLayout()
        self.functional_class_layout.setObjectName("functional_class_layout")
        self.functional_class_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.functional_class_label.setObjectName("functional_class_label")
        self.functional_class_layout.addWidget(self.functional_class_label)
        self.input_scroll_layout.addLayout(self.functional_class_layout)
        self.functional_class_comboBox = HumbleComboBox(self.input_scroll_widget)
        self.functional_class_comboBox.setObjectName("comboBox")
        self.functional_class_comboBox.addItems(["I", "II", "III", "IV"])
        self.functional_class_layout.addWidget(self.functional_class_comboBox)

        # Topographic factor
        self.topographic_factor_layout = QtWidgets.QHBoxLayout()
        self.topographic_factor_layout.setObjectName("topographic_factor_layout")
        self.topographic_factor_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.topographic_factor_label.setObjectName("topographic_factor_label")
        self.topographic_factor_layout.addWidget(self.topographic_factor_label)
        self.input_scroll_layout.addLayout(self.topographic_factor_layout)
        self.topographic_factor_comboBox = HumbleComboBox(self.input_scroll_widget)
        self.topographic_factor_comboBox.setObjectName("comboBox")
        self.topographic_factor_comboBox.addItems(["T1", "T2", "T3", "T4"])
        self.topographic_factor_layout.addWidget(self.topographic_factor_comboBox)

        # Soil class
        self.soil_class_layout = QtWidgets.QHBoxLayout()
        self.soil_class_layout.setObjectName("soil_class_layout")
        self.soil_class_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.soil_class_label.setObjectName("soil_class_label")
        self.soil_class_layout.addWidget(self.soil_class_label)
        self.input_scroll_layout.addLayout(self.soil_class_layout)
        self.soil_class_comboBox = HumbleComboBox(self.input_scroll_widget)
        self.soil_class_comboBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.soil_class_comboBox.setObjectName("comboBox")
        self.soil_class_comboBox.addItems(["A", "B", "C", "D", "E"])
        self.soil_class_layout.addWidget(self.soil_class_comboBox)

        # Limit state design
        self.limit_state_layout = QtWidgets.QHBoxLayout()
        self.limit_state_layout.setObjectName("limit_state_layout")
        self.limit_state_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.limit_state_label.setObjectName("limit_state_label")
        self.limit_state_layout.addWidget(self.limit_state_label)
        self.input_scroll_layout.addLayout(self.limit_state_layout)
        self.limit_state_comboBox = HumbleComboBox(self.input_scroll_widget)
        self.limit_state_comboBox.setObjectName("comboBox")
        self.limit_state_comboBox.addItems(["SLO", "SLD", "SLV", "SLC"])
        self.limit_state_layout.addWidget(self.limit_state_comboBox)

        # Line 1
        self.line_1 = QtWidgets.QFrame(self.input_scroll_widget)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.input_scroll_layout.addWidget(self.line_1)

        # kf
        self.kf_layout = QtWidgets.QHBoxLayout()
        self.kf_layout.setObjectName("kf_layout")
        self.kf_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.kf_label.setObjectName("kf_label")
        self.kf_layout.addWidget(self.kf_label)
        self.kf_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.kf_SpinBox.setSingleStep(0.01)
        self.kf_SpinBox.setObjectName("kf_SpinBox")
        self.kf_layout.addWidget(self.kf_SpinBox)
        self.input_scroll_layout.addLayout(self.kf_layout)

        # Storey number
        self.storey_number_layout = QtWidgets.QHBoxLayout()
        self.storey_number_layout.setObjectName("storey_number_layout")
        self.storey_number_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.storey_number_label.setObjectName("storey_number_label")
        self.storey_number_label.setDisabled(True)
        self.storey_number_layout.addWidget(self.storey_number_label)
        self.storey_number_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.storey_number_SpinBox.setObjectName("storey_number_SpinBox")
        self.storey_number_SpinBox.setDecimals(0)
        self.storey_number_SpinBox.setDisabled(True)
        self.storey_number_layout.addWidget(self.storey_number_SpinBox)

        # Send button
        self.send_button = QtWidgets.QPushButton(self.input_scroll_widget)
        self.send_button.setAutoDefault(False)
        self.send_button.setDisabled(True)
        self.send_button.setDefault(False)
        self.send_button.setObjectName("send_button")
        self.storey_number_layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.count_storey_boxes)

        # Upload storey data
        self.storey_data_1row_layout = QtWidgets.QHBoxLayout()
        self.input_scroll_layout.addLayout(self.storey_data_1row_layout)
        self.storey_data_2row_layout = QtWidgets.QHBoxLayout()
        self.input_scroll_layout.addLayout(self.storey_data_2row_layout)

        self.storey_data_button = QtWidgets.QPushButton(self.input_scroll_widget)
        self.storey_data_button.setAutoDefault(False)
        self.storey_data_button.setDefault(False)
        self.storey_data_button.setObjectName("storey_data_button")
        self.storey_data_1row_layout.addWidget(self.storey_data_button)
        self.storey_data_button.clicked.connect(self.show_storey_data_boxes)

        # Manual storey input radio button
        self.manual_input_checkBox = QtWidgets.QCheckBox(self.input_box)
        self.manual_input_checkBox.setObjectName("manual_input_checkBox")
        self.manual_input_checkBox.toggled.connect(self.send_button.setEnabled)
        self.manual_input_checkBox.toggled.connect(
            self.storey_number_SpinBox.setEnabled
        )
        self.manual_input_checkBox.toggled.connect(self.storey_number_label.setEnabled)
        self.manual_input_checkBox.toggled.connect(self.storey_data_button.setDisabled)
        self.input_scroll_layout.addWidget(self.manual_input_checkBox)

        # Add Storey number layout
        self.input_scroll_layout.addLayout(self.storey_number_layout)
        self.storey_layout = QtWidgets.QFormLayout()
        self.storey_layout.setObjectName("storey_layout")
        self.input_scroll_layout.addLayout(self.storey_layout)

        # Update UI
        self.input_scroll_area.setWidget(self.input_scroll_widget)
        self.input_box_layout.addWidget(self.input_scroll_area)

        # Line 2
        self.line_2 = QtWidgets.QFrame(self.input_scroll_widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.input_scroll_layout.addWidget(self.line_2)

        # dp
        self.dp_layout = QtWidgets.QHBoxLayout()
        self.dp_layout.setObjectName("dp_layout")
        self.dp_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.dp_label.setObjectName("dp_label")
        self.dp_layout.addWidget(self.dp_label)
        self.dp_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.dp_SpinBox.setDecimals(10)
        self.dp_SpinBox.setMaximum(99.0)
        self.dp_SpinBox.setSingleStep(0.0000000001)
        self.dp_SpinBox.setObjectName("dp_SpinBox")
        self.dp_layout.addWidget(self.dp_SpinBox)
        self.input_scroll_layout.addLayout(self.dp_layout)

        # u_DB
        self.u_DB_layout = QtWidgets.QHBoxLayout()
        self.u_DB_layout.setObjectName("u_DB_layout")
        self.u_DB_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.u_DB_label.setObjectName("u_DB_label")
        self.u_DB_layout.addWidget(self.u_DB_label)
        self.u_DB_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.u_DB_SpinBox.setSingleStep(0.01)
        self.u_DB_SpinBox.setObjectName("u_DB_SpinBox")
        self.u_DB_layout.addWidget(self.u_DB_SpinBox)
        self.input_scroll_layout.addLayout(self.u_DB_layout)

        # k_DB
        self.k_DB_layout = QtWidgets.QHBoxLayout()
        self.k_DB_layout.setObjectName("k_DB_layout")
        self.k_DB_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.k_DB_label.setObjectName("k_DB_label")
        self.k_DB_layout.addWidget(self.k_DB_label)
        self.k_DB_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.k_DB_SpinBox.setSingleStep(0.01)
        self.k_DB_SpinBox.setObjectName("k_DB_SpinBox")
        self.k_DB_layout.addWidget(self.k_DB_SpinBox)
        self.input_scroll_layout.addLayout(self.k_DB_layout)

        # Span length
        self.span_length_layout = QtWidgets.QHBoxLayout()
        self.span_length_layout.setObjectName("span_length_layout")
        self.span_length_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.span_length_label.setObjectName("span_length_label")
        self.span_length_layout.addWidget(self.span_length_label)
        self.span_length_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.span_length_SpinBox.setObjectName("span_length_SpinBox")
        self.span_length_SpinBox.setMaximum(99)
        self.span_length_SpinBox.setSingleStep(0.01)
        self.span_length_layout.addWidget(self.span_length_SpinBox)
        self.input_scroll_layout.addLayout(self.span_length_layout)

        # Interfloor height
        self.interfloor_height_layout = QtWidgets.QHBoxLayout()
        self.interfloor_height_layout.setObjectName("interfloor_height_layout")
        self.interfloor_height_label = QtWidgets.QLabel(self.input_scroll_widget)
        self.interfloor_height_label.setObjectName("interfloor_height_label")
        self.interfloor_height_layout.addWidget(self.interfloor_height_label)
        self.interfloor_height_SpinBox = HumbleSpinBox(self.input_scroll_widget)
        self.interfloor_height_SpinBox.setObjectName("interfloor_height_SpinBox")
        self.interfloor_height_SpinBox.setMaximum(99)
        self.interfloor_height_SpinBox.setSingleStep(0.01)
        self.interfloor_height_layout.addWidget(self.interfloor_height_SpinBox)
        self.input_scroll_layout.addLayout(self.interfloor_height_layout)

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
        self.output_scroll_widget = QtWidgets.QWidget()
        self.output_scroll_widget.setGeometry(QtCore.QRect(0, 0, 385, 475))
        self.output_scroll_widget.setObjectName("output_scroll_widget")

        self.output_layout = QtWidgets.QFormLayout()
        self.output_layout.setObjectName("output_layout")
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

        self.mass_dict = {}
        self.eigenvalue_dict = {}
        self.brace_number_dict = {}

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AIDApp"))
        self.input_box.setTitle(_translate("MainWindow", "Input Values"))
        self.file_zonation_button.setText(
            _translate("MainWindow", "Seismic Zonation Values")
        )
        self.x_label.setText(_translate("MainWindow", "X Pushover"))
        self.x_textBox.setPlaceholderText(
            _translate("MainWindow", "Enter X Coordinates")
        )
        self.y_label.setText(_translate("MainWindow", "Y Pushover"))
        self.y_textBox.setPlaceholderText(
            _translate("MainWindow", "Enter Y Coordinates")
        )
        self.damping_coeff_label.setText(
            _translate("MainWindow", "Damping coefficient [%]")
        )
        self.nominal_age_label.setText(_translate("MainWindow", "Nominal life [years]"))
        self.functional_class_label.setText(
            _translate("MainWindow", "Functional class")
        )
        self.topographic_factor_label.setText(
            _translate("MainWindow", "Topographic factor")
        )
        self.soil_class_label.setText(_translate("MainWindow", "Soil class"))
        self.limit_state_label.setText(_translate("MainWindow", "Limit State Design"))
        self.dp_label.setText(_translate("MainWindow", "d<sub>p</sub> [m]"))
        self.u_DB_label.setText(_translate("MainWindow", "\u03BC<sub>DB</sub>"))
        self.k_DB_label.setText(_translate("MainWindow", "\u03BA<sub>DB</sub>"))
        self.kf_label.setText(_translate("MainWindow", "\u03BA<sub>(F)</sub>"))
        self.span_length_label.setText(_translate("MainWindow", "Span Length [m]"))
        self.interfloor_height_label.setText(
            _translate("MainWindow", "Inter-floor Height [m]")
        )
        self.manual_input_checkBox.setText(_translate("MainWindow", "Manual Input"))
        self.storey_number_label.setText(_translate("MainWindow", "# of storeys:"))
        self.send_button.setText(_translate("MainWindow", "Send"))
        self.storey_data_button.setText(_translate("MainWindow", "Show Storey Data"))
        self.ok_button.setText(_translate("MainWindow", "Ok"))
        self.output_box.setTitle(_translate("MainWindow", "Output Values"))

    def open_zonation(self):
        path = QtWidgets.QFileDialog.getOpenFileName()
        if path != ("", ""):
            print(path[0])
        self.path_zonation = path[0]

    def show_storey_data_boxes(self):
        """Show the boxes to input data masses, eigenvalues, and brace numbers"""
        # Storey mass
        self.storey_mass_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.storey_mass_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )

        # Storey eigenvalues
        self.storey_eigenvalues_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.storey_eigenvalues_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )

        # Storey upwinds
        self.storey_upwinds_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.storey_upwinds_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )

        self.storey_mass_textBox.setPlaceholderText(
            ("Enter masses of each storey")
        )
        self.storey_eigenvalues_textBox.setPlaceholderText(
            ("Enter eigenvalues for each storey")
        )
        self.storey_upwinds_textBox.setPlaceholderText(
            ("Enter the amount of Upwinds for each storey")
        )

        self.storey_data_1row_layout.addWidget(self.storey_mass_textBox)
        self.storey_data_2row_layout.addWidget(self.storey_eigenvalues_textBox)
        self.storey_data_2row_layout.addWidget(self.storey_upwinds_textBox)
        self.storey_data_button.setDisabled(True)

    def getInfo(self):
        storey_masses = []
        self.pushover_x = self.x_textBox.toPlainText()
        self.pushover_y = self.y_textBox.toPlainText()

        if self.mass_dict is True:
            for element in self.mass_dict.values():
                storey_masses.append(element.value())
            eigenvalues = []
            for element in self.eigenvalue_dict.values():
                eigenvalues.append(element.value())
            brace_number = []
            for element in self.brace_number_dict.values():
                brace_number.append(element.value())
        else:
            storey_masses = input_handler.generate_storey_data(
                self.storey_mass_textBox.toPlainText()
            )
            eigenvalues = input_handler.generate_storey_data(
                self.storey_eigenvalues_textBox.toPlainText()
            )
            brace_number = input_handler.generate_storey_data(
                self.storey_upwinds_textBox.toPlainText()
            )

        # Feed the values to the main program
        output = aidapp.main(
            self.dp_SpinBox.value(),
            self.u_DB_SpinBox.value(),
            self.k_DB_SpinBox.value(),
            self.kf_SpinBox.value(),
            storey_masses,
            eigenvalues,
            brace_number,
            self.path_zonation,
            self.pushover_x,
            self.pushover_y,
            self.span_length_SpinBox.value(),
            self.interfloor_height_SpinBox.value(),
            self.nominal_age_SpinBox.value(),
            self.functional_class_comboBox.currentText(),
            self.topographic_factor_comboBox.currentText(),
            self.soil_class_comboBox.currentText(),
            self.limit_state_comboBox.currentText(),
            self.damping_coeff_SpinBox.value(),
        )

        self.output_field(output)

    def count_storey_boxes(self):
        self.send_button.setDisabled(True)
        self.storey_number_SpinBox.setDisabled(True)
        self.show_storey_boxes(self.storey_number_SpinBox.value())

    def show_storey_boxes(self, i):
        k = 1
        while k < (i + 1):
            # dynamically create key
            mass_key = k
            eigenvalue_key = k
            brace_number_key = k
            mass_value = HumbleSpinBox()
            mass_value.setMaximum(10000)
            mass_value.setDecimals(0)
            self.mass_dict[mass_key] = mass_value
            eigenvalue_value = HumbleSpinBox()
            eigenvalue_value.setDecimals(10)
            eigenvalue_value.setSingleStep(0.0000000001)
            self.eigenvalue_dict[eigenvalue_key] = eigenvalue_value
            brace_number_value = HumbleSpinBox()
            brace_number_value.setDecimals(0)
            self.brace_number_dict[brace_number_key] = brace_number_value

            self.storey_layout.addRow(
                QtWidgets.QLabel(f"Storey #{k} mass [ton]"), self.mass_dict[mass_key]
            )
            self.storey_layout.addRow(
                QtWidgets.QLabel(f"Storey #{k} eigenvalue"),
                self.eigenvalue_dict[eigenvalue_key],
            )
            self.storey_layout.addRow(
                QtWidgets.QLabel(f"Storey #{k} brace #"),
                self.brace_number_dict[brace_number_key],
            )
            k += 1

    def output_field(self, output_values):
        (
            self.kc_n_s_array,
            self.Fc_n_s_array,
            i,
            x_bilinear,
            y_bilinear_ms2,
            sd_meters,
            sa_ms2,
            kn_eff_list,
            y_bilinear_ms2_0,
            kn_eff_list_0,
            de_0,
            de_n,
            dp,
        ) = output_values
        output_textbrowser = QtWidgets.QTextBrowser()
        output_textbrowser.setAcceptRichText(True)
        output_textbrowser.setAutoFillBackground(True)

        output_textbrowser.append(f"Iteration #{i}")
        output_textbrowser.append("\n")
        output_textbrowser.append("kc,<sub>i,<sub>s</sub></sub> array:")
        n = 1
        for element in self.kc_n_s_array:
            label = (
                "kc"
                + "<sub>"
                + str(n)
                + ","
                + "<sub>s</sub></sub>"
                + " = "
                + str(element)
                + " kN"
            )
            output_textbrowser.append(label)
            n = n + 1

        n = 1
        output_textbrowser.append("\n")
        output_textbrowser.append("Fc,<sub>i,<sub>s</sub></sub> array:")
        for element in self.Fc_n_s_array:
            label = (
                "Fc,"
                + "<sub>"
                + str(n)
                + ","
                + "<sub>s</sub></sub>"
                + " = "
                + str(element)
                + " kN"
            )
            output_textbrowser.append(label)
            n = n + 1

        # Disable the buttons and SpinBoxes: as of now to user
        # has to reload the program in order to get new values
        self.file_zonation_button.setEnabled(False)
        self.ok_button.setEnabled(False)
        self.damping_coeff_SpinBox.setEnabled(False)
        self.nominal_age_SpinBox.setEnabled(False)
        self.functional_class_comboBox.setEnabled(False)
        self.topographic_factor_comboBox.setEnabled(False)
        self.soil_class_comboBox.setEnabled(False)
        self.limit_state_comboBox.setEnabled(False)
        self.dp_SpinBox.setEnabled(False)
        self.u_DB_SpinBox.setEnabled(False)
        self.k_DB_SpinBox.setEnabled(False)
        self.kf_SpinBox.setEnabled(False)
        self.span_length_SpinBox.setEnabled(False)
        self.interfloor_height_SpinBox.setEnabled(False)
        self.storey_data_button.setEnabled(False)
        self.manual_input_checkBox.setEnabled(False)

        # File Export button
        self.file_export_button = QtWidgets.QPushButton(self.output_box)
        self.file_export_button.setText("Export Output Values")
        self.file_export_button.setEnabled(True)
        self.file_export_button.setAutoDefault(False)
        self.file_export_button.setObjectName("file_export_button")
        self.file_export_button.clicked.connect(self.trigger_generate_output_file)

        # Graph
        def plot_graph():
            """Plot the graph of the response spectrum"""
            from graph import Graph

            gr = Graph()
            gr.plot_final(
                x_bilinear,
                y_bilinear_ms2,
                sd_meters,
                sa_ms2,
                kn_eff_list,
                self.figure,
                self.canvas,
                y_bilinear_ms2_0,
                kn_eff_list_0,
                de_0,
                de_n,
                dp,
            )

            self.graphLayout = QtWidgets.QFormLayout()
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
            self.graph_box.setMinimumSize(QtCore.QSize(500, 700))
            self.graph_scroll_layout.addLayout(self.graphLayout)
            self.graph_scroll_area.setWidget(self.graph_scroll_widget)
            self.graph_box_layout.addWidget(self.graph_scroll_area)

            self.graph_scroll_layout.addWidget(self.canvas)
            self.toolbar = NavigationToolbar(self.canvas, self.graph_scroll_area)
            self.graph_box_layout.addWidget(self.toolbar)

            self.verticalLayout.addWidget(self.graph_box)
            self.show_graph_button.setEnabled(False)

        # Show graph button
        self.show_graph_button = QtWidgets.QPushButton(self.output_box)
        self.show_graph_button.setText("Show graph")
        self.show_graph_button.setEnabled(True)
        self.show_graph_button.setAutoDefault(False)
        self.show_graph_button.setObjectName("show_graph_button")
        self.show_graph_button.clicked.connect(plot_graph)

        # Display output values & Export button
        self.output_box_layout.addWidget(output_textbrowser)
        self.output_box_layout.addWidget(self.show_graph_button)
        self.output_box_layout.addWidget(self.file_export_button)

    def trigger_generate_output_file(self):
        export_handler.generate_output_file(self.kc_n_s_array, self.Fc_n_s_array)


if __name__ == "__main__":
    from sys import argv, exit

    # Check if the program is being packaged with a splash screen
    # using PyInstaller, if so, close the splash when the it's finished
    # loading.
    import os
    import importlib

    if "_PYIBoot_SPLASH" in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash

        pyi_splash.close()

    app = QtWidgets.QApplication(argv)
    Dialog = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()

    exit(app.exec_())
