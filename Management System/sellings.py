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
import style

defaultImg ="images/store.png"
class SellProducts(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(350, 150, 250, 450)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()
    def widgets(self):
        ##### TOP WIDGETS #####

        self.sellProductImg = QLabel()
        self.img =QPixmap("icons/shop.png")
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Products")
        self.titleText.setAlignment(Qt.AlignCenter)

        ######## BOTTOM WIDGETS ########
        self.productCombo = QComboBox()
        self.productCombo.currentIndexChanged.connect(self.changeComboValue)
        self.memberCombo = QComboBox()
        self.quantityCombo = QComboBox()
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.sellProduct)


        query1 = ("SELECT * FROM products WHERE product_availability= ?")
        products = cur.execute(query1,('Available',)).fetchall()
        print(products)
        query2 =("SELECT member_id, member_name FROM members")
        members = cur.execute(query2).fetchall()
        quantity = products[0][4]

        for product in products:
            self.productCombo.addItem(product[1],product[0])

        for member in members:
            self.memberCombo.addItem(member[1],member[0])

        for i in range(1,quantity+1):
            self.quantityCombo.addItem(str(i))

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.sellProductTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.sellProductBottomFrame())

        ######## Add Widgets ########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Product: "), self.productCombo)
        self.bottomLayout.addRow(QLabel("Member: "), self.memberCombo)
        self.bottomLayout.addRow(QLabel("quantity: "), self.quantityCombo)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def changeComboValue(self):
        self.quantityCombo.clear()
        product_id = self.productCombo.currentData()
        query = "SELECT product_quota FROM products WHERE product_id =?"
        quota = cur.execute(query,(product_id,)).fetchone()


        for i in range(1,quota[0]+1):
            self.quantityCombo.addItem(str(i))

    def sellProduct(self):
        global productName, productId, memberName, memberId, quantity
        productName = self.productCombo.currentText()
        productId = self.productCombo.currentData()
        memberName = self.memberCombo.currentText()
        memberId = self.memberCombo.currentData()
        quantity = int(self.quantityCombo.currentText())

        self.confirm = ConfirmWindow()
        self.close()

class ConfirmWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sell Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(350, 150, 250, 450)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### TOP WIDGETS #####

        self.sellProductImg = QLabel()
        self.img = QPixmap("icons/shop.png")
        self.sellProductImg.setPixmap(self.img)
        self.sellProductImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Sell Products")
        self.titleText.setAlignment(Qt.AlignCenter)
        ######BOTTOM WIDGETS ##########
        global productName, productId, memberName, memberId, quantity
        priceQuery = "SELECT product_price FROM products WHERE product_id=?"
        price = cur.execute(priceQuery,(productId,)).fetchone()
        print(price)
        self.amount = int(quantity) * int(price[0])
        self.productName = QLabel()
        self.productName.setText(productName)
        self.memberName = QLabel()
        self.memberName.setText(memberName)
        self.amountLable = QLabel()
        self.amountLable.setText(str(price[0])+ "x"+ str(quantity) +"=" + str(self.amount))
        self.confirmBtn = QPushButton("Confirm")
        self.confirmBtn.clicked.connect(self.confirm)


    def layouts(self):

        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.confirmProductTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.confirmProductBottomFrame())


        ######## Add Widgets ########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.sellProductImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Product: "), self.productName)
        self.bottomLayout.addRow(QLabel("Member: "), self.memberName)
        self.bottomLayout.addRow(QLabel("Amount: "), self.amountLable)
        self.bottomLayout.addRow(QLabel(""), self.confirmBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)


    def confirm(self):
        global productName, productId, memberName, memberId, quantity

        try:
            sellQuery = ("INSERT INTO 'sellings' (selling_product_id,selling_member_id,selling_quantity,selling_amount) VALUES (?,?,?,?)")
            cur.execute(sellQuery,(productId,memberId,quantity,self.amount))
            quotaQuery = "SELECT product_quota FROM products WHERE product_id = ?"
            self.quota = cur.execute(quotaQuery,(productId,)).fetchone()
            print(self.quota)
            con.commit()

            if quantity == self.quota[0]:
                updateQuotaQuery = "UPDATE products set product_quota=?, product_availability=? WHERE product_id =?"
                cur.execute(updateQuotaQuery,(0,'UnAvailable',productId))
                con.commit()

            else:
                newQuota = (self.quota[0] - quantity)
                updateQuotaQuery = "UPDATE products set product_quota =? WHERE product_id =?"
                cur.execute(updateQuotaQuery,(newQuota,productId))
                con.commit()

            QMessageBox.information(self,"Info","Successful")

        except:
            QMessageBox.information(self,"Info","Something Went Wrong")
