import pickle

f = open("fichiers/comptes.dat", "wb")
pickle.dump([], f)
f.close()
