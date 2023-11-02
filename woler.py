from wakeonlan import send_magic_packet

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

def wakePc(selection,name,mac):
    print(str(selection)+" Starting  "+name+" MAC:"+str(mac).strip())
    send_magic_packet(str(mac).strip(), ip_address='192.168.0.255', port=9)

while True:
    #os.system('cls')
    # Print menu
    print('- - - - - - - - - - - - - - - - - - ')
    for i, x in enumerate(list_pc):
        print(str(i)+" : "+x)
        #print(x+" "+str(list_pc[x]))
    print("a  : Wake Up All PCs")
    print("q  : Quit")
    print('- - - - - - - - - - - - - - - - - - ')

    postazione = input('Select a PC: ')

    if(postazione=="q"):
        exit()

    if(postazione=="a"):
        print("Wake Up All PCs ...")
        for i, x in enumerate(list_pc):
            wakePc(i,x,list_pc[x])
            #print(str(i)+" Starting  "+x+ "MAC:"+str(list_pc[x])+" ...")
            #send_magic_packet(str(list_pc[x]), ip_address='192.168.0.255', port=9)

    else:
        postazione = int(postazione)
        for i, x in enumerate(list_pc):
            if(postazione==i):
                wakePc(i,x,list_pc[x])
                #print(str(i)+" Starting  "+x+" ...")
                #send_magic_packet(str(list_pc[x]), ip_address='192.168.0.255', port=9)



