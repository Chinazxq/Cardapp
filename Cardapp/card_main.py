
import sys
import socket
import pymongo
from cards import Ui_MainWindow
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

class Cardapp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_card)
        self.ui.pushButton_2.clicked.connect(self.display_card)
        self.ui.deleteCard.clicked.connect(self.delete_card)
        self.ui.pushButton_3.clicked.connect(self.change_card)
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient["cards"]
        self.ui.tableWidget.setRowCount(40)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setHorizontalHeaderLabels(["姓名","年龄","电话"])
        self.display_card()
        #点击选中行
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableWidget.itemClicked.connect(self.select_card)

    def change_card(self):
        """"修改名片"""
        mycol = self.mydb['info']
        name_1 = self.ui.textEdit.toPlainText()
        if name_1 == "":
            QMessageBox.information(self,"","错误")
            return
        age_1 = self.ui.textEdit_2.toPlainText()
        phone_1 = self.ui.textEdit_3.toPlainText()
        myquery = {"name":name_1}
        newvalues = {"$set":{"age":age_1,"phone":phone_1}}
        mycol.update_one(myquery,newvalues)
        self.ui.tableWidget.clearContents()
        self.display_card()
        self.clear_text()
        QMessageBox.information(self,"","修改成功！")

    def delete_card(self):
        """删除名片"""
        #print("delete")
        name_1 = self.ui.textEdit.toPlainText()
        mycol = self.mydb['info']
        myquery = {"name":name_1}
        mycol.delete_one(myquery)
        self.ui.tableWidget.clearContents()
        self.display_card()
        self.clear_text()

    def select_card(self):
        """选中行的内容显示"""
        items = self.ui.tableWidget.selectedItems()
        #print(items[0].text())
        self.ui.textEdit.setText(items[0].text())
        self.ui.textEdit_2.setText(items[1].text())
        self.ui.textEdit_3.setText(items[2].text())

    def add_card(self):
        """新增名片"""
        mycol = self.mydb['info']
        name_1 = self.ui.textEdit.toPlainText()
        myquery = {"name":name_1}
        mydoc = mycol.find(myquery)
        #print(mydoc)
        if mydoc.count() != 0:
            #print("%s已存在！" % name_1)
            QMessageBox.information(self,"新增失败","已存在！")
            return
        age_1 = self.ui.textEdit_2.toPlainText()
        phone_1 = self.ui.textEdit_3.toPlainText()
        card_dict = {
            "name":name_1,
            "age":age_1,
            "phone":phone_1}
        mycol.insert_one(card_dict)
        self.clear_text()
        #将新增的名片显示在tablewidget中
        i = mycol.count()
        newItem_1 = QTableWidgetItem(card_dict["name"])
        self.ui.tableWidget.setItem(i-1,0,newItem_1)
        newItem_2 = QTableWidgetItem(card_dict["age"])
        self.ui.tableWidget.setItem(i-1,1,newItem_2)
        newItem_3 = QTableWidgetItem(card_dict["phone"])
        self.ui.tableWidget.setItem(i-1,2,newItem_3)

    def clear_text(self):
        """清空输入框"""
        self.ui.textEdit.clear()
        self.ui.textEdit_2.clear()
        self.ui.textEdit_3.clear()

    def display_card(self):
        """显示"""
        mycol = self.mydb['info']
        i = 0
        for card_dict in mycol.find():
            #print("%s" % card_dict["name"])
            newItem_1 = QTableWidgetItem(card_dict["name"])
            self.ui.tableWidget.setItem(i,0,newItem_1)
            newItem_2 = QTableWidgetItem(card_dict["age"])
            self.ui.tableWidget.setItem(i,1,newItem_2)
            newItem_3 = QTableWidgetItem(card_dict["phone"])
            self.ui.tableWidget.setItem(i,2,newItem_3)
            i += 1



if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Cardapp()
    a.show()
    sys.exit(app.exec_())