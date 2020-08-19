import os
import sqlite3

con = sqlite3.connect("products.db")
cur = con.cursor()
import sys
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PIL import Image

defaultImg ="images/store.png"
class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(350, 150, 250, 450)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def widgets(self):
        ###### WIDGETS TOP LAYOUT ####

        self.addProductImg = QLabel()
        self.img = QPixmap("icons/addproduct.png")
        self.addProductImg.setPixmap(self.img)
        self.titleText = QLabel("Add Product")

        ####### WIDGETS BOTTOM  LAYOUT ####
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Name of Product")
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setPlaceholderText("Enter name of Manufacturer")
        self.priceEntry =QLineEdit()
        self.priceEntry.setPlaceholderText("Enter Price of Product")
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setPlaceholderText("Enter Quota of Product")
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addProduct)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ####### TOP WIDGETS ########
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)
        ##### WIDGET OF BOTTOM/FORM LAYOUT ####
        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "), self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price:  "), self.priceEntry)
        self.bottomLayout.addRow(QLabel("Quota: "), self.quotaEntry)
        self.bottomLayout.addRow(QLabel("Upload: "), self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)


    def UI(self):
        self.widgets()
        self.layouts()

    def uploadImg(self):
        global defaultImg
        size =(256, 256)
        self.filename,ok =QFileDialog.getOpenFileName(self, "Upload Image","","Image Files(*.jpg *.png")
        if ok:
            defaultImg = os.path.basename(self.filename)
            print(defaultImg)
            img = Image.open(self.filename)
            img = img.resize(size)
            img.save("images/{0}".format(defaultImg))

    def addProduct(self):
        global defaultImg
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = self.priceEntry.text()
        quota = self.quotaEntry.text()

        if (name and manufacturer and price and quota != "") :

            try:
                query = "INSERT INTO 'products' (product_name,product_manufacturer,product_price,product_quota,product_img) VALUES(?,?,?,?,?)"
                cur.execute(query, (name, manufacturer, price, quota, defaultImg))
                con.commit()
                QMessageBox.information(self, "Info", "Product Added Successfully")
            except:
                QMessageBox.information(self, "Warning","Product Not Added!")

        else:
            QMessageBox.information(self, "Warning!","Fields Cannot be Empty")