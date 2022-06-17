from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.label import Label
from database import *


compt = 0
result_sorted = []
# Step 2: Création des fenêtres différentes classes et methodes associées

    # fenêtre principale après connexion  Ma majeure/Resultat/Info Majeures/Paramètres
class MainWindow(Screen):
    pass

    # fenêtre des propositions Oui/Neutre/Non

class MajeureWindow(Screen):
    global result_sorted
    first = StringProperty("")
    second = StringProperty("")
    third = StringProperty("")
    #result_sorted = ObjectProperty()
    def on_enter(self, *args):
        message_warning(self.manager.get_screen("login").ids.itmd.text)

    proposition = StringProperty(bd_proposition("proposition.txt").get_new_bloc_proposition()[0])
    def update_text(self,label_text):
        self.box.text = label_text
    def ajout_point_majeure(self):
        bd_p.calcul_ajout(bd_p.get_new_bloc_proposition()[compt])
    def retrait_point_majeure(self):
        bd_p.calcul_retrait(bd_p.get_new_bloc_proposition()[compt])

    def new_proposition(self):
        global compt
        global result_sorted
        compt += 1
        if (compt == len(bd_p.get_new_bloc_proposition())):
            compt = 0
            bd_p.aleatoire()
            result_sorted = bd_p.dict_resultat()
            self.first = result_sorted[-1][0] + ": " + str(result_sorted[-1][1])
            self.second = result_sorted[-2][0] + ": " + str(result_sorted[-2][1])
            self.third = result_sorted[-3][0] + ": " + str(result_sorted[-3][1])
            print(result_sorted)
            bd_p.reset_dict_maj(dict_majeure)
            sm.current = "Accueil"
            result_dispo()
        self.proposition = bd_p.get_new_bloc_proposition()[compt]

    # fenêtre Info Majeures

class InfoWindow(Screen):
   pass

    # La classe qui permet de gerer le passage d'une fenêtre à l'autre : les transitions
class WindowManager(ScreenManager):
    pass
    # fenêtre Paramètres appli
class ParametresWindow(Screen):
    pass

    # fenêtre resultat
class ResultWindow(Screen):
    def on_enter(self, *args):
        self.first_label.text = self.manager.get_screen("Majeure").ids.first_itrm.text
        self.second_label.text = self.manager.get_screen("Majeure").ids.second_itrm.text
        self.third_label.text = self.manager.get_screen("Majeure").ids.third_itrm.text
        self.first_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.first_itrm.text[:2])
        self.second_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.second_itrm.text[:2])
        self.third_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.third_itrm.text[:2])
        #print(self.manager.get_screen("Majeure").ids.third_itrm.text[:3])
        #print(len(self.manager.get_screen("Majeure").ids.third_itrm.text[:-3]))
    first_maj_ttl = ObjectProperty()
    second_maj_ttl = ObjectProperty()
    third_maj_ttl = ObjectProperty()
    first_label = ObjectProperty()
    second_label = ObjectProperty()
    third_label = ObjectProperty()


    # fenêtre login
class LoginWindow(Screen):
    intermediaire = ObjectProperty(None)  # intermediaire est la variable qui nous permet d'utiliser le user_name collecté sur la fênetre create account et stocké dans la bd

    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.intermediaire.text = db.give_user_name(self.email.text) + ", \n\nRépond aux affirmations et obtient \nle resultat dans la section RESULTAT"
            self.reset()
            sm.current = "Accueil"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

# fenêtre de creation de compte

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""

# fonctions appelées en cas d'erreur de replissage des champs de saisie

def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid email or password.'),
                  size_hint=(.7, .7), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(.7, .7), size=(400, 400))

    pop.open()

def result_dispo():
    pop = Popup(title='Bravo!',
                  content=Label(text='Success! \n Les resultats de votre dernier test\n sont disponible dans la section Resultat\n'),
                  size_hint=(.8, .7), size=(400, 400))

    pop.open()
def message_warning(name_user):
    pop = Popup(title='Attention!!!',
                content=Label(
                    text= "Bonjour " + name_user + ", \n\n Tes réponses aux affirmation \ndéfinissent la qualité de tes resultat."),
                size_hint=(.8, .7), size=(400, 400))


    pop.open()

#FONCTION retiurne majeure en toute lettre

def maj_en_toute_lettre(majeure):
    if(majeure == 'DE'):
        return 'DATA ENGINEERING'
    elif (majeure == 'AE'):
        return 'AERONAUTIQUE ET ESPACE'
    elif (majeure == 'IN'):
        return 'INGENIERIE NUMERIQUE'
    elif (majeure == 'SM'):
        return 'STRUCTURE ET MATERIAUX\n                 DURABLE'
    elif (majeure == 'EN'):
        return 'ENERGIE ET ENVIRONNEMENT'
    elif (majeure == 'IAD'):
        return 'INGENIERIE ET ARCHITECTURE\n                DURABLE'
    elif (majeure == 'IA'):
        return 'INGENIERIE ET MANAGEMENT'
    elif (majeure == 'IS'):
        return 'INGENIERIE ET SANTE'
    else:
        return 'ERROR'

# liaison avec le fichier kv
kv = Builder.load_file("Alfred.kv")
db = DataBase("users.txt")
bd_p = bd_proposition("proposition.txt")
# A sm on affecte une instance de windowManager classe qui nous permet de gérer le passage d'une fenêtre à l'autre
sm = WindowManager()

# On ajoute toutes les fenêtres devant être ajoutées
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="Accueil"),MajeureWindow(name="Majeure"),ParametresWindow(name="param"),ResultWindow(name="result"),InfoWindow(name="Info")]
for screen in screens:
    sm.add_widget(screen)

# On definit la première fenêtre qui va s'afficher
sm.current = "Accueil"

# on definit le constructeur de l'appli
class AlfredApp(App):
    def build(self):
        return sm

# On run l'appli
if __name__ == "__main__":
    Window.size = (397, 550)
    #Window.clearcolor = (1,1,1,1)
    AlfredApp().run()

