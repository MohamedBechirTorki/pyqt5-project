from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLabel, QFrame, QFileDialog, QMessageBox
from PyQt5.QtCore import QObject, QEvent
from PyQt5.QtGui import QPixmap
import pickle


class Frame(QFrame):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print(event)


class PushButton(QPushButton):
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
            if obj.objectName() in ["profile", "missions"]:
                func3()
            else:
                func()
            obj.setStyleSheet(active_style)
            if obj.objectName() == "ouvriers":
                ouvriers()
            elif obj.objectName() == "add_ouv":
                ajouter()
            elif obj.objectName() == "infos":
                infos()
            elif obj.objectName() == "profile":
                profile()
            elif obj.objectName() == "missions":
                missions()
            else:
                lire_suite(obj.objectName())
        return super().eventFilter(obj, event)


def admin():
    global login
    login = loadUi("fenetres/connection.ui")
    style = open("css/login.css", "r").read()
    login.setStyleSheet(style)
    login.show()
    login.connecter.clicked.connect(connecter_admin)


def func3():
    ouvrier.profile.setStyleSheet("")
    ouvrier.missions.setStyleSheet("")


def func():
    administration.ouvriers.setStyleSheet("")
    administration.add_ouv.setStyleSheet("")
    administration.infos.setStyleSheet("")


def lire_suite(cin):
    global T
    i = 0
    test = False
    while i < len(T) and not test:
        if T[i]["cin"] == cin:
            test = True
        else:
            i += 1
    info = loadUi("fenetres/informations.ui")
    info.show()
    info.image.setStyleSheet(f"""
        background-image: url("images/{cin}.jpg");
        background-position: 50%;
        border: 5px solid #333;
    """)
    info.label1.setText(T[i]["np"] + "\n" + T[i]["spécialiser"] +
                        "\nde l'age " + str(T[i]["age"]) + "\n")
    info.label2.setText("son salaire est " + str(T[i]["salaire"])+"\n"
                        + "son cin de numero " + T[i]["cin"] + "\n"
                        + "et son carte E-dinar de numero " + T[i]["carte"])
    style = open("css/informations.css", "r").read()
    info.setStyleSheet(style)
    info.exec_()


test = True


def ouvrier_func(T):
    administration.grid.setColumnStretch(0, 3)
    height = 0
    i, j = 0, 0
    for D in T:
        vbox = QVBoxLayout()
        image = QLabel()
        nom = QLabel(D["np"] + " "+str(D["age"]))
        nom.setStyleSheet("""
            color: white;
            font-size: 12px;
        """)
        nom.setFixedSize(160, 20)
        spec = QLabel(D["spécialiser"])
        spec.setObjectName("spec")
        spec.setFixedSize(160, 20)
        image.setStyleSheet("""
            background-image: url("images/"""+D["cin"]+""".jpg");
            background-position: 50%;
        """)
        image.setFixedSize(100, 150)
        btn = QPushButton("Lire la suite")
        btn.setObjectName(D["cin"])
        MouseObserver(btn)

        btn.setFixedSize(100, 30)
        vbox.addWidget(image)
        vbox.addWidget(nom)
        vbox.addWidget(spec)
        vbox.addWidget(btn)
        print(i, j)
        administration.grid.addLayout(vbox, i, j)
        if j == 0:
            height += 270
        j += 1
        if j == 3:
            j = 0
            i += 1
    administration.scroll.setFixedHeight(height)


def tri_salaire():
    global T
    permute = True
    while permute:
        permute = False
        for i in range(len(T)-1):
            if T[i]["salaire"] < T[i+1]["salaire"]:
                T[i], T[i+1] = T[i + 1], T[i]
                permute = True
    ouvrier_func(T)


def tri_age():
    global T
    permute = True
    while permute:
        permute = False
        for i in range(len(T)-1):
            if T[i]["age"] < T[i+1]["age"]:
                T[i], T[i+1] = T[i+1], T[i]
                permute = True
    ouvrier_func(T)


def ouvriers():
    global T
    administration.widgets.setCurrentWidget(administration.ouvrier_page)
    ouvrier_func(T)
    administration.tri_salaire.clicked.connect(tri_salaire)
    administration.tri_age.clicked.connect(tri_age)

    administration.ouvrier_page.setStyleSheet("""
        background-color: #232730;
    """)
    administration.grid.setSpacing(0)

    administration.scroll.setLayout(administration.grid)


def selectImage():
    global pixmap
    try:
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
        border: 4px solid black;
        """)
    except:
        return


def func2():
    global pixmap
    administration.np.setText("")
    administration.password.setText("")
    administration.age.setText("")
    administration.carte.setText("")
    administration.cin.setText("")
    administration.image.setPixmap(QPixmap())
    administration.image.setStyleSheet("")
    pixmap = ""


def ajt_btn():
    global T
    msg = QMessageBox()
    msg.setStyleSheet("""
        font-size: 15px;
        background-color: #333333;
        color: white;
    """)
    if administration.np.text() == "":
        msg.setText("Il faux saisir le nom et le prenom")
        msg.exec_()
    elif administration.password.text() == "":
        msg.setText("Il faux saisir la mot de passe")
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
    elif administration.choisir.currentText() == "Choisir":
        msg.setText("Il faux choisir une spécialiser")
        msg.exec_()
    elif not administration.salaire.text().isdigit() or int(administration.salaire.text()) < 100:
        msg.setText("Il faux saisir un salaire valide")
        msg.exec_()
    elif not pixmap:
        msg.setText("Il faux selectionner une image")
        msg.exec_()
    else:
        compte = {
            "np": administration.np.text(),
            "password": administration.password.text(),
            "age": int(administration.age.text()),
            "cin": administration.cin.text(),
            "carte": administration.carte.text(),
            "spécialiser": administration.choisir.currentText(),
            "salaire": eval(administration.salaire.text())
        }
        pixmap.save("images/"+compte["cin"]+".jpg")
        F = open("fichiers/comptes.dat", "rb")
        T = pickle.load(F)
        F.close()
        T.append(compte)
        F = open("fichiers/comptes.dat", "wb")
        pickle.dump(T, F)
        F.close()
        func2()
        msg.setText("Ce compte a été créé")
        msg.exec_()


def ajouter():
    administration.widgets.setCurrentWidget(administration.ajouter_page)
    administration.ouvrir.clicked.connect(selectImage)
    administration.ajt.clicked.connect(ajt_btn)


def checked_func():
    jobs = []
    if administration.backend.isChecked():
        jobs.append(administration.backend.text())
    if administration.fontend.isChecked():
        jobs.append(administration.fontend.text())
    if administration.graphic.isChecked():
        jobs.append(administration.graphic.text())
    if administration.data.isChecked():
        jobs.append(administration.data.text())
    nb = 0
    somme = 0
    for ouv in T:
        if ouv["spécialiser"] in jobs:
            nb += 1
            somme += ouv["salaire"]
    administration.nb.setText(str(nb))
    administration.somme.setText(str(somme))


def infos():
    administration.widgets.setCurrentWidget(administration.infos_page)
    administration.backend.clicked.connect(checked_func)
    administration.fontend.clicked.connect(checked_func)
    administration.data.clicked.connect(checked_func)
    administration.graphic.clicked.connect(checked_func)
    checked_func()


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
        #ouvriers, #add_ouv, #infos {
            border: 8px solid transparent;
            border-right-color: #C0C103;
        }
        """
        administration.ouvriers.setStyleSheet(active_style)
        ouvriers()
        MouseObserver(administration.ouvriers)
        MouseObserver(administration.add_ouv)
        MouseObserver(administration.infos)
        administration.exec_()


def connecter_ouvrier():
    global ouvrier, i
    global active_style
    username = login.username.text()
    password = login.password.text()
    i = 0
    test = False
    while i < len(T) and not test:
        if T[i]["np"] == username and T[i]["password"] == password:
            test = True
        else:
            i += 1

    if not test:
        login.msg.setText("Le Nom ou le mot de passe est incorrect")
    else:
        fenetre.close()
        login.close()
        ouvrier = loadUi("fenetres/ouvrier.ui")
        style = open("css/administration.css", "r").read()
        ouvrier.setStyleSheet(style)
        ouvrier.show()
        active_style = """
        #profile, #missions {
            border: 8px solid transparent;
            border-right-color: #C0C103;
        }
        """
        ouvrier.profile.setStyleSheet(active_style)
        profile()
        MouseObserver(ouvrier.profile)
        MouseObserver(ouvrier.missions)
        ouvrier.exec_()


missions_t = {
    "Graphique designer": ["Modifier l'image pic.jpg et envoyer par email",
                           "Faire UI designe d'un site web de vente online"],
    "Fontend developer": ["Faire le css de header section de notre site web",
                          "Ecrire le code javascript pour le partie (login)", ""],
    "Backend developer": ["Ecrire un code django dans une fichier server.py pour connecter index.html avec data.db", ""],
    "Data scientist": ["", ""]
}


def missions():
    global ouvrier
    ouvrier.widgets.setCurrentWidget(ouvrier.missions_page)
    ouvrier.mission1.setText(missions_t[T[i]["spécialiser"]][0])
    ouvrier.mission2.setText(missions_t[T[i]["spécialiser"]][1])


def profile():
    global ouvrier
    ouvrier.widgets.setCurrentWidget(ouvrier.profile_page)
    ouvrier.image.setStyleSheet("""
        background-image: url("images/""" + T[i]["cin"] + """.jpg");
        background-position: center;
    """)
    ouvrier.np.setText(T[i]["np"] + " " + str(T[i]["age"]) +
                       "\n\n\n" + T[i]["spécialiser"])
    ouvrier.cin.setText(T[i]["cin"])
    ouvrier.salaire.setText(str(T[i]["salaire"]))
    ouvrier.carte.setText(T[i]["carte"])


def ouvrier():
    global login
    login = loadUi("fenetres/connection.ui")
    style = open("css/login.css", "r").read()
    login.setStyleSheet(style)
    login.show()
    login.connecter.clicked.connect(connecter_ouvrier)


F = open("fichiers/comptes.dat", "rb")
T = pickle.load(F)
F.close()

style = open("css/fenetre.css", "r").read()
app = QApplication([])
fenetre = loadUi("fenetres/fenetre.ui")
fenetre.setStyleSheet(style)
fenetre.show()
fenetre.admin.clicked.connect(admin)
fenetre.ouvrier.clicked.connect(ouvrier)
app.exec_()
