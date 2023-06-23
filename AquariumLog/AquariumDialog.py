from PyQt6.QtWidgets import QDialog, QLabel, QGroupBox, QDialogButtonBox, QLineEdit, QFormLayout, QVBoxLayout, QDateTimeEdit
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QDoubleValidator

class SignInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Input
        self.input_email = QLineEdit()
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Action button
        self.signin_button = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Close)
        self.signin_button.accepted.connect(self.accept)
        self.signin_button.rejected.connect(self.reject)

        # Load
        self.init_dialog()

    def init_dialog(self):
        # Form
        sign_in_groupbox = QGroupBox('Login')
        sign_in_form_layout = QFormLayout()
        sign_in_form_layout.addRow(QLabel('Email'), self.input_email)
        sign_in_form_layout.addRow(QLabel('Password'), self.input_password)
        sign_in_groupbox.setLayout(sign_in_form_layout)

        # Dialog layout
        sign_in_layout = QVBoxLayout()
        sign_in_layout.addWidget(sign_in_groupbox)
        sign_in_layout.addWidget(self.signin_button)
        self.setLayout(sign_in_layout)

class UploadDataDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Upload Aquarium Data")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Date
        self.date_input = QDateTimeEdit()
        self.date_input.setDateTime(QDateTime.currentDateTime())
        self.date_input.setCalendarPopup(True)
        # Input
        self.validator = QDoubleValidator(0.0, 99.99, 2)
        self.input_ph = QLineEdit()
        self.input_ph.setFixedWidth(150)
        self.input_sg = QLineEdit()
        self.input_sg.setFixedWidth(150)
        self.input_no = QLineEdit()
        self.input_no.setFixedWidth(150)
        self.input_po = QLineEdit()
        self.input_po.setFixedWidth(150)
        self.input_kh = QLineEdit()
        self.input_kh.setFixedWidth(150)
        self.input_ca = QLineEdit()
        self.input_ca.setFixedWidth(150)
        self.input_mg = QLineEdit()
        self.input_mg.setFixedWidth(150)

        # Action button
        self.btn_add_data = QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Close)
        self.btn_add_data.accepted.connect(self.accept)
        self.btn_add_data.rejected.connect(self.reject)

        # Load
        self.init_dialog()

    def init_dialog(self):
        # Form
        upload_data_group = QGroupBox('Add Data')
        upload_data_form_layout = QFormLayout()
        upload_data_form_layout.addRow('Datetime', self.date_input)
        upload_data_form_layout.addRow(QLabel('pH'), self.input_ph)
        upload_data_form_layout.addRow(QLabel('Sg'), self.input_sg)
        upload_data_form_layout.addRow(QLabel('NO3'), self.input_no)
        upload_data_form_layout.addRow(QLabel('PO4'), self.input_po)
        upload_data_form_layout.addRow(QLabel('Kh'), self.input_kh)
        upload_data_form_layout.addRow(QLabel('Ca'), self.input_ca)
        upload_data_form_layout.addRow(QLabel('Mg'), self.input_mg)
        upload_data_group.setLayout(upload_data_form_layout)

        # Layout
        upload_data_layout = QVBoxLayout()
        upload_data_layout.addWidget(upload_data_group)
        upload_data_layout.addWidget(self.btn_add_data)
        self.setLayout(upload_data_layout)

