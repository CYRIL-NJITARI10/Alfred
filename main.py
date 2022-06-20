from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import matplotlib.pyplot as plt
from database import *


compt = 0
result_sorted = []
list_tuple_result = []
test_success = False
reset_last_test = False
# Step 2: Création des fenêtres différentes classes et methodes associées

    # fenêtre principale après connexion  Ma majeure/Resultat/Info Majeures/Paramètres
class MainWindow(Screen):
    def on_enter(self, *args):
        global reset_last_test
        self.user_N = db.give_user_name(self.manager.get_screen("login").ids.current_email.text)
        if (reset_last_test == False and rslt.get_user_result(self.user_N) != -1):
            self.manager.get_screen("result").ids.first_label.text = rslt.get_user_result(self.user_N)[-3]
            self.manager.get_screen("result").ids.second_label.text = rslt.get_user_result(self.user_N)[-2]
            self.manager.get_screen("result").ids.third_label.text = rslt.get_user_result(self.user_N)[-1]
            self.manager.get_screen("result").ids.second_label.text = rslt.get_user_result(self.user_N)[-2]
            self.manager.get_screen("result").first_maj_ttl.text = maj_en_toute_lettre(rslt.get_user_result(self.user_N)[-3][:rslt.get_user_result(self.user_N)[-3].find(":")])
            self.manager.get_screen("result").second_maj_ttl.text = maj_en_toute_lettre(rslt.get_user_result(self.user_N)[-2][:rslt.get_user_result(self.user_N)[-2].find(":")])
            self.manager.get_screen("result").third_maj_ttl.text = maj_en_toute_lettre(rslt.get_user_result(self.user_N)[-1][:rslt.get_user_result(self.user_N)[-1].find(":")])
    # fenêtre des propositions Oui/Neutre/Non

class MajeureWindow(Screen):
    global result_sorted
    first = StringProperty("")
    second = StringProperty("")
    third = StringProperty("")
    user_N = ObjectProperty()
    proposition = StringProperty(bd_proposition("proposition.txt").get_new_bloc_proposition()[0])

    def on_enter(self, *args):
        self.user_N = db.give_user_name(self.manager.get_screen("login").ids.current_email.text)
        message_warning(self.manager.get_screen("login").ids.itmd.text)
        call_premier_essai(self.user_N)


    def update_text(self,label_text):
        self.box.text = label_text
    def ajout_point_majeure(self):
        bd_p.calcul_ajout(bd_p.get_new_bloc_proposition()[compt])
    def retrait_point_majeure(self):
        bd_p.calcul_retrait(bd_p.get_new_bloc_proposition()[compt])

    def new_proposition(self):
        global compt
        global result_sorted
        global list_tuple_result, test_success, reset_last_test
        compt += 1
        if (compt == len(bd_p.get_new_bloc_proposition())):
            compt = 0
            test_success = True
            reset_last_test = False
            bd_p.aleatoire()
            list_tuple_result = bd_p.list_tupl_result()
            result_sorted = bd_p.dict_resultat()
            self.first = result_sorted[-1][0] + ": " + str(result_sorted[-1][1])
            self.second = result_sorted[-2][0] + ": " + str(result_sorted[-2][1])
            self.third = result_sorted[-3][0] + ": " + str(result_sorted[-3][1])
            rslt.add_user_result(list_tuple_result,self.first,self.second,self.third, self.user_N)
            #print(result_sorted)
            #bd_p.reset_dict_maj(dict_majeure)
            sm.current = "Accueil"
            result_dispo()
        self.proposition = bd_p.get_new_bloc_proposition()[compt]
    # fenêtre detail Info
class DetailInfoWindow(Screen):
    pass
    # fenêtre Info Majeures
class InfoWindow(Screen):
    pass

    # La classe qui permet de gerer le passage d'une fenêtre à l'autre : les transitions
class WindowManager(ScreenManager):
    pass
