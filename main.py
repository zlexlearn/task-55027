import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt6.uic import loadUi

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)

        self.tableWidget = self.findChild(QTableWidget, "tableWidget")
        self.load_data_button = self.findChild(QPushButton, "loadDataButton")

        self.load_data_button.clicked.connect(self.load_data)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        c = connection.cursor()
        c.execute("SELECT * FROM coffee")
        rows = c.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])

        for row_index, row_data in enumerate(rows):
            for col_index, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

        connection.close()

def main():
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()