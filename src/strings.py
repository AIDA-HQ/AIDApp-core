"""Module where the strings are defined."""
from qtpy import QtCore


def retranslate_ui(self, main_window):
    """Set the text of the widgets."""
    main_window.setWindowTitle(
        QtCore.QCoreApplication.translate("MainWindow", "AIDApp")
    )
    self.input_box.setTitle(
        QtCore.QCoreApplication.translate("MainWindow", "Input Values")
    )
    self.zonation_data_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Zonation Data")
    )
    self.zonation_data_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate("MainWindow", "Enter seismic zonation values")
    )
    self.x_p_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "X Pushover")
    )
    self.x_p_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate("MainWindow", "Enter pushover X coordinates")
    )
    self.y_p_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Y Pushover")
    )
    self.y_p_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate("MainWindow", "Enter pushover Y coordinates")
    )
    self.damping_coeff_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Damping coefficient [%]")
    )
    self.nominal_age_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Nominal life [years]")
    )
    self.functional_class_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Functional class")
    )
    self.topographic_factor_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Topographic factor")
    )
    self.soil_class_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Soil class")
    )
    self.limit_state_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Limit State Design")
    )
    self.dp_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "d<sub>p</sub> [m]")
    )
    self.u_DB_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "\u03BC<sub>DB</sub>")
    )
    self.k_DB_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "\u03BA<sub>DB</sub>")
    )
    self.kf_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "\u03BA<sub>(F)</sub>")
    )
    self.span_length_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Span Length [m]")
    )
    self.interfloor_height_label.setText(
        QtCore.QCoreApplication.translate("MainWindow", "Inter-floor Height [m]")
    )
    self.storey_mass_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate("MainWindow", "Enter the mass of each storey")
    )
    self.storey_eigenvalues_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate("MainWindow", "Enter the first eigenvalue")
    )
    self.storey_upwinds_textBox.setPlaceholderText(
        QtCore.QCoreApplication.translate(
            "MainWindow", "Enter the amount of upwinds of each storey"
        )
    )
    self.ok_button.setText(QtCore.QCoreApplication.translate("MainWindow", "Ok"))
    self.output_box.setTitle(
        QtCore.QCoreApplication.translate("MainWindow", "Output Values")
    )
