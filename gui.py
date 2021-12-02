from qtpy.QtWidgets import (
    QDialog,
    QApplication,
    QGroupBox,
    QVBoxLayout,
    QLabel,
    QDoubleSpinBox,
    QSpinBox,
    QDialogButtonBox,
    QFormLayout,
)
import sys
from main import AIDApp

aidapp = AIDApp()


class Window(QDialog):

    # constructor
    def __init__(self):
        super(Window, self).__init__()

        # setting window title
        self.setWindowTitle("AIDApp")

        # setting geometry to the window
        self.setGeometry(100, 100, 300, 400)

        # creating a group box
        self.Input_Box = QGroupBox("Data")

        # creating spin boxes to select input values
        self.dpSpinBar = QDoubleSpinBox()
        self.μ_DB_SpinBar = QDoubleSpinBox()
        self.k_DB_SpinBar = QDoubleSpinBox()
        self.Kf_SpinBar = QDoubleSpinBox()

        self.storey_number_SpinBar = QSpinBox()

        self.dpSpinBar.setDecimals(10)

        # calling the method that create the form
        self.createForm()
        # create a button to display Boxes to fill with storey masses
        self.storeyBox = QDialogButtonBox(QDialogButtonBox.Yes)
        # adding action when form is accepted
        self.storeyBox.accepted.connect(self.count_storey_boxes)

        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)
        # addding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        # creating a vertical layout
        mainLayout = QVBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.Input_Box)
        mainLayout.addWidget(self.storeyBox)

        # adding button box to the layout
        mainLayout.addWidget(self.buttonBox)

        # setting lay out
        self.setLayout(mainLayout)

    # get info method called when form is accepted
    def getInfo(self):

        storey_masses = []
        for element in mass_dict.values():
            storey_masses.append(element.value())

        eigenvalues = []
        for element in eigenvalue_dict.values():
            eigenvalues.append(element.value())
        # Feed the values to the main program
        output = aidapp.main(
            self.dpSpinBar.value(),
            self.μ_DB_SpinBar.value(),
            self.k_DB_SpinBar.value(),
            self.Kf_SpinBar.value(),
            storey_masses,
            eigenvalues,
        )

        self.output_field(output)

    def count_storey_boxes(self):
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

            # calculate value
            mass_value = QSpinBox()
            mass_value.setMaximum(1000)
            mass_dict[mass_key] = mass_value

            eigenvalue_value = QDoubleSpinBox()
            eigenvalue_value.setDecimals(10)
            eigenvalue_dict[eigenvalue_key] = eigenvalue_value

            self.layout.addRow(
                QLabel("Storey #" + str(k) + " mass"), mass_dict[mass_key]
            )
            self.layout.addRow(
                QLabel("Storey #" + str(k) + " eigenvalue"),
                eigenvalue_dict[eigenvalue_key],
            )
            k += 1

    # creat form method
    def createForm(self):

        # creating a form layout
        self.layout = QFormLayout()

        # adding rows
        self.layout.addRow(QLabel("dp"), self.dpSpinBar)
        self.layout.addRow(QLabel("μ_DB"), self.μ_DB_SpinBar)
        self.layout.addRow(QLabel("k_DB"), self.k_DB_SpinBar)
        self.layout.addRow(QLabel("Kf"), self.Kf_SpinBar)
        self.layout.addRow(QLabel("# Storeys"), self.storey_number_SpinBar)

        # setting layout
        self.Input_Box.setLayout(self.layout)

    def output_field(self, output_values):
        (
            Vp_DB,
            check,
            i,
            Vy_F_DB,
            Vp_F_DB,
            kn_eff,
            ξ_eff_F_DB,
            ξn_eff,
            check_Vp_DB,
        ) = output_values

        i_string = "Iteraction #" + str(i)
        Vy_F_DB_string = "Vy_F_DB: " + str(Vy_F_DB) + " m/s^2"
        Vp_F_DB_string = "Vp_F_DB: " + str(Vp_F_DB) + " m/s^2"
        ξ_eff_F_DB_string = "ξ_eff_F_DB: " + str(ξ_eff_F_DB) + " %"
        ξn_eff_string = "ξ" + str(i) + "_eff: " + str(ξn_eff)
        Vp_DB_string = "Vp_DB: " + str(Vp_DB)
        check_string = "check: " + str(check) + " %"
        check_Vp_DB_string = "check_Vp_DB: " + str(check_Vp_DB) + " %"

        self.i_label = QLabel()
        self.i_label.setText(i_string)
        self.layout.addRow(self.i_label)

        self.Vp_DB_label = QLabel()
        self.Vp_DB_label.setText(Vp_DB_string)
        self.layout.addRow(self.Vp_DB_label)

        self.Vy_F_DB_label = QLabel()
        self.Vy_F_DB_label.setText(Vy_F_DB_string)
        self.layout.addRow(self.Vy_F_DB_label)

        self.Vp_F_DB_label = QLabel()
        self.Vy_F_DB_label.setText(Vp_F_DB_string)
        self.layout.addRow(self.Vy_F_DB_label)

        self.ξ_eff_F_DB_label = QLabel()
        self.ξ_eff_F_DB_label.setText(ξ_eff_F_DB_string)
        self.layout.addRow(self.ξ_eff_F_DB_label)

        self.ξn_eff_label = QLabel()
        self.ξn_eff_label.setText(ξn_eff_string)
        self.layout.addRow(self.ξn_eff_label)

        self.check_label = QLabel()
        self.ξn_eff_label.setText(check_string)
        self.layout.addRow(self.check_label)

        self.check_Vp_DB_label = QLabel()
        self.ξn_eff_label.setText(check_Vp_DB_string)
        self.layout.addRow(self.check_Vp_DB_label)


# main method
if __name__ == "__main__":

    # create pyqt5 app
    app = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()
    # showing the window
    window.show()

    # start the app
    sys.exit(app.exec())
