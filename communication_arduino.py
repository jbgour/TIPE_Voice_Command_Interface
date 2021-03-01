from serial import Serial

def instructions(chaine):
    #lettre à entrer par exemple
    serial_port.write(str(chaine).encode('ascii')) #envoi de l'instruction, codée en ascii
    serial_port.readline()#lit ce qu'envoie l'arduino