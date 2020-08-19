import os
import sqlite3
import sys
import addproduct, addmember, sellings, style
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import Image
con = sqlite3.connect("products.db")
cur = con.cursor()

global productId, memberId


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Manager")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(130, 80, 1200, 600)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayProducts()
        self.displayMembers()
        self.getStatistics()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.tb.addSeparator()
        ###### TOOLBAR BUTTONS ###########
        ##### ADD PRODUCT #########
        self.addProduct = QAction(QIcon("icons/add.png"), "Add Product", self)
        self.tb.addAction(self.addProduct)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addSeparator()

        ######ADD  MEMBER #########
        self.addMember = QAction(QIcon('icons/users.png'),"Add Member", self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()

        ###### SELL PRODUCT #######
        self.sellProduct = QAction(QIcon("icons/sell.png"), "Sell Product", self)
        self.tb.addAction(self.sellProduct)
        self.sellProduct.triggered.connect(self.funcSellProducts)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1,"Products")
        self.tabs.addTab(self.tab2,"Members")
        self.tabs.addTab(self.tab3,"Statistics")


    def widgets(self):
        ##### TAB-1 WIDGETS #####
        ###### MAIN LEFT LATOUT WIDGETS #####

        self.productTable = QTableWidget()
        self.productTable.setColumnCount(6)
        self.productTable.setColumnHidden(0, True)
        self.productTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.productTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.productTable.setHorizontalHeaderItem(2, QTableWidgetItem("Manufacturer"))
        self.productTable.setHorizontalHeaderItem(3, QTableWidgetItem("Price"))
        self.productTable.setHorizontalHeaderItem(4, QTableWidgetItem("Quota"))
        self.productTable.setHorizontalHeaderItem(5, QTableWidgetItem("Availability"))
        self.productTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.productTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.productTable.doubleClicked.connect(self.selectedProduct)

        ####### RIGHT TOP LAYOUT WIDGETS ########
        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search for Product")
        self.searchButton = QPushButton("Search")
        self.searchButton.clicked.connect(self.searchProducts)
        self.searchButton.setStyleSheet(style.searchButtonStyle())

        ###### RIGHT MIDDLE WIDGETS ########
        self.allProducts = QRadioButton("All Products")
        self.availableProducts = QRadioButton("Available Products")
        self.notAvailableProducts = QRadioButton(" Not Available Products")
        self.listButton = QPushButton("List")
        self.listButton.clicked.connect(self.listProduct)
        self.listButton.setStyleSheet(style.listButtonStyle())

        ###### TAB-2 WIDGETS ########
        self.memberTable= QTableWidget()
        self.memberTable.setColumnCount(4)
        self.memberTable.setHorizontalHeaderItem(0, QTableWidgetItem("Member ID"))
        self.memberTable.setHorizontalHeaderItem(1, QTableWidgetItem("Member Name"))
        self.memberTable.setHorizontalHeaderItem(2, QTableWidgetItem("Member SurName"))
        self.memberTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.memberTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.memberTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.memberTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.memberTable.doubleClicked.connect(self.selectedMember)
        self.memberSearchText = QLabel("Search Members Bro")
        self.memberSearchEntry = QLineEdit()
        self.memberSearchButton = QPushButton("Search")
        self.memberSearchButton.clicked.connect(self.searchMembers)

        ####### TAB-3 WIDGETS #########
        self.totalProductLabel = QLabel()
        self.totalMemberLabel = QLabel()
        self.soldProductLabel = QLabel()
        self.totalAmountLabel = QLabel()


    def layouts(self):
        #### TAB1 LAYOUTS #######
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QVBoxLayout()
        self.mainRightLayout= QVBoxLayout()
        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()
        self.topGroupBox = QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox = QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())
        self.bottomGroupBox = QGroupBox()

        ###### ADD WIDGET ############
        #### MAIN LAYOUT WIDGET ######
        self.mainLeftLayout.addWidget(self.productTable)

        ###### RIGHT TOP LAYOUT ######
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self .rightTopLayout)

        ##### RIGHT MIDDLE LAYOUT ######
        self.rightMiddleLayout.addWidget(self.allProducts)
        self.rightMiddleLayout.addWidget(self.availableProducts)
        self.rightMiddleLayout.addWidget(self.notAvailableProducts)
        self.rightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)


        #### MAIN RIGHT LAYOUT  ADDING ######
        self.mainRightLayout.addWidget(self.topGroupBox,20)
        self.mainRightLayout.addWidget(self.middleGroupBox,20)
        self.mainRightLayout.addWidget(self.bottomGroupBox,60)
        ##### MAIN LAYOUT ADDING ##########
        self.mainLayout.addLayout(self.mainLeftLayout, 70)
        self.mainLayout.addLayout(self.mainRightLayout, 30)

        self.tab1.setLayout(self.mainLayout)
        ##### TAB-2 LAYOUTS #########
        self.memberMainLayout = QHBoxLayout()
        self.memberLeftLayout = QHBoxLayout()
        self.memberRightLayout = QHBoxLayout()
        self.memberRightGroupBox = QGroupBox("Search for Members")
        self.memberRightGroupBox.setContentsMargins(10, 10, 10, 400)
        self.memberRightLayout.addWidget(self.memberSearchText)
        self.memberRightLayout.addWidget(self.memberSearchEntry)
        self.memberRightLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightLayout)

        self.memberLeftLayout.addWidget(self.memberTable)


        self.memberMainLayout.addLayout(self.memberLeftLayout, 70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox, 30)
        self.tab2.setLayout(self.memberMainLayout)
        ######## TAB-3 LAYOUTS #########
        self.statisticsMainLayout = QVBoxLayout()
        self.statisticsLayout = QFormLayout()
        self.statisticsGroupBox = QGroupBox("Statistics")

        self.statisticsLayout.addRow(QLabel("Total Products: "),self.totalProductLabel)
        self.statisticsLayout.addRow(QLabel("Total Members: "),self.totalMemberLabel)
        self.statisticsLayout.addRow(QLabel("Sold Products: "),self.soldProductLabel)
        self.statisticsLayout.addRow(QLabel("Total Amount: "),self.totalAmountLabel)

        self.statisticsGroupBox.setLayout(self.statisticsLayout)
        self.statisticsGroupBox.setFont(QFont("Arial",16))
        self.statisticsMainLayout.addWidget(self.statisticsGroupBox)
        self.tab3.setLayout(self.statisticsMainLayout)
        self.tabs.blockSignals(False)


    def funcAddProduct(self):
        self.newProduct = addproduct.AddProduct()

    def funcAddMember(self):
        self.newMember = addmember.AddMember()

    def displayProducts(self):
        self.productTable.setFont(QFont("Times, 12"))
        for i in reversed(range(self.productTable.rowCount())):
            self.productTable.removeRow(i)

        query = cur.execute("SELECT product_id, product_name, product_manufacturer, product_price, product_quota, product_availability FROM products")

        for row_data in query:
            row_number = self.productTable.rowCount()
            self.productTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.productTable.setItem(row_number,column_number, QTableWidgetItem(str(data)))

        self.productTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displayMembers(self):
        self.memberTable.setFont(QFont("Times,12"))
        for i in reversed(range(self.memberTable.rowCount())):
            self.memberTable.removeRow(i)

        members = cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number = self.memberTable.rowCount()
            self.memberTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.memberTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        self.memberTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedProduct(self):
        global productId
        listProduct = []
        for i in range(0,6):
            listProduct.append(self.productTable.item(self.productTable.currentRow(),i).text())

        productId = listProduct[0]
        self.display = DisplayProduct()
        self.display.show()


    def selectedMember(self):
        global memberId
        listMember= []

        for i in range(0,4):
            listMember.append(self.memberTable.item(self.memberTable.currentRow(),i).text())
            memberId = listMember[0]
            self.displayMember = DisplayMember()
            self.displayMember.show()

    def searchProducts(self):
        value = self.searchEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning!","Search query cannot be Empty!")
        else:
            self.searchEntry.setText("")

            query = "SELECT product_id,product_name,product_manufacturer,product_price,product_quota,product_availability FROM products WHERE product_name LIKE ? or product_manufacturer LIKE ?"
            results = cur.execute(query,('%'+ value + '%','%' + value + '%')).fetchall()
            print(results)
            if results == []:
                QMessageBox.information(self, "Warning!","There is no Product/manufacturer with this name")
            else:
                for i in reversed(range(self.productTable.rowCount())):
                    self.productTable.removeRow(i)

                for row_data in results:
                    row_number = self.productTable.rowCount()
                    self.productTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.productTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))


    def searchMembers(self):
        value = self.memberSearchEntry.text()
        if value == "":
            QMessageBox.information(self,"Warning", "Search cannot be Empty")
        else:
            self.memberSearchEntry.setText("")
            query = "SELECT * FROM members WHERE member_name LIKE ? or member_surname LIKE ? or member_phone LIKE ?"
            results = cur.execute(query,('%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
            print(results)

            if results == []:
                QMessageBox.information(self, 'Warning!', "There is no such member")
            else:

                for i in reversed(range(self.memberTable.rowCount())):
                    self.memberTable.removeRow(i)

                for row_data in results:
                    row_number = self.memberTable.rowCount()
                    self.memberTable.insertRow(row_number)
                    for column_number,data in enumerate(row_data):
                        self.memberTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))


    def listProduct(self):
        if self.allProducts.isChecked() == True:
            self.displayProducts()
        elif self.availableProducts.isChecked():
            query = ("SELECT product_id, product_name, product_manufacturer, product_price, product_quota,"
            "product_availability FROM products WHERE product_availability='Available' ")
            products = cur.execute(query).fetchall()
            print(products)

            for i in reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)

            for row_data in products:
                row_number = self.productTable.rowCount()
                self.productTable.insertRow(row_number)

                for column_number,data in enumerate(row_data):
                    self.productTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

        elif self.notAvailableProducts.isChecked():
            query = ("SELECT product_id, product_name, product_manufacturer, product_price, product_quota,"
                     "product_availability FROM products WHERE product_availability='UnAvailable' ")
            products = cur.execute(query).fetchall()
            print(products)

            for i in reversed(range(self.productTable.rowCount())):
                self.productTable.removeRow(i)

            for row_data in products:
                row_number = self.productTable.rowCount()
                self.productTable.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.productTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def funcSellProducts(self):
        self.sell = sellings.SellProducts()

    def getStatistics(self):
        countProducts = cur.execute("SELECT count(product_id) FROM products").fetchall()
        countMembers = cur.execute("SELECT count(member_id) FROM members").fetchall()
        soldProducts = cur.execute("SELECT SUM(selling_quantity) FROM sellings").fetchall()
        totalAmount = cur.execute("SELECT SUM(selling_amount) FROM sellings").fetchall()
        totalAmount = totalAmount[0][0]
        soldProducts = soldProducts[0][0]
        countProducts = countProducts[0][0]
        countMembers= countMembers[0][0]
        self.totalProductLabel.setText(str(countProducts))
        self.totalMemberLabel.setText(str(countMembers))
        self.totalProductLabel.setText(str(soldProducts))
        self.totalAmountLabel.setText(str(totalAmount)+ " $")

    def tabChanged(self):
        self.getStatistics()
        self.displayProducts()
        self.displayMembers()

