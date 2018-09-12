d = {'l':1.123,'m':1.3,'n':0.334,'b':15}

list = sorted(d.items(),key=lambda item:item[1],reverse=True)

print(list)
