from PyQt6.QtWidgets import (
    QDialog, QLabel, QGroupBox, QDialogButtonBox, QLineEdit, QFormLayout, QVBoxLayout, QDateTimeEdit, QGridLayout )
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QDoubleValidator
import pyqtgraph as pg
import os

class SignInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Log In")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setFixedWidth(300)
        self.setFixedHeight(165)

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
        self.setFixedWidth(300)
        self.setFixedHeight(350)

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

class GraphDialog(QDialog):

    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Aquarium Graph')
        self.setFixedWidth(1800)

        # Plot
        self.plot_ph = pg.PlotWidget()
        self.plot_sg = pg.PlotWidget()
        self.plot_no = pg.PlotWidget()
        self.plot_po = pg.PlotWidget()
        self.plot_kh = pg.PlotWidget()
        self.plot_ca = pg.PlotWidget()
        self.plot_mg = pg.PlotWidget()

        # Data
        self.data = data

        # Init dialog
        self.init_dialog()


    def init_dialog(self):

        # Map data
        index = []
        num = 0
        date = []
        ph = []
        sg = []
        no = []
        po = []
        kh = []
        ca = []
        mg = []
        if self.data:
            for key, value in self.data.items():
                date.append(value['date'][:8])
                ph.append(float(value['ph']))
                sg.append(float(value['sg']))
                no.append(float(value['no']))
                po.append(float(value['po']))
                kh.append(float(value['kh']))
                ca.append(float(value['ca']))
                mg.append(float(value['mg']))
                num += 1
                index.append(str(num))

        # X labels
        x_labels = index

        # pH Groupbox
        ph_group = QGroupBox('PH')
        ph_layout = QVBoxLayout()

        # pH plot
        plot_ph = self.plot_ph
        plot_ph.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_ph.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_ph.plot(ph, pen='g', symbol='x', symbolPen='g', symbolBrush=0.2, name='PH')
        ph_top_val = 8.4
        ph_bottom_val = 8.1
        ph_top_line = pg.InfiniteLine(pos=ph_top_val, angle=0, movable=False, pen='g')
        ph_bottom_line = pg.InfiniteLine(pos=ph_bottom_val, angle=0, movable=False, pen='g')
        plot_ph.addItem(ph_top_line)
        plot_ph.addItem(ph_bottom_line)

        # Plot widget placement
        ph_layout.addWidget(plot_ph)
        ph_group.setLayout(ph_layout)

        # sg Groupbox
        sg_group = QGroupBox('SG')
        sg_layout = QVBoxLayout()

        # sg plot
        plot_sg = self.plot_sg
        plot_sg.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_sg.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_sg.plot(sg, pen='r', symbol='x', symbolPen='r', symbolBrush=0.2, name='SG')
        sg_top_val = 1.026
        sg_bottom_val = 1.024
        sg_top_line = pg.InfiniteLine(pos=sg_top_val, angle=0, movable=False, pen='r')
        sg_bottom_line = pg.InfiniteLine(pos=sg_bottom_val, angle=0, movable=False, pen='r')
        plot_sg.addItem(sg_top_line)
        plot_sg.addItem(sg_bottom_line)

        # Plot widget placement
        sg_layout.addWidget(plot_sg)
        sg_group.setLayout(sg_layout)

        # no Groupbox
        no_group = QGroupBox('NO3 in ppm')
        no_layout = QVBoxLayout()

        # no plot
        plot_no = self.plot_no
        plot_no.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_no.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_no.plot(no, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='NO3')
        no_top_val = 10
        no_bottom_val = 0
        no_top_line = pg.InfiniteLine(pos=no_top_val, angle=0, movable=False, pen='b')
        no_bottom_line = pg.InfiniteLine(pos=no_bottom_val, angle=0, movable=False, pen='b')
        plot_no.addItem(no_top_line)
        plot_no.addItem(no_bottom_line)

        # Plot widget placement
        no_layout.addWidget(plot_no)
        no_group.setLayout(no_layout)

        # po Groupbox
        po_group = QGroupBox('PO4 in ppm')
        po_layout = QVBoxLayout()

        # no plot
        plot_po = self.plot_po
        plot_po.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_po.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_po.plot(po, pen='y', symbol='x', symbolPen='y', symbolBrush=0.2, name='PO4')
        po_top_val = 0
        po_bottom_val = 0.03
        po_top_line = pg.InfiniteLine(pos=po_top_val, angle=0, movable=False, pen='y')
        po_bottom_line = pg.InfiniteLine(pos=po_bottom_val, angle=0, movable=False, pen='y')
        plot_po.addItem(po_top_line)
        plot_po.addItem(po_bottom_line)

        # Plot widget placement
        po_layout.addWidget(plot_po)
        po_group.setLayout(po_layout)

        # kh Groupbox
        kh_group = QGroupBox('KH in dKH')
        kh_layout = QVBoxLayout()

        # no plot
        plot_kh = self.plot_kh
        plot_kh.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_kh.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_kh.plot(kh, pen='c', symbol='x', symbolPen='c', symbolBrush=0.2, name='KH')
        kh_top_val = 12
        kh_bottom_val = 8
        kh_top_line = pg.InfiniteLine(pos=kh_top_val, angle=0, movable=False, pen='c')
        kh_bottom_line = pg.InfiniteLine(pos=kh_bottom_val, angle=0, movable=False, pen='c')
        plot_kh.addItem(kh_top_line)
        plot_kh.addItem(kh_bottom_line)

        # Plot widget placement
        kh_layout.addWidget(plot_kh)
        kh_group.setLayout(kh_layout)

        # ca Groupbox
        ca_group = QGroupBox('CA in ppm')
        ca_layout = QVBoxLayout()

        # ca plot
        plot_ca = self.plot_ca
        plot_ca.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_ca.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_ca.plot(ca, pen='w', symbol='x', symbolPen='w', symbolBrush=0.2, name='CA')
        ca_top_val = 450
        ca_bottom_val = 380
        ca_top_line = pg.InfiniteLine(pos=ca_top_val, angle=0, movable=False, pen='w')
        ca_bottom_line = pg.InfiniteLine(pos=ca_bottom_val, angle=0, movable=False, pen='w')
        plot_ca.addItem(ca_top_line)
        plot_ca.addItem(ca_bottom_line)

        # Plot widget placement
        ca_layout.addWidget(plot_ca)
        ca_group.setLayout(ca_layout)

        # mg Groupbox
        mg_group = QGroupBox('MG in ppm')
        mg_layout = QVBoxLayout()

        # mg plot
        plot_mg = self.plot_mg
        plot_mg.getPlotItem().getAxis('bottom').setStyle(tickTextOffset=15)
        plot_mg.getPlotItem().getAxis('bottom').setTicks([list(enumerate(x_labels))])
        plot_mg.plot(mg, pen='m', symbol='x', symbolPen='m', symbolBrush=0.2, name='MG')
        mg_top_val = 1400
        mg_bottom_val = 1200
        mg_top_line = pg.InfiniteLine(pos=mg_top_val, angle=0, movable=False, pen='m')
        mg_bottom_line = pg.InfiniteLine(pos=mg_bottom_val, angle=0, movable=False, pen='m')
        plot_mg.addItem(mg_top_line)
        plot_mg.addItem(mg_bottom_line)

        # Plot widget placement
        mg_layout.addWidget(plot_mg)
        mg_group.setLayout(mg_layout)

        # Main layout
        main_layout = QGridLayout()
        main_layout.addWidget(ph_group, 0, 0)
        main_layout.addWidget(sg_group, 0, 1)
        main_layout.addWidget(no_group, 0, 2)
        main_layout.addWidget(po_group, 0, 3)
        main_layout.addWidget(kh_group, 1, 0)
        main_layout.addWidget(ca_group, 1, 1)
        main_layout.addWidget(mg_group, 1, 2)
        self.setLayout(main_layout)
        print(self.data)