class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(400, 100, 300, 500)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()

    def memberDetails(self):
        global memberId

        query = "SELECT * FROM members WHERE member_id =?"
        member = cur.execute(query,(memberId,)).fetchone()

        self.memberName = member[1]
        self.memberSurName = member[2]
        self.memberPhone = member[3]

    def widgets(self):
        ####### TOP LAYOUT WIDGETS #########
        self.memberImg = QLabel()
        self.img = QPixmap("icons/members.png")
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display Member")
        self.titleText.setAlignment(Qt.AlignCenter)
        ####### BOTTOM LAYOUT WIDGETS #########
        self.nameEntry =QLineEdit()
        self.nameEntry.setText(self.memberName)
        self.surNameEntry = QLineEdit()
        self.surNameEntry.setText(self.memberSurName)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.memberPhone)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateMember)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteMember)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.memberTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.memberBottomFrame())

        ####### ADD WIDGETS #########
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("SurName: "), self.surNameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.updateBtn)
        self.bottomLayout.addRow(QLabel(""), self.deleteBtn)

        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def deleteMember(self):
        global memberId
        mbox = QMessageBox.question(self, "WARING!", "Are you sure you wanna delete This Member", QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                query = "DELETE FROM members WHERE member_id =?"
                cur.execute(query,(memberId,))
                con.commit()
                QMessageBox.information(self, "Information", "Member Deleted")

            except:
                QMessageBox.information(self, "Warning", "Member NOT Deleted")

        # else:
        #     QMessageBox.information(self, "Information", "Fields cannot be empty")

    def updateMember(self):
        global memberId
        name = self.nameEntry.text()
        surname = self.surNameEntry.text()
        phone = self.phoneEntry.text()

        if name and surname and phone !="":
            try:
                query = "UPDATE members set member_name=?, member_surname=?, member_phone=? WHERE member_id=?"
                cur.execute(query,(name, surname, phone, memberId))
                con.commit()
                QMessageBox.information(self,"Info","Member Updated Successfully")
                self.close()

            except:
                QMessageBox.information(self,"WARNING!","Member NOT Updated ")
        else:
            QMessageBox.information(self, "WARNING!", "Fields cannot be empty Sir")


class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Products Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(400, 100, 300, 500)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()

    def productDetails(self):
        global productId
        query = ("SELECT * FROM products WHERE product_id=?")
        product = cur.execute(query,(productId,)).fetchone() #Single ITem tuple=(i,)
        self.productName = product[1]
        self.productManufacturer = product[2]
        self.productPrice = product[3]
        self.productQuota = product[4]
        self.productImg = product[5]
        self.productStatus = product[6]

    def widgets(self):
        ### TOP LAYOUT WIDGETS ####
        self.product_Img = QLabel()
        self.img = QPixmap("images/{}".format(self.productImg))
        self.product_Img.setPixmap(self.img)
        self.product_Img.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Update Product")
        self.titleText.setAlignment(Qt.AlignCenter)


        ###### BOTTOM LAYOUT WIDGETS ######
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.productName)
        self.manufacturerEntry = QLineEdit()
        self.manufacturerEntry.setText(self.productManufacturer)
        self.priceEntry = QLineEdit()
        self.priceEntry.setText(str(self.productPrice))
        self.quotaEntry = QLineEdit()
        self.quotaEntry.setText(str(self.productQuota))
        self.availabilityCombo =QComboBox()
        self.availabilityCombo.addItems(['Available','UnAvailable'])
        self.uploadBtn = QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteProduct)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateProduct)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame = QFrame()
        self.bottomFrame.setStyleSheet(style.productBottomFrame())
        ###### ADD WIDGETS #######
        ###### TOP WIDGETS LAYOUT ADD ######
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.product_Img)
        self.topFrame.setLayout(self.topLayout)

        ###### BOTTOM WIDGETS ADD ########
        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Manufacturer: "),self.manufacturerEntry)
        self.bottomLayout.addRow(QLabel("Price: "),self.priceEntry)
        self.bottomLayout.addRow(QLabel("Quota: "),self.quotaEntry)
        self.bottomLayout.addRow(QLabel("Status: "),self.availabilityCombo)
        self.bottomLayout.addRow(QLabel("Image: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)


        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global productId
        size =(256, 256)
        self.filename,ok = QFileDialog.getOpenFileName(self,"upload Image","","Image FIles(*.jpg *.png")
        if ok:
            self.productImg = os.path.basename(self.filename)
            img = Image.open(self.filename)
            img= img.resize(size)
            img.save("images/{0}".format(self.productImg))


    def updateProduct(self):
        name = self.nameEntry.text()
        manufacturer = self.manufacturerEntry.text()
        price = int(self.priceEntry.text())
        quota = int(self.quotaEntry.text())
        status = self.availabilityCombo.currentText()
        defaultImg = self.productImg

        if name and manufacturer and price and quota !="":
            try:
                query = "UPDATE products set product_name=?, product_manufacturer=?, product_price=?, product_quota=?, product_img=?, product_availability=? WHERE product_id=?"
                cur.execute(query,(name, manufacturer, price, quota, defaultImg, status,productId))
                con.commit()
                QMessageBox.information(self, "Info","Product Updated!")



            except:
                QMessageBox.information(self, "WARNING!","Product NOT Updated!")
        else:
            QMessageBox.information(self, "WARNING!", "Fields Cannot Be Empty!")

    def deleteProduct(self):
        global productId
        mbox= QMessageBox.question(self,"WARING!","Are you sure you wanna delete",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM products WHERE product_id =?",(productId,))
                con.commit()
                QMessageBox.information(self,"Information","Product Deleted")
                self.close()

            except:
                QMessageBox.information(self,"Warning","Product NOT Deleted")

        else:
            QMessageBox.information(self, "Information", "Fields cannot be empty")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
