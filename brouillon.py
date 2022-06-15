import random


#current_bloc = 1
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
        if(nbr_bloc * nbr_prop_par_bloc != len(self.propo)):
            print('error')
        else:
            n = random.randint(1,nbr_bloc)
            print(n)
            while self.current_bloc == n:
                n = random.randint(1, nbr_bloc)
                print(n)
            self.current_bloc = n
            return self.current_bloc
    def get_new_bloc_proposition(self):
        self.current_proposition = []
        n = 1
        for i in range(self.nbr_prop_par_bloc,16):
            self.current_proposition.append(self.propo[i][0])
        return self.current_proposition

class test:
    def __init__(self):
        self.nbr = None
    def get_nbr(self):
        return self.nbr
    def aleatoire(self):
        self.nbr = random.randint(1,5)
        return self.nbr


T = test()
print(T.get_nbr())
print(T.aleatoire())




#print(bd_proposition("proposition.txt").set_current_bloc_proposition())
#print(bd_proposition("proposition.txt").get_new_bloc_proposition())
