import datetime
import random

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        self.file = open(self.filename, "r")
        self.users = {}

        for line in self.file:
            email, password, name, created = line.strip().split(";")
            self.users[email] = (password, name, created)

        self.file.close()

    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1
    def give_user_name(self,email):
        return self.users[email][1]
    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email exists already")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(user + ";" + self.users[user][0] + ";" + self.users[user][1] + ";" + self.users[user][2] + "\n")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


class bd_proposition:
    def __init__(self, filename):
        self.filename = filename
        self.propo = None
        self.file = None
        self.nbr_prop_par_bloc = 8
        self.nbr_bloc = 2
        self.current_bloc = None
        self.current_proposition = None
        self.load()
        #print(self.current_bloc)

    def load(self):
        self.file = open(self.filename, "r")
        self.propo = []

        for line in self.file:
            proposition, DE, AE, EN, IN, IS, IA, IAD, SM = line.split(";")
            self.propo.append([proposition,DE, AE, EN, IN, IS, IA, IAD, SM[:len(SM)-1]])
        self.file.close()

    def dict_proposition(self):
        return self.propo

    def set_current_bloc_proposition(self):
        if(self.nbr_bloc * self.nbr_prop_par_bloc != len(self.propo)):
            print('error')
        else:
            n = random.randint(1,self.nbr_bloc)
            #print(n)
            while self.current_bloc == n:
                n = random.randint(1, self.nbr_bloc)
                #print(n)
            return n
    def get_new_bloc_proposition(self):
        self.current_proposition = []
        n = 1
        for i in range((n-1)* self.nbr_prop_par_bloc,n*self.nbr_prop_par_bloc):
            self.current_proposition.append(self.propo[i][0])
        return self.current_proposition

allPropositions = ['J aime faire des pièces Catia', 'je souhaite construire un avenir avec des solutions durables','j adore créer des applications et des sites internet ',
'j ai toujours aimer associer le médical à l ingénieurie']


def initialisation():
    # connexion a mysql
    mypass = "Popsy123"
    mydatabase = "base_d_alfred"

    con = pymysql.connect(host="localhost", user="root", password=mypass, database=mydatabase)
    cur = con.cursor()
    #n = cur.execute("select * from majeures")
    compt = 0
    for i in range(0, len(allPropositions)):
        insertMaj = "insert into majeures(description_maj) values('" + allPropositions[i] + "');"
        try:
            #insertMaj = "insert into majeures(description_maj) values('J aime faire des pièces Catia');"
            cur.execute(insertMaj)
            con.commit()
            compt = compt + 1
        except:
            print("error")
            break
    #if compt == len(allPropositions):
        #messagebox.showinfo('succès', "La table a été initialisée avec succès!")
