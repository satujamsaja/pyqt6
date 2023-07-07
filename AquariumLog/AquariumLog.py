import sys

import requests.exceptions
import yaml
import json
import os
import time
import pyrebase
from urllib.parse import quote
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QTableWidget , QTableWidgetItem,
    QHeaderView, QPushButton, QDialogButtonBox, QMessageBox, QDateTimeEdit, QAbstractItemView, QFileDialog  )

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
        self.sign_out_btn.setVisible(False)
        self.sign_out_btn.clicked.connect(self.disconnect_firebase)
        self.upload_photo_btn = QPushButton('Upload Photos')
        self.upload_photo_btn.setFixedHeight(60)
        self.upload_photo_btn.clicked.connect(self.open_upload_photo_dialog)
        self.upload_photo_btn.setDisabled(True)
        self.display_graphics_btn = QPushButton('Display Graphics')
        self.display_graphics_btn.setFixedHeight(60)
        self.display_graphics_btn.setDisabled(True)
        self.upload_data_btn = QPushButton('Upload Data')
        self.upload_data_btn.setFixedHeight(60)
        self.upload_data_btn.setDisabled(True)
        self.upload_data_btn.clicked.connect(self.open_upload_data_dialog)
        # Init datatable
        self.log_table = QTableWidget(1, 8)
        self.log_table_header = self.log_table.horizontalHeader()
        self.log_table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.log_table.setHorizontalHeaderLabels(["Date", "pH", "Sg", "NO3", "PO4", "KH", "CA", "MG"])
        # Labels
        self.firebase_label = QLabel('Firebase: Disconnected')
        self.upload_label = QLabel('Upload: No file uploaded')
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
        # Add table to layout
        dashboard_log_layout.addWidget(self.log_table)
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
        # Dashboard status
        dashboard_status_groupbox = QGroupBox('Status')
        dashboard_status_groupbox.setFixedHeight(75)
        dashboard_status_layout = QHBoxLayout()
        dashboard_status_layout.addWidget(self.firebase_label)
        dashboard_status_layout.addWidget(self.upload_label)
        dashboard_status_groupbox.setLayout(dashboard_status_layout)
        # layouts
        dashboard_layout.addWidget(dashboard_image_groupbox)
        dashboard_layout.addWidget(dashboard_log_groupbox)
        dashboard_layout.addWidget(dashboard_operation_groupbox)
        dashboard_layout.addWidget(dashboard_status_groupbox)

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
                self.upload_photo_btn.setDisabled(False)
                self.display_graphics_btn.setDisabled(False)
                self.upload_data_btn.setDisabled(False)
                self.sign_in_btn.setVisible(False)
                self.sign_out_btn.setVisible(True)
                self.firebase_label.setText('Firebase: Connected')
                self.load_data_aquarium()
                self.load_photo_aquarium()
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

    def display_insert_message(self, msg):
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Close)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Yes)

        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.open_upload_data_dialog()

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
            self.load_data_aquarium(userid)
            self.display_insert_message('Insert data success. Enter another data?')
        except Exception as e:
            print(e)

    def load_data_aquarium(self):
        db = self.firebase.database()
        userid = self.user['localId']
        try:
            data = db.child('users').child(userid).child('data').get()
            data_value = data.val()
            self.log_table.setRowCount(len(data_value))
            row = 0
            for log in data_value:
                log_data = data_value[log]
                self.log_table.setItem(row, 0, QTableWidgetItem(log_data['date']))
                self.log_table.setItem(row, 1, QTableWidgetItem(log_data['ph']))
                self.log_table.setItem(row, 2, QTableWidgetItem(log_data['sg']))
                self.log_table.setItem(row, 3, QTableWidgetItem(log_data['no']))
                self.log_table.setItem(row, 4, QTableWidgetItem(log_data['po']))
                self.log_table.setItem(row, 5, QTableWidgetItem(log_data['kh']))
                self.log_table.setItem(row, 6, QTableWidgetItem(log_data['ca']))
                self.log_table.setItem(row, 7, QTableWidgetItem(log_data['mg']))
                row += 1

        except Exception as e:
            print(e)

    def open_upload_photo_dialog(self):
        paths, _ = QFileDialog.getOpenFileNames(self, 'Select image(s)', '', 'Images (*.png *.jpg *.jpeg)')
        files = []
        storage = self.firebase.storage()
        userid = self.user['localId']
        for path in paths:
            if path != '':
                filename = os.path.basename(path)
                files.append(filename)
                file, ext = os.path.splitext(filename)
                timestamp = int(time.time())
                storage.child('users').child(userid).child(file +  '-' + str(timestamp) + ext).put(path)

        self.upload_label.setText('Upload: ' + ','.join(files))

    def load_photo_aquarium(self):
        storage = self.firebase.storage()
        userid = self.user['localId']
        photos = storage.child('users').child(userid).list_files()
        for photo in photos:
            path_encode = quote(photo.name)
            print(path_encode)
            url = self.config['storageBaseUrl'] + self.config['storageBucket'] + '/o/' + path_encode + '?alt=media'
            print(url)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exec = AquariumLog()
    sys.exit(app.exec())
