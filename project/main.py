from ctypes import resize
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QFrame, QFileDialog, QMessageBox
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPixmap
import pickle


class Frame(QFrame):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print(event)


class MouseObserver(QObject):
    def __init__(self, widget):
        super().__init__(widget)
        self._widget = widget
        self.widget.installEventFilter(self)

    @property
    def widget(self):
        return self._widget

    def eventFilter(self, obj, event):
        if obj is self.widget and event.type() == QEvent.MouseButtonPress:
            func()
            obj.setStyleSheet(active_style)
            if obj.objectName() == "ouvriers":
                ouvriers()
            elif obj.objectName() == "add_ouv":
                ajouter()
            else:
                discuter()
        return super().eventFilter(obj, event)


def admin():
    global login
    login = loadUi("fenetres/connection.ui")
    style = open("css/login.css", "r").read()
    login.setStyleSheet(style)
    login.show()
    login.connecter.clicked.connect(connecter_admin)


def func():
    administration.ouvriers.setStyleSheet("")
    administration.add_ouv.setStyleSheet("")
    administration.discuter.setStyleSheet("")


def ouvriers():
    administration.widgets.setCurrentWidget(administration.ouvrier_page)


def selectImage():
    global pixmap
    pixmap = ""
    print(1)
    fname = QFileDialog.getOpenFileName(
        caption="Open file", directory="", filter="Image files (*jpeg *.jpg *.gif)")
    imagePath = fname[0]
    pixmap = QPixmap(imagePath)
    pixmap = pixmap.scaledToHeight(130)
    administration.image.setPixmap(QPixmap(pixmap))
    administration.image.resize(pixmap.width(), pixmap.height())
    administration.image.setStyleSheet("""
    border: 4px solid gray;
    """)


def func2():
    global pixmap
    administration.nom.setText("")
    administration.prenom.setText("")
    administration.age.setText("")
    administration.carte.setText("")
    administration.cin.setText("")
    administration.image.setPixmap(QPixmap())
    administration.image.setStyleSheet("")
    pixmap = ""


def ajt_btn():
    msg = QMessageBox()
    msg.setStyleSheet("""
        font-size: 15px;
        background-color: #333333;
        color: white;
    """)
    if administration.nom.text() == "":
        msg.setText("Il faux saisir le nom")
        msg.exec_()
    elif administration.prenom.text() == "":
        msg.setText("Il faux saisir le prenom")
        msg.exec_()
    elif administration.age.text() == "" or not administration.age.text().isdigit() or not 17 < int(administration.age.text()) < 90:
        msg.setText("Il faux saisir un age valide")
        msg.exec_()
    elif len(administration.cin.text()) != 8 or not administration.cin.text().isdigit():
        msg.setText("Il faux saisir un numero de cin contient 8 chiffres")
        msg.exec_()
    elif len(administration.carte.text()) != 16 or not administration.carte.text().isdigit():
        msg.setText("Il faux saisir un numero de carte contient 16 chiffres")
        msg.exec_()
    elif not pixmap:
        msg.setText("Il faux selectionner une image")
        msg.exec_()
    else:
        compte = {
            "nom": administration.nom.text(),
            "prenom": administration.prenom.text(),
            "age": int(administration.age.text()),
            "cin": administration.cin.text(),
            "carte": administration.carte.text(),
        }
        pixmap.save("images/"+compte["cin"]+".jpg")
        F = open("fichiers/comptes.dat", "ab")
        pickle.dump(compte, F)
        func2()
        msg.setText("Ce compte a été créé")
        msg.exec_()


def ajouter():
    administration.widgets.setCurrentWidget(administration.ajouter_page)
    administration.ouvrir.clicked.connect(selectImage)
    administration.ajt.clicked.connect(ajt_btn)


def discuter():
    print(2)


def connecter_admin():
    global administration
    global active_style
    username = login.username.text()
    password = login.password.text()
    F = open("fichiers/admin.dat", "rb")
    D = pickle.load(F)
    if username != D["username"] or password != D["password"]:
        login.msg.setText("Le Nom ou le mot de passe est incorrect")
    else:
        fenetre.close()
        login.close()
        administration = loadUi("fenetres/administration.ui")
        style = open("css/administration.css", "r").read()
        administration.setStyleSheet(style)
        administration.show()
        active_style = """
        #ouvriers, #add_ouv, #discuter {
            border: 8px solid transparent;
            border-right-color: #C0C103;
        }
        """
        administration.ouvriers.setStyleSheet(active_style)
        ouvriers()
        MouseObserver(administration.ouvriers)
        MouseObserver(administration.add_ouv)
        MouseObserver(administration.discuter)
        administration.exec_()


style = open("css/fenetre.css", "r").read()
app = QApplication([])
fenetre = loadUi("fenetres/fenetre.ui")
fenetre.setStyleSheet(style)
fenetre.show()
fenetre.admin.clicked.connect(admin)
app.exec_()
