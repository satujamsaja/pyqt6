import sys

import requests.exceptions
import yaml
import json
import pyrebase
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QTableWidget , QTableWidgetItem,
    QHeaderView, QPushButton, QDialogButtonBox, QMessageBox, QDateTimeEdit  )

from PyQt6.QtGui import QIcon, QPixmap, QImage, QDoubleValidator
from PyQt6.QtCore import Qt

from AquariumDialog import SignInDialog, UploadDataDialog

class AquariumLog(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aquarium Log')
        self.setFixedWidth(900)
        self.setFixedHeight(780)
        # Define image container
        self.tank_image_container = QLabel('')
        # Define buttons
        self.sign_in_btn = QPushButton('Sign In')
        self.sign_in_btn.setFixedHeight(60)
        self.sign_in_btn.clicked.connect(self.open_signin_dialog)
        self.sign_out_btn = QPushButton('Sign Out')
        self.sign_out_btn.setFixedHeight(60)
        #self.sign_out_btn.setVisible(False)
        self.sign_out_btn.clicked.connect(self.disconnect_firebase)
        self.upload_photo_btn = QPushButton('Upload Photos')
        self.upload_photo_btn.setFixedHeight(60)
        #self.upload_photo_btn.setDisabled(True)
        self.display_graphics_btn = QPushButton('Display Graphics')
        self.display_graphics_btn.setFixedHeight(60)
        self.display_graphics_btn.setDisabled(True)
        self.upload_data_btn = QPushButton('Upload Data')
        self.upload_data_btn.setFixedHeight(60)
        #self.upload_data_btn.setDisabled(True)
        self.upload_data_btn.clicked.connect(self.open_upload_data_dialog)
        # Load ui
        self.init_dashboard_ui()
        # Load config
        self.load_config()
        # Init firebase
        self.init_firebase()
        # Users
        self.user = {}

    def init_dashboard_ui(self):
        dashboard_layout = QVBoxLayout()
        # Tank photo container
        dashboard_image_groupbox = QGroupBox('Photo')
        # Tank photo image
        dashboard_image_tank_layout = QVBoxLayout()
        # tank_image_container = QLabel('')
        # tank_image = QImage('tank.jpeg')
        # tank_image_pixmap = QPixmap.fromImage(tank_image.scaled(860,400))
        # tank_image_container.setPixmap(tank_image_pixmap)
        dashboard_image_tank_layout.addWidget(self.tank_image_container)
        dashboard_image_groupbox.setLayout(dashboard_image_tank_layout)
        # Tank log container
        dashboard_log_groupbox = QGroupBox('Logs')
        dashboard_log_groupbox.setFixedHeight(200)
        dashboard_log_groupbox.setFixedWidth(875)
        dashboard_log_layout = QVBoxLayout()
        # Tank log table
        log_table = QTableWidget(1, 8)
        log_table_header = log_table.horizontalHeader()
        log_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        log_table.setHorizontalHeaderLabels(["Date", "pH", "Sg", "NO3", "PO4", "KH", "CA", "MG"])
        log_table.setItem(0, 0, QTableWidgetItem("08 June 2023, 10:00 PM"))
        log_table.setItem(0, 1, QTableWidgetItem("8.3"))
        log_table.setItem(0, 2, QTableWidgetItem("1.025"))
        log_table.setItem(0, 3, QTableWidgetItem("2"))
        log_table.setItem(0, 4, QTableWidgetItem("0.03"))
        log_table.setItem(0, 5, QTableWidgetItem("8.5"))
        log_table.setItem(0, 6, QTableWidgetItem("400"))
        log_table.setItem(0, 7, QTableWidgetItem("1300"))
        dashboard_log_layout.addWidget(log_table)
        dashboard_log_groupbox.setLayout(dashboard_log_layout)
        # Tank operation container
        dashboard_operation_groupbox = QGroupBox('Menu')
        dashboard_operation_groupbox.setFixedWidth(875)
        dashboard_operation_groupbox.setFixedHeight(100)
        dashboard_operation_layout = QHBoxLayout()
        # Tank operation buttons
        dashboard_operation_layout.addWidget(self.sign_in_btn)
        dashboard_operation_layout.addWidget(self.sign_out_btn)
        dashboard_operation_layout.addWidget(self.upload_photo_btn)
        dashboard_operation_layout.addWidget(self.display_graphics_btn)
        dashboard_operation_layout.addWidget(self.upload_data_btn)
        dashboard_operation_groupbox.setLayout(dashboard_operation_layout)
        # layouts
        dashboard_layout.addWidget(dashboard_image_groupbox)
        dashboard_layout.addWidget(dashboard_log_groupbox)
        dashboard_layout.addWidget(dashboard_operation_groupbox)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(dashboard_layout)
        self.setCentralWidget(central_widget)
        self.show()

    def load_config(self):
        with open('config.yml', 'r') as config:
            self.config = yaml.load(config, Loader=yaml.SafeLoader)

    def init_firebase(self):
        self.firebase = pyrebase.initialize_app(self.config)

    def open_signin_dialog(self):
        signin_dialog = SignInDialog()
        if signin_dialog.exec():
            email = signin_dialog.input_email.text()
            password = signin_dialog.input_password.text()
            self.connect_firebase(email, password)

    def connect_firebase(self, email, password):
        if email != '' and password != '':
            auth = self.firebase.auth()
            try:
                self.user = auth.sign_in_with_email_and_password(email, password)
                self.sign_in_btn.setDisabled(True)
                # self.upload_photo_btn.setDisabled(False)
                # self.display_graphics_btn.setDisabled(False)
                # self.upload_data_btn.setDisabled(False)
                # self.sign_in_btn.setVisible(False)
                # self.sign_out_btn.setVisible(True)
            except requests.exceptions.HTTPError as error:
                msg = self.error_handler(error)
                self.display_error(msg)
        else:
            self.display_error('Password and email is empty')

    def error_handler(self, error):
        msg = json.loads(error.args[1])['error']['message']
        errors = {
            'INVALID_EMAIL' : 'Invalid email address',
            'INVALID_PASSWORD': 'Invalid password',
            'EMAIL_NOT_FOUND': 'Email not found'
        }
        return errors[msg]

    def display_error(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Close)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Retry)

        if msg_box.exec() == QMessageBox.StandardButton.Retry:
            self.open_signin_dialog()

    def disconnect_firebase(self):
        self.sign_out_btn.setVisible(False)
        self.sign_in_btn.setVisible(True)
        self.sign_in_btn.setDisabled(False)
        self.upload_photo_btn.setDisabled(True)
        self.display_graphics_btn.setDisabled(True)
        self.upload_data_btn.setDisabled(True)
        self.open_signin_dialog()

    def open_upload_data_dialog(self):
        upload_data_dialog = UploadDataDialog()
        if upload_data_dialog.exec():
            userid = self.user['localId']
            date = upload_data_dialog.date_input.text()
            ph = upload_data_dialog.input_sg.text()
            sg = upload_data_dialog.input_sg.text()
            no = upload_data_dialog.input_no.text()
            po = upload_data_dialog.input_po.text()
            kh = upload_data_dialog.input_kh.text()
            ca = upload_data_dialog.input_ca.text()
            mg = upload_data_dialog.input_mg.text()
            self.insert_data_aquarium(userid, date, ph, sg, no, po, kh, ca, mg)

    def insert_data_aquarium(self, userid, date, ph, sg, no, po, kh, ca, mg):
        db = self.firebase.database()
        print(self.user)
        try:
            db.child('users').child(userid).child('data').push({
                "date": date,
                "ph": ph,
                "sg": sg,
                "no": no,
                "po": po,
                "kh": kh,
                "ca": ca,
                "mg": mg
            })
        except Exception as e:
            print(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exec = AquariumLog()
    sys.exit(app.exec())
