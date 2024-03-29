#DEFINITION DES FONCTIONS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier


#Définition genreDummies pour créer des variables binaires pour le genre de films
def genresDummies(DataFrame):
  '''création d'une colonne pour chaque genre de films et codage binaire'''
  tmp = DataFrame["genres"].str.split('|',expand=True)
  for element in tmp[0].unique():
    DataFrame[element]=0
    DataFrame.loc[DataFrame["genres"].str.contains(element), element] = 1

def askMeGenre(df) :
    '''fonction qui demande un genre de film à l'utilisateur et retourne les statistiques principales de ce genre de film dans la bdd'''
    print("Hello ! Quel genre de film aimez-vous ?")
    genre = input("Action, Adventure, Animation, Children's, Comedy, Crime, \n Documentary, Drama, Fantasy, Film-Noir, Horror, Musical, Mystery, Romance, Sci-Fi, Thriller, War, Western ? ")
    genre = str.capitalize(genre)
    # calculs sur le df total :
    NbFilmsTotaux = len(np.unique(df.movieId))
    MOY = df.groupby('movieId').mean()['rating'].mean() 
    
    # subset de dataframe correspondant au genre :
    res = df[df[genre] == 1]
    # calculer les stats descriptives pour ce genre et les afficher
    # on regroupe les avis par film en utilisant movieId:
    df_grouped = res.groupby('movieId')

    # nombre de films de ce genre : 
    nbFilm = len(df_grouped)
    print(f'Il y a {nbFilm} films répertoriés pour le genre {genre}')
    if nbFilm > NbFilmsTotaux/ 5 :
        print('Il y a du choix dans cette catégorie !!')
    
    # nombre de films | % / films totaux 
    print(f'Cela représente {round(nbFilm / NbFilmsTotaux  * 100, 1)} % des films totaux')
    # moyenne des films de ce genre :
    df_grouped.mean()['rating'].sort_values(ascending = False)
    MoyParGenre = df_grouped.mean()['rating'].mean()
    print(f'En moyenne ces films sont notés {round(MoyParGenre,1)} / 5 étoiles (la moyenne pour tous les films est {round(MOY,1)})')
    
    # boxplot montrant la distribution des films de cette catégorie
    # réglagle des sorties graphiques
    font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

    plt.rc('font', **font)
    
    plt.figure(figsize = (20, 8))
    plt.subplot(1,2,1)
    sns.boxplot(y = res['rating'], showmeans=True)
    plt.title(f'Répartition des notes pour le genre : {genre}')

    # répartition des notes:
    plt.subplot(1,2,2)
    sns.distplot(res['rating'], kde = False)
    plt.title(f'Voici la distribution des notes pour le genre {genre}')
    plt.tight_layout()
    plt.show()

# fonction qui lit un fichier texte
def lectureTxt(name = 'listeFilm.txt'):
    '''fonction qui lit un fichier texte et renvoit une liste des éléments lus'''
    f = open(name, 'r', encoding = "utf8")
    listeFilm = []
    content = f.readlines()
    for x in content:
        listeFilm.append(x.strip())

    return(listeFilm)
