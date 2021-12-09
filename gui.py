from qtpy.QtWidgets import (
    QDialog,
    QApplication,
    QPushButton,
    QGroupBox,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QDialogButtonBox,
    QFormLayout,
)
from qtpy import QtCore
from main import AIDApp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

aidapp = AIDApp()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("AIDApp")
        Dialog.resize(900, 500)
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")

        # Input Box
        self.input_Box = QGroupBox(Dialog)
        self.input_Box.setEnabled(True)
        self.input_Box.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.input_Box.setAutoFillBackground(False)
        self.input_Box.setFlat(False)
        self.input_Box.setCheckable(False)
        self.input_Box.setObjectName("input_Box")
        self.inputLayout = QFormLayout(self.input_Box)
        self.inputLayout.setObjectName("inputLayout")

        # dp
        self.dp_label = QLabel(self.input_Box)
        self.dp_label.setObjectName("dp_label")
        self.inputLayout.setWidget(0, QFormLayout.LabelRole, self.dp_label)
        self.dp_SpinBar = QDoubleSpinBox(self.input_Box)
        self.dp_SpinBar.setMaximum(99.99)
        self.dp_SpinBar.setDecimals(10)
        self.dp_SpinBar.setObjectName("dp_SpinBar")

        self.inputLayout.setWidget(0, QFormLayout.FieldRole, self.dp_SpinBar)

        # u_DB
        self.u_DB_label = QLabel(self.input_Box)
        self.u_DB_label.setObjectName("u_DB_label")
        self.inputLayout.setWidget(2, QFormLayout.LabelRole, self.u_DB_label)
        self.u_DB_SpinBar = QDoubleSpinBox(self.input_Box)
        self.u_DB_SpinBar.setObjectName("u_DB_SpinBar")

        self.inputLayout.setWidget(2, QFormLayout.FieldRole, self.u_DB_SpinBar)

        # k_DB
        self.k_DB_label = QLabel(self.input_Box)
        self.k_DB_label.setObjectName("k_DB_label")
        self.inputLayout.setWidget(4, QFormLayout.LabelRole, self.k_DB_label)
        self.k_DB_SpinBar = QDoubleSpinBox(self.input_Box)
        self.k_DB_SpinBar.setObjectName("k_DB_SpinBar")

        self.inputLayout.setWidget(4, QFormLayout.FieldRole, self.k_DB_SpinBar)

        # Kf
        self.Kf_label = QLabel(self.input_Box)
        self.Kf_label.setObjectName("Kf_label")
        self.inputLayout.setWidget(5, QFormLayout.LabelRole, self.Kf_label)
        self.Kf_SpinBar = QDoubleSpinBox(self.input_Box)
        self.Kf_SpinBar.setObjectName("Kf_SpinBar")

        self.inputLayout.setWidget(5, QFormLayout.FieldRole, self.Kf_SpinBar)

        # Storey Number
        self.storey_number_label = QLabel(self.input_Box)
        self.storey_number_label.setObjectName("storey_number_label")
        self.inputLayout.setWidget(6, QFormLayout.LabelRole, self.storey_number_label)

        # Send button
        self.sendButton = QPushButton(self.input_Box)
        self.sendButton.setDefault(False)
        self.sendButton.setFlat(False)
        self.sendButton.setObjectName("sendButton")
        self.sendButton.clicked.connect(self.count_storey_boxes)

        self.inputLayout.setWidget(7, QFormLayout.FieldRole, self.sendButton)
        self.storey_number_SpinBar = QSpinBox(self.input_Box)
        self.storey_number_SpinBar.setObjectName("storey_number_SpinBar")
        self.inputLayout.setWidget(7, QFormLayout.LabelRole, self.storey_number_SpinBar)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.input_Box)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.groupBox)

        # Main button
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(Dialog.reject)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonBox)
        self.output_box = QGroupBox(Dialog)
        self.output_box.setObjectName("output_box")
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.output_box)

        # a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("AIDApp", "AIDApp"))
        self.input_Box.setTitle(_translate("AIDApp", "Input Values"))
        self.dp_label.setText(_translate("AIDApp", "dp"))
        self.u_DB_label.setText(_translate("AIDApp", "μ_DB"))
        self.k_DB_label.setText(_translate("AIDApp", "k_DB"))
        self.Kf_label.setText(_translate("AIDApp", "Kf"))
        self.storey_number_label.setText(_translate("AIDApp", "# of storeys:"))
        self.sendButton.setText(_translate("AIDApp", "Send"))
        self.groupBox.setTitle(_translate("AIDApp", "Graph"))
        self.output_box.setTitle(_translate("AIDApp", "Output Values"))

    def getInfo(self):
        storey_masses = []
        for element in mass_dict.values():
            storey_masses.append(element.value())
        eigenvalues = []
        for element in eigenvalue_dict.values():
            eigenvalues.append(element.value())
        # Feed the values to the main program
        output = aidapp.main(
            self.dp_SpinBar.value(),
            self.u_DB_SpinBar.value(),
            self.k_DB_SpinBar.value(),
            self.Kf_SpinBar.value(),
            storey_masses,
            eigenvalues,
        )

        self.output_field(output)

    def count_storey_boxes(self):
        self.sendButton.setEnabled(False)
        self.show_storey_boxes(self.storey_number_SpinBar.value())

    def show_storey_boxes(self, i):
        global mass_dict
        global eigenvalue_dict

        mass_dict = {}
        eigenvalue_dict = {}

        k = 0
        while k < i:
            # dynamically create key
            mass_key = k
            eigenvalue_key = k
            mass_value = QSpinBox()
            mass_value.setMaximum(1000)
            mass_dict[mass_key] = mass_value
            eigenvalue_value = QDoubleSpinBox()
            eigenvalue_value.setDecimals(10)
            eigenvalue_dict[eigenvalue_key] = eigenvalue_value

            self.inputLayout.addRow(
                QLabel("Storey #" + str(k) + " mass"), mass_dict[mass_key]
            )
            self.inputLayout.addRow(
                QLabel("Storey #" + str(k) + " eigenvalue"),
                eigenvalue_dict[eigenvalue_key],
            )
            k += 1
        self.input_Box.setLayout(self.inputLayout)

    def output_field(self, output_values):
        (
            Vp_DB,
            check,
            i,
            Vy_F_DB,
            Vp_F_DB,
            _kn_eff,
            ξ_eff_F_DB,
            ξn_eff,
            check_Vp_DB,
            x_bilinear,
            y_bilinear_ms2,
            sd_meters,
            sa_ms2,
            kn_eff_list,
            sd_meters_0,
            sa_ms2_0,
        ) = output_values
        i_string = "Iteraction #" + str(i)
        Vy_F_DB_string = "Vy_F_DB: " + str(Vy_F_DB) + " m/s^2"
        Vp_F_DB_string = "Vp_F_DB: " + str(Vp_F_DB) + " m/s^2"
        ξ_eff_F_DB_string = "ξ_eff_F_DB: " + str(ξ_eff_F_DB) + " %"
        ξn_eff_string = "ξ" + str(i) + "_eff: " + str(ξn_eff)
        Vp_DB_string = "Vp_DB: " + str(Vp_DB)
        check_string = "check: " + str(check) + " %"
        check_Vp_DB_string = "check_Vp_DB: " + str(check_Vp_DB) + " %"

        self.outputLayout = QFormLayout()

        self.i_label = QLabel()
        self.i_label.setText(i_string)
        self.outputLayout.addRow(self.i_label)

        self.Vp_DB_label = QLabel()
        self.Vp_DB_label.setText(Vp_DB_string)
        self.outputLayout.addRow(self.Vp_DB_label)

        self.Vy_F_DB_label = QLabel()
        self.Vy_F_DB_label.setText(Vy_F_DB_string)
        self.outputLayout.addRow(self.Vy_F_DB_label)

        self.Vp_F_DB_label = QLabel()
        self.Vp_F_DB_label.setText(Vp_F_DB_string)
        self.outputLayout.addRow(self.Vp_F_DB_label)

        self.ξ_eff_F_DB_label = QLabel()
        self.ξ_eff_F_DB_label.setText(ξ_eff_F_DB_string)
        self.outputLayout.addRow(self.ξ_eff_F_DB_label)

        self.ξn_eff_label = QLabel()
        self.ξn_eff_label.setText(ξn_eff_string)
        self.outputLayout.addRow(self.ξn_eff_label)

        self.check_label = QLabel()
        self.check_label.setText(check_string)
        self.outputLayout.addRow(self.check_label)

        self.check_Vp_DB_label = QLabel()
        self.check_Vp_DB_label.setText(check_Vp_DB_string)
        self.outputLayout.addRow(self.check_Vp_DB_label)
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
        self.groupBox.setLayout(self.graphLayout)
        self.graphLayout.addWidget(self.canvas)

        self.output_box.setLayout(self.outputLayout)

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

        ax.plot(sd_meters, sa_ms2, color="#002260", label="ξ=5%")
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
    import sys

    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
