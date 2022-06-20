import datetime
import random
from kivy.uix.floatlayout import FloatLayout


nbr_bloc = 9
id_bloc = random.randint(1, nbr_bloc)
dict_majeure = {}

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
        self.nbr_prop_par_bloc = 9
        self.nbr_bloc = 9
        self.current_bloc = None
        self.list_majeures = None
        self.id_bloc = 1
        self.load()


    def load(self):
        global dict_majeure
        self.file = open(self.filename, "r")
        self.propo = []
        self.list_majeures = ["DE","AE","EN","IN","IS","IA","IAD","SM"]

        for line in self.file:
            proposition, DE, AE, EN, IN, IS, IA, IAD, SM = line.split(";")
            self.propo.append([proposition,int(DE), int(AE), int(EN), int(IN), int(IS), int(IA), int(IAD), int(SM[:len(SM)-1])])
        self.file.close()
        for i in self.list_majeures:
            dict_majeure[i]=0
    def dict_proposition(self):
        return self.propo

    def calcul_ajout(self,affirmation_courante):
        global dict_majeure
        for i in range(0,len(self.propo)):
            if(self.propo[i][0] == affirmation_courante):
                for j in range(1,len(self.propo[i])):
                    dict_majeure[self.list_majeures[j - 1]] += self.propo[i][j]
    def calcul_retrait(self,affirmation_courante):
        global dict_majeure
        for i in range(0,len(self.propo)):
            if(self.propo[i][0] == affirmation_courante):
                for j in range(1,len(self.propo[i])):
                    dict_majeure[self.list_majeures[j - 1]] -= self.propo[i][j]
    def list_tupl_result(self):
        return list(zip(dict_majeure.keys(), dict_majeure.values()))
    def dict_resultat(self):
        return sorted(dict_majeure.items(), key=lambda t: t[1])
    def reset_dict_maj(self,dict_majeure):
        for i in self.list_majeures:
            dict_majeure[i]=0
    def aleatoire(self):
        global id_bloc
        n = 0
        if (self.nbr_bloc * self.nbr_prop_par_bloc != len(self.propo)):
            print('No pasa nada')
        else:
            n = random.randint(1, self.nbr_bloc)
            while id_bloc == n:
                n = random.randint(1, self.nbr_bloc)
        id_bloc = n
    def get_new_bloc_proposition(self):
        global id_bloc
        self.current_bloc = []
        for i in range((id_bloc - 1) * self.nbr_prop_par_bloc,id_bloc * self.nbr_prop_par_bloc):
            if(self.propo[i][0] not in self.list_majeures):
                if(len(self.propo[i][0])>62):
                    self.current_bloc.append(self.propo[i][0][:62][:self.propo[i][0][:62].rfind(" ")]+"\n"+self.propo[i][0][self.propo[i][0][:62].rfind(" "):])
                else:
                    self.current_bloc.append(self.propo[i][0])
        return self.current_bloc




class resultat:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.result = None
        self.stat_tab = None
        self.list_majeures = None
        self.load()


    def load(self):
            self.file = open(self.filename, "r")
            self.result = {}
            self.stat_tab = {}
            self.list_majeures = ["DE", "AE", "EN", "IN", "IS", "IA", "IAD", "SM"]

            for line in self.file:
                user_name,DE, AE, EN, IN, IS, IA, IAD, SM,max1,max2,max3 = line.strip().split(";")
                self.result[user_name] = (DE, AE, EN, IN, IS, IA, IAD, SM, max1, max2, max3)
            for i in range(0,8):
                self.stat_tab[self.list_majeures[i]] = [0,0,0]
            self.file.close()
    def get_user_result(self, user_name):
        if user_name in self.result:
            return self.result[user_name]
        else:
            return -1
    def add_user_result(self, table_result_sorted,max1,max2,max3,user_name):
            self.result[user_name] = (str(table_result_sorted[0][1]), str(table_result_sorted[1][1]), str(table_result_sorted[2][1]),str(table_result_sorted[3][1]),str(table_result_sorted[4][1]),str(table_result_sorted[5][1]),str(table_result_sorted[6][1]),str(table_result_sorted[7][1]),max1,max2,max3)
            self.save()
    def have_last_result(self, user_name):
        if user_name not in self.result:
            return True
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.result:
                f.write(user + ";" + self.result[user][0] + ";" + self.result[user][1] + ";" + self.result[user][2]+ ";"  +self.result[user][3]+ ";" +self.result[user][4]+ ";" +self.result[user][5] + ";" + self.result[user][6]+ ";" +self.result[user][7]+ ";" +self.result[user][8]+ ";" + self.result[user][9]+ ";" + self.result[user][10]+"\n")

    def statistiques(self):
        for i in range(0,8):
            for k,v in self.result.items():
                if(v[i] == "-1"):
                    self.stat_tab[self.list_majeures[i]][0] += int(100/len(self.result))
                if (v[i] == "0"):
                    self.stat_tab[self.list_majeures[i]][1] += int(100/len(self.result))
                if (v[i] == "1"):
                    self.stat_tab[self.list_majeures[i]][2] += int(100/len(self.result))
        #print(len(self.stat_tab))
        return self.stat_tab



#print(resultat("resultats").statistiques())
