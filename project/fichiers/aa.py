import pickle

# Remplace 'ton_fichier.pkl' par le nom de ton fichier pickle
with open('comptes.dat', 'rb') as f:
    tableau = pickle.load(f)

print(tableau)