class Statistiques(Screen):
    text_result_stat1 = ObjectProperty(str(resultat("resultats").statistiques()["DE"][0])+"           "+str(resultat("resultats").statistiques()["DE"][1])+"           "+str(resultat("resultats").statistiques()["DE"][2]))
    text_result_stat2 =ObjectProperty(str(resultat("resultats").statistiques()["AE"][0])+"           "+str(resultat("resultats").statistiques()["AE"][1])+"           "+str(resultat("resultats").statistiques()["AE"][2]))
    text_result_stat3 = ObjectProperty(str(resultat("resultats").statistiques()["EN"][0])+"           "+str(resultat("resultats").statistiques()["EN"][1])+"           "+str(resultat("resultats").statistiques()["EN"][2]))
    text_result_stat4 = ObjectProperty(str(resultat("resultats").statistiques()["IN"][0])+"           "+str(resultat("resultats").statistiques()["IN"][1])+"           "+str(resultat("resultats").statistiques()["IN"][2]))
    text_result_stat5 = ObjectProperty(str(resultat("resultats").statistiques()["IS"][0])+"           "+str(resultat("resultats").statistiques()["IS"][1])+"           "+str(resultat("resultats").statistiques()["IS"][2]))
    text_result_stat6 = ObjectProperty(str(resultat("resultats").statistiques()["IA"][0])+"           "+str(resultat("resultats").statistiques()["IA"][1])+"           "+str(resultat("resultats").statistiques()["IA"][2]))
    text_result_stat7 = ObjectProperty(str(resultat("resultats").statistiques()["IAD"][0])+"           "+str(resultat("resultats").statistiques()["IAD"][1])+"           "+str(resultat("resultats").statistiques()["IAD"][2]))
    text_result_stat8 = ObjectProperty(str(resultat("resultats").statistiques()["SM"][0])+"           "+str(resultat("resultats").statistiques()["SM"][1])+"           "+str(resultat("resultats").statistiques()["SM"][2]))

    # fenêtre Paramètres appli
class ParametresWindow(Screen):
    def reset_dernier_test(self):
        global reset_last_test
        bd_p.reset_dict_maj(dict_majeure)
        reset_last_test = True
        self.user_N = db.give_user_name(self.manager.get_screen("login").ids.current_email.text)
        self.manager.get_screen("result").ids.first_label.text = ""
        self.manager.get_screen("result").ids.second_label.text = ""
        self.manager.get_screen("result").ids.third_label.text = ""
        self.manager.get_screen("result").ids.second_label.text = ""
        self.manager.get_screen("result").first_maj_ttl.text = ""
        self.manager.get_screen("result").second_maj_ttl.text = ""
        self.manager.get_screen("result").third_maj_ttl.text = ""
        print("reset ok")

    # fenêtre resultat
class ResultWindow(Screen):
    def on_enter(self, *args):
        if(test_success and reset_last_test == False):
            self.first_label.text = self.manager.get_screen("Majeure").ids.first_itrm.text
            self.second_label.text = self.manager.get_screen("Majeure").ids.second_itrm.text
            self.third_label.text = self.manager.get_screen("Majeure").ids.third_itrm.text
            self.first_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.first_itrm.text[:self.manager.get_screen("Majeure").ids.first_itrm.text.find(':')])
            self.second_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.second_itrm.text[:self.manager.get_screen("Majeure").ids.second_itrm.text.find(':')])
            self.third_maj_ttl.text = maj_en_toute_lettre(self.manager.get_screen("Majeure").ids.third_itrm.text[:self.manager.get_screen("Majeure").ids.third_itrm.text.find(':')])
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
    current_email = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.current_email.text = self.email.text
            self.intermediaire.text =  "\n\nRépond aux affirmations " + db.give_user_name(self.email.text) + " et obtient \nle resultat dans la section RESULTAT"
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
                    text=  name_user + ", \n\n Tes réponses aux affirmations \ndéfinissent la qualité de tes resultat."),
                size_hint=(.8, .7), size=(400, 400))


    pop.open()

def call_premier_essai(user_name):
    if(rslt.have_last_result(user_name)):
        pop = Popup(title='Attention!!!',
                        content=Label(
                        text="Bonjour " + user_name + ", \n\n C'est parti pour ton premier essai "),
                        size_hint=(.7, .7), size=(400, 400))

        pop.open()
    else:
        pop = Popup(title='Attention!!!',
                    content=Label(
                        text="Heureux de te revoir " + user_name + ", \n\n Réinitialise tout et recommence dans\n la section Paramètres \nsi non ignore ce message et \ncontinue ton dernier test "),
                    size_hint=(.7, .7), size=(400, 400))

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
rslt = resultat("resultats")
# A sm on affecte une instance de windowManager classe qui nous permet de gérer le passage d'une fenêtre à l'autre
sm = WindowManager()

# On ajoute toutes les fenêtres devant être ajoutées
screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"), MainWindow(name="Accueil"),MajeureWindow(name="Majeure"),ParametresWindow(name="param"),ResultWindow(name="result"),InfoWindow(name="Info"),DetailInfoWindow(name="DetailInfo"),Statistiques(name="stats")]
for screen in screens:
    sm.add_widget(screen)

# On definit la première fenêtre qui va s'afficher
sm.current = "stats"

# on definit le constructeur de l'appli
class AlfredApp(App):
    def build(self):
        return sm

# On run l'appli
if __name__ == "__main__":
    Window.size = (397, 550)
    #Window.clearcolor = (1,1,1,1)
    AlfredApp().run()

