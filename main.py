import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget, QPushButton, QDialog, QLineEdit, QComboBox, QDialogButtonBox
)
from PyQt6.uic import loadUi

class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("addEditCoffeeForm.ui", self)

        self.buttonBox.accepted.connect(self.save_data)
        self.buttonBox.rejected.connect(self.reject)

    def save_data(self):
        sort_name = self.sortNameEdit.text()
        roast_degree = self.roastDegreeEdit.text()
        ground = self.groundComboBox.currentText()
        taste_description = self.tasteDescriptionEdit.text()
        price = self.priceEdit.text()
        package_volume = self.packageVolumeEdit.text()

        if hasattr(self, 'coffee_id'):
            self.update_coffee(sort_name, roast_degree, ground, taste_description, price, package_volume)
        else:
            self.add_coffee(sort_name, roast_degree, ground, taste_description, price, package_volume)

        self.accept()

    def add_coffee(self, sort_name, roast_degree, ground, taste_description, price, package_volume):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO coffee (sort_name, roast_degree, ground, taste_description, price, package_volume)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sort_name, roast_degree, ground, taste_description, price, package_volume))
        connection.commit()
        connection.close()

    def update_coffee(self, sort_name, roast_degree, ground, taste_description, price, package_volume):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE coffee
            SET sort_name = ?, roast_degree = ?, ground = ?, taste_description = ?, price = ?, package_volume = ?
            WHERE id = ?
        """, (sort_name, roast_degree, ground, taste_description, price, package_volume, self.coffee_id))
        connection.commit()
        connection.close()

class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)

        self.tableWidget = self.findChild(QTableWidget, "tableWidget")
        self.load_data_button = self.findChild(QPushButton, "loadDataButton")
        self.add_button = self.findChild(QPushButton, "addButton")
        self.edit_button = self.findChild(QPushButton, "editButton")

        self.load_data_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_coffee)
        self.edit_button.clicked.connect(self.edit_coffee)
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Молотый/в зернах", "Описание вкуса", "Цена", "Объем упаковки"])

        for row_index, row_data in enumerate(rows):
            for col_index, cell_data in enumerate(row_data):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(cell_data)))

        connection.close()

    def add_coffee(self):
        dialog = AddEditCoffeeForm(self)
        dialog.exec()
        self.load_data()

    def edit_coffee(self):
        selected_items = self.tableWidget.selectedItems()
        if selected_items:
            try:
                coffee_id = int(selected_items[0].text())
            except ValueError:
                coffee_id = selected_items[0].text()
            dialog = AddEditCoffeeForm(self)
            dialog.coffee_id = coffee_id

            connection = sqlite3.connect("coffee.sqlite")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM coffee WHERE id = ?", (coffee_id,))
            row = cursor.fetchone()
            connection.close()

            if row:
                dialog.sortNameEdit.setText(row[1])
                dialog.roastDegreeEdit.setText(row[2])
                dialog.groundComboBox.setCurrentText(row[3])
                dialog.tasteDescriptionEdit.setText(row[4])
                dialog.priceEdit.setText(str(row[5]))
                dialog.packageVolumeEdit.setText(str(row[6]))

            dialog.exec()
            self.load_data()

def main():
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
