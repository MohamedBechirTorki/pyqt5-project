from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap

import pickle


f = open("fichiers/admin.dat", "wb")
D = {
    "username": "Mohamed",
    "password": "1234"
}
pickle.dump(D, f)
f.close()

app = QApplication([])
administration = loadUi("fenetres/administration.ui")
style = open("css/administration.css", "r").read()
administration.setStyleSheet(style)
administration.show()
app.exec_()
