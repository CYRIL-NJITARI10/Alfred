
list_majeures = ["DE","AE","EN","IN","IS","IA","IAD","SM"]
indice = 0
def get_info_majeure(filename):
    file = open(filename, "r")
    infoM = ""
    for line in file:
        infoM += line
    file.close()
    return infoM


obFichier.write('<a href="http://www.ma-page-web.fr/logitheque/">CLIQUER SUR CE LIEN</a>')

#print(get_info_majeure("in"))
