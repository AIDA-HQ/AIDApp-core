"""GUI of AIDApp."""

from qtpy import QtCore, QtWidgets

from aidapp.main import AIDApp

import aidapp.linguist_rc

import aidapp.strings as strings

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure
from aidapp.file_handler import InputHandler, ExportHandler

aidapp = AIDApp()
input_handler = InputHandler()
export_handler = ExportHandler()


class HumbleSpinBox(QtWidgets.QDoubleSpinBox):
    """Class to make spinboxes not scrollable"""

    def __init__(self, *args):
        super(HumbleSpinBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        """Make the spinbox not scrollable when focused."""
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(HumbleSpinBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        """Make the spinbox not scrollable when not focused."""
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(HumbleSpinBox, self).focusOutEvent(event)

    @staticmethod
    def wheelEvent(event):
        """Ignore the wheel event."""
        event.ignore()


class HumbleComboBox(QtWidgets.QComboBox):
    """Class to make comboboxes not scrollable."""

    def __init__(self, *args):
        super(HumbleComboBox, self).__init__(*args)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def focusInEvent(self, event):
        """Make the combobox not scrollable when focused."""
        self.setFocusPolicy(QtCore.Qt.WheelFocus)
        super(HumbleComboBox, self).focusInEvent(event)

    def focusOutEvent(self, event):
        """Make the combobox not scrollable when not focused."""
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        super(HumbleComboBox, self).focusOutEvent(event)

    @staticmethod
    def wheelEvent(event):
        """Ignore the wheel event."""
        event.ignore()


class Ui_MainWindow:
    """Main GUI window."""

    def __init__(self):
        # Init all the self variables
        self.centralwidget = None
        self.main_scrollArea = None
        self.main_scroll_widget = None
        self.verticalLayout_8 = None
        self.verticalLayout = None
        self.horizontalLayout = None
        self.input_box = None
        self.input_box_layout = None
        self.file_upload_layout = None
        self.zonation_ag_label = None
        self.zonation_ag_textBox = None
        self.zonation_fo_label = None
        self.zonation_fo_textBox = None
        self.zonation_tc_label = None
        self.zonation_tc_textBox = None
        self.file_pushover_layout = None
        self.x_p_coord_layout = None
        self.x_p_label = None
        self.x_p_textBox = None
        self.y_p_coord_layout = None
        self.y_p_label = None
        self.y_p_textBox = None
        self.input_scroll_area = None
        self.input_scroll_widget = None
        self.input_scroll_layout = None
        self.damping_coeff_layout = None
        self.damping_coeff_label = None
        self.damping_coeff_SpinBox = None
        self.nominal_age_layout = None
        self.nominal_age_label = None
        self.nominal_age_SpinBox = None
        self.functional_class_layout = None
        self.functional_class_label = None
        self.functional_class_comboBox = None
        self.topographic_factor_layout = None
        self.topographic_factor_label = None
        self.topographic_factor_comboBox = None
        self.soil_class_layout = None
        self.soil_class_label = None
        self.soil_class_comboBox = None
        self.limit_state_layout = None
        self.limit_state_label = None
        self.limit_state_comboBox = None
        self.line_1 = None
        self.kf_layout = None
        self.kf_label = None
        self.kf_SpinBox = None
        self.storey_number_layout = None
        self.storey_number_label = None
        self.storey_data_1row_layout = None
        self.storey_data_2row_layout = None
        self.storey_layout = None
        self.line_2 = None
        self.dp_layout = None
        self.dp_label = None
        self.dp_SpinBox = None
        self.u_DB_layout = None
        self.u_DB_label = None
        self.u_DB_SpinBox = None
        self.k_DB_layout = None
        self.k_DB_label = None
        self.k_DB_SpinBox = None
        self.span_length_layout = None
        self.span_length_label = None
        self.span_length_SpinBox = None
        self.interfloor_height_layout = None
        self.interfloor_height_label = None
        self.interfloor_height_SpinBox = None
        self.buttonBox = None
        self.ok_button = None
        self.output_box = None
        self.output_box_layout = None
        self.output_scroll_widget = None
        self.output_layout = None
        self.figure = None
        self.canvas = None
        self.menubar = None
        self.mass_dict = None
        self.eigenvalue_dict = None
        self.brace_number_dict = None
        self.storey_mass_textBox = None
        self.storey_eigenvalues_textBox = None
        self.storey_upwinds_textBox = None
        self.pushover_x = None
        self.pushover_y = None
        self.zonation_data = None
        self.kc_n_s_array = None
        self.Fc_n_s_array = None
        self.file_export_button = None
        self.graphLayout = None
        self.graph_box = None
        self.graph_box_layout = None
        self.graph_scroll_area = None
        self.graph_scroll_widget = None
        self.graph_scroll_layout = None
        self.graph_layout = None
        self.toolbar = None
        self.show_graph_button = None
        self.translation = None

    def setupUi(self, MainWindow):
        """Setup the GUI."""
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
        self.input_box.setMinimumSize(QtCore.QSize(360, 500))
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

        # Zonation Box
        # External enclosure
        zonation_external_layout = QtWidgets.QHBoxLayout()

        # --
        # ag - first box to the left
        zonation_ag_vertical_layout = QtWidgets.QVBoxLayout()
        zonation_ag_vertical_layout.setObjectName("zonation_ag_vertical_layout")
        # label
        self.zonation_ag_label = QtWidgets.QLabel(self.input_box)
        self.zonation_ag_label.setObjectName("zonation_ag_label")
        self.zonation_ag_label.setMaximumHeight(20)
        self.zonation_ag_label.setAlignment(QtCore.Qt.AlignHCenter)
        zonation_ag_vertical_layout.addWidget(self.zonation_ag_label)
        # text box
        self.zonation_ag_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.zonation_ag_textBox.setObjectName("zonation_ag_textBox")
        self.zonation_ag_textBox.setMinimumHeight(160)
        self.zonation_ag_textBox.setMaximumHeight(160)
        zonation_ag_vertical_layout.addWidget(self.zonation_ag_textBox)

        # --
        # fo - middle box

        zonation_fo_vertical_layout = QtWidgets.QVBoxLayout()
        zonation_fo_vertical_layout.setObjectName("zonation_fo_vertical_layout")
        # label
        self.zonation_fo_label = QtWidgets.QLabel(self.input_box)
        self.zonation_fo_label.setObjectName("zonation_fo_label")
        self.zonation_fo_label.setMaximumHeight(20)
        self.zonation_fo_label.setAlignment(QtCore.Qt.AlignHCenter)
        zonation_fo_vertical_layout.addWidget(self.zonation_fo_label)
        # text box
        self.zonation_fo_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        # disable scrollbar
        self.zonation_fo_textBox.setObjectName("zonation_fo_textBox")
        self.zonation_fo_textBox.setMinimumHeight(160)
        self.zonation_fo_textBox.setMaximumHeight(160)
        zonation_fo_vertical_layout.addWidget(self.zonation_fo_textBox)

        # --
        # Tc - right box

        zonation_tc_vertical_layout = QtWidgets.QVBoxLayout()
        zonation_tc_vertical_layout.setObjectName("zonation_tc_vertical_layout")
        # label
        self.zonation_tc_label = QtWidgets.QLabel(self.input_box)
        self.zonation_tc_label.setObjectName("zonation_tc_label")
        self.zonation_tc_label.setMaximumHeight(20)
        self.zonation_tc_label.setAlignment(QtCore.Qt.AlignHCenter)
        zonation_tc_vertical_layout.addWidget(self.zonation_tc_label)
        # text box
        self.zonation_tc_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.zonation_tc_textBox.setObjectName("zonation_tc_textBox")
        self.zonation_tc_textBox.setMinimumHeight(160)
        self.zonation_tc_textBox.setMaximumHeight(160)
        zonation_tc_vertical_layout.addWidget(self.zonation_tc_textBox)

        # Add the zonation external layout the file upload layout
        zonation_external_layout.addLayout(zonation_ag_vertical_layout)
        zonation_external_layout.addLayout(zonation_fo_vertical_layout)
        zonation_external_layout.addLayout(zonation_tc_vertical_layout)
        self.file_upload_layout.addLayout(zonation_external_layout)

        # Pushover coord buttons
        self.file_pushover_layout = QtWidgets.QHBoxLayout()
        self.file_pushover_layout.setObjectName("file_pushover_layout")

        # X Coordinates
        self.x_p_coord_layout = QtWidgets.QVBoxLayout()
        self.x_p_label = QtWidgets.QLabel(self.input_box)
        self.x_p_label.setObjectName("x_p_label")
        self.x_p_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.x_p_label.setMaximumHeight(20)

        self.x_p_coord_layout.addWidget(self.x_p_label)
        self.x_p_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.x_p_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed
        )
        self.x_p_textBox.setMinimumHeight(75)
        self.x_p_textBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.x_p_coord_layout.addWidget(self.x_p_textBox)

        # Y Coordinates
        self.y_p_coord_layout = QtWidgets.QVBoxLayout()
        self.y_p_label = QtWidgets.QLabel(self.input_box)
        self.y_p_label.setObjectName("y_p_label")
        self.y_p_label.setAlignment(QtCore.Qt.AlignHCenter)
        self.y_p_label.setMaximumHeight(20)

        self.y_p_coord_layout.addWidget(self.y_p_label)
        self.y_p_textBox = QtWidgets.QPlainTextEdit(self.input_box)
        self.y_p_textBox.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed
        )
        self.y_p_textBox.setMinimumHeight(75)
        self.y_p_textBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.y_p_coord_layout.addWidget(self.y_p_textBox)

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

        # Upload storey data
        self.storey_data_1row_layout = QtWidgets.QHBoxLayout()
        self.input_scroll_layout.addLayout(self.storey_data_1row_layout)
        self.storey_data_2row_layout = QtWidgets.QHBoxLayout()
        self.input_scroll_layout.addLayout(self.storey_data_2row_layout)

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

        self.storey_data_1row_layout.addLayout(self.kf_layout)
        self.storey_data_1row_layout.addWidget(self.storey_mass_textBox)

        self.storey_data_2row_layout.addWidget(self.storey_eigenvalues_textBox)
        self.storey_data_2row_layout.addWidget(self.storey_upwinds_textBox)

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

        self.change_lang()  # Set language
        strings.retranslate_ui(self, MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def change_lang(self):
        """Change the language of the application."""
        self.translation = QtCore.QTranslator()
        self.translation.load(":translations/aidapp_it")  # no suffix .qm
        QtWidgets.QApplication.instance().installTranslator(self.translation)

    def getInfo(self):
        """Get the input values from the widgets and send them to the main program."""
        storey_masses = []
        self.pushover_x = self.x_p_textBox.toPlainText()
        self.pushover_y = self.y_p_textBox.toPlainText()
        zonation_ag = self.zonation_ag_textBox.toPlainText()
        zonation_fo = self.zonation_fo_textBox.toPlainText()
        zonation_tc = self.zonation_tc_textBox.toPlainText()
        zonation_data = [zonation_ag, zonation_fo, zonation_tc]

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
            zonation_data,
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

    def output_field(self, output_values):
        """Create and populate the output field."""
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
        """Trigger the generate_output_file function"""
        export_handler.generate_output_file(self.kc_n_s_array, self.Fc_n_s_array)


if __name__ == "__main__":
    import sys

    # Check if the program is being packaged with a splash screen
    # using PyInstaller, if so, close the splash when the it's finished
    # loading.
    import os
    import importlib

    if "_PYIBoot_SPLASH" in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash

        pyi_splash.close()

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())