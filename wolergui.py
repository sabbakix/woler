import tkinter as tk
from tkinter import messagebox
from wakeonlan import send_magic_packet
import csv

list_pc = {}
with open('list.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    next(csvFile)  # Skip the header row
    for lines in csvFile:
        list_pc[lines[0]] = lines[1]

def wakePc(name, mac):
    print("Starting  "+name+" MAC:"+str(mac).strip())
    send_magic_packet(str(mac).strip(), ip_address='192.168.0.255', port=9)
    messagebox.showinfo("Info", "Magic packet sent to " + name)

def wakeAll():
    for name, mac in list_pc.items():
        wakePc(name, mac)

root = tk.Tk()
root.title("Wake-on-LAN")

frame = tk.Frame(root)
frame.pack(padx=30, pady=20)

for i, (name, mac) in enumerate(list_pc.items()):
    button = tk.Button(frame, text="Wake " + name, command=lambda name=name, mac=mac: wakePc(name, mac))
    button.pack(side=tk.TOP, padx=10, pady=5, anchor='w')


wake_all_button = tk.Button(frame, text="Wake All", command=wakeAll)
wake_all_button.pack(side=tk.TOP)

exit_button = tk.Button(frame, text="QUIT", fg="red", command=root.destroy)
exit_button.pack(side=tk.BOTTOM)

root.mainloop()