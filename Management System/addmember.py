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
class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(350, 150, 250, 450)
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ##### TOP WIDGETS #######
        self.addMemberImg = QLabel()
        self.img = QPixmap("icons/addmember.png")
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add Member")
        self.titleText.setAlignment(Qt.AlignCenter)

        ####### BOTTOM WIDGETS ########
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Namme of Member")
        self.surnameEntry = QLineEdit()
        self.surnameEntry.setPlaceholderText("Enter Namme of Member")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Namme of Member")
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addMember)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        ##### ADD WIDGETS #####
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "), self.nameEntry)
        self.bottomLayout.addRow(QLabel("SurName: "), self.surnameEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def addMember(self):
        name = self.nameEntry.text()
        surname = self.surnameEntry.text()
        phone = self.phoneEntry.text()

        if(name and surname and phone !=""):
            try:
                query = "INSERT INTO 'members' (member_name, member_surname, member_phone) VALUES (?,?,?) "
                cur.execute(query,(name, surname, phone))
                con.commit()
                QMessageBox.information(self,"Info","Member Added Successfully")
                self.nameEntry.setText("")
                self.surnameEntry.setText("")
                self.phoneEntry.setText("")

            except:
                QMessageBox.information(self,"Warning!","Member Not Added")

        else:
            QMessageBox.information(self, "Warning!", "Fields Cannot be empty!")


def main():
    App = QApplication(sys.argv)
    window = AddMember()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
