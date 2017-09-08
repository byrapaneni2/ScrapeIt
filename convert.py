import pickle
import json
data = pickle.load(open("parsed/sale/apartment/Agra/4d423236373939383037.pkl","rb"))
output = open("c.txt","w")
output.write(str(data))
output.flush()
output.close()