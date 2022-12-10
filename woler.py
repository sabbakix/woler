from wakeonlan import send_magic_packet
#import os, time

import csv

list_pc = {}

with open('list.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            #print(f'\t{row[0]} : {row[1]}')
            list_pc[row[0]] = row[1]
            line_count += 1
    #print(f'Processed {line_count} lines.')


while True:
    #os.system('cls')
    # Print menu
    print('- - - - - - - - - - - - - - - - - - ')
    for i, x in enumerate(list_pc):
        print(str(i)+" : "+x)
        #print(x+" "+str(list_pc[x]))
    print("x  : esci")
    print('- - - - - - - - - - - - - - - - - - ')

    postazione = input('Seleziona una postazione: ')

    if(postazione=="x"):
        exit()

    postazione = int(postazione)

    if(postazione==0):
        print("Accendi tutte le postazioni...")
        for i, x in enumerate(list_pc):
            if(i==0):
                continue
            print(str(i)+" Starting  "+x+" ...")
            send_magic_packet(str(list_pc[x]), ip_address='192.168.0.255', port=9)

    else:
        for i, x in enumerate(list_pc):
            if(postazione==i):
                print(str(i)+" Starting  "+x+" ...")
                send_magic_packet(str(list_pc[x]), ip_address='192.168.0.255', port=9)

    #time.sleep(2)
