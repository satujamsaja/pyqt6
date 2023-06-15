from PyQt6.QtWidgets import QDialog, QLabel, QGroupBox, QDialogButtonBox, QLineEdit, QFormLayout, QVBoxLayout
from PyQt6.QtCore import Qt


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
