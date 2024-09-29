import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sqlite3
from datetime import *


#sql_commands_runner.execute()
#sql_commands_runner.execute("SELECT * FROM StockTable")


class Stationery_Pantry(QWidget):
    def __init__(self, parent=None):
        
        QWidget.__init__(self, parent)
        
        self.setGeometry(250, 150, 400, 400)                       # setting the window style and title
        self.setWindowTitle('Stationery Pantry Tuckshop')
        self.setPalette(QPalette(QColor('cyan')))        
        
        self.POS_Tables = sqlite3.connect('StockTable.db')              # connecting the database to python for access
        self.sql_commands_runner = self.POS_Tables.cursor()           
        
        #for row in self.data:
            #print(row[0])
        
        self.pixmap = QPixmap('StationeryR')              # sets picture
        self.pic_label = QLabel()
        self.pic_label.setPixmap(self.pixmap)
        
        self.enter_item = QLineEdit()                  # creating the line edit to enter number of items one wants               
        
        self.combo_items = QComboBox()                 # creating the dropdown list to show all the items sold
        self.combo_items.addItem('Pen')
        self.combo_items.addItem('Pencil')
        self.combo_items.addItem('Eraser')
        self.combo_items.addItem('Pencil Case')
        self.combo_items.addItem('Sharpner')
        self.combo_items.addItem('Calculator')
        self.combo_items.addItem('Ruler')
        self.combo_items.addItem('Highlighters')
        self.combo_items.addItem('Mini Whiteboard')
        self.combo_items.addItem('Whiteboard Markers')
        self.combo_items.addItem('Hard Cover Book')
        self.combo_items.addItem('College Exercise Book')          
        
        self.feedback_btn = QPushButton('Feedback')                     # creating the feedback button
        self.feedback_btn.setFont(QFont('Arial',11,2))
        self.feedback_btn.clicked.connect(self.feedback_button)
        
        self.ok_btn = QPushButton('Ok')                     # creating the ok button
        self.ok_btn.setFont(QFont('Arial',11,2))
        self.ok_btn.clicked.connect(self.ok_button)
        
        self.close_btn = QPushButton('Close')                # creating the close button
        self.close_btn.setFont(QFont('Arial',11,2))
        self.close_btn.clicked.connect(self.close_button)
        
        self.grid = QGridLayout()                             # grid layout for all the other widgets
        self.grid.addWidget(self.combo_items,0,0)
        self.grid.addWidget(self.enter_item,1,0)
        self.grid.addWidget(self.feedback_btn,2,0)
        self.grid.addWidget(self.ok_btn,3,0)
        self.grid.addWidget(self.close_btn,3,1)        
        self.grid_widget = QWidget()
        self.grid_widget.setLayout(self.grid)
        
        self.hbox = QHBoxLayout()                     # layout for the shop's picture 
        self.hbox.addWidget(self.pic_label)
        self.hbox.addWidget(self.grid_widget)
        self.setLayout(self.hbox)
        
    def close_button(self):
        self.close()                # to exit when the close button is clicked
        
    def ok_button(self):
        self.sql_commands_runner = self.POS_Tables.execute("SELECT Available FROM StockTable")
        self.data = self.sql_commands_runner.fetchall()        # retrieves the data from Available field
        stockItem = self.combo_items.currentText()                # gets the current text from the combbox
        quant_select = self.enter_item.displayText()             # gets the text from the line edit
        
        for quantity in self.data:
            #print(quantity[0])
            
            if int(quantity[0]) >= int(quant_select):
                #print("___________")
                left = int(quantity[0]) - int(quant_select)
                new_quant = "UPDATE StockTable SET Available = ? WHERE ItemName = ?" # updates item after a sale has been made
                quants = (left, stockItem)
                self.sql_commands_runner.execute(new_quant, quants)
                date_purch = str(datetime.today())
                
                sold = int(quantity[0]) - left
                sales = "INSERT into SalesTable VALUES (?, ?, ?)"
                sales_thing = (stockItem,sold,date_purch)
                self.sql_commands_runner.execute(sales, sales_thing)
                
                self.POS_Tables.commit()
                
            else:
                feed_back = QMessageBox()
                feed_back.setText('Sorry, we do not have the number of items selected')
                feed_back.setWindowTitle('Feedback')
                feed_back.exec()
                
    def feedback_button(self): # create message box box
        report = QMessageBox()
        report.setText('This is the sales report window')
        report.setWindowTitle('Sales Report')
        report.exec()        
        
#sql_commands_runner.close()
#POS_Tables.close()
def main():
    app = QApplication(sys.argv)                              # creates necessary app object
    
    my_widget = Stationery_Pantry()                                # set window title
    my_widget.show()                                          # show window
    sys.exit(app.exec_())                                     # start executing main app event loop and return value to exit the system
    
main()    