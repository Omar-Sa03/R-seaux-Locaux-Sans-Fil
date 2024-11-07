import platform
import subprocess
import re
import time
import tkinter as tk
from tkinter import messagebox

def scan_networks():
    OS = platform.system()
    networks = []

    if OS == "Windows":
        command = "netsh wlan show networks mode=Bssid"
    elif OS == "Linux":
        command = "sudo iwlist scan"
    else:
        print("Unsupported OS")
        return networks

    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            print("Error:", err.decode('utf-8').strip())
            return networks

        output = out.decode('utf-8').strip()

        if OS == "Windows":
            # Modified regex to capture SSID with spaces
            pattern = re.compile(r"SSID\s+\d+\s+:\s+(.*?)\s+.*?Signal\s+:\s+(\d+)%", re.DOTALL)
        elif OS == "Linux":
            pattern = re.compile(r"ESSID:\"(.*?)\".*?Signal level=(.*?) dBm", re.DOTALL)

        matches = pattern.findall(output)
        for ssid, strength in matches:
            networks.append((ssid.strip(), strength.strip()))
    
    except Exception as e:
        print(f"An error occurred: {e}")

    return networks

def connect_to_strongest_network(networks):
    if not networks:
        messagebox.showinfo("No Networks", "No networks found.")
        return
    strongest_network = max(networks, key=lambda x: int(x[1]))
    ssid = strongest_network[0]
    messagebox.showinfo("Connecting", f"Connecting to: {ssid} with signal strength {strongest_network[1]}%")

    OS = platform.system()

    if OS == "Windows":
        command = f'netsh wlan connect name="{ssid}"'
    elif OS == "Linux":
        command = f"nmcli dev wifi connect '{ssid}'"
    else:
        messagebox.showerror("Error", "Unsupported OS")

def refresh_networks():
    networks = scan_networks()
    network_list.delete(0, tk.END)
    if networks:
        for ssid, strength in networks:
            network_list.insert(tk.END, f"SSID: {ssid}, Signal Strength: {strength}%")
        connect_button.config(state=tk.NORMAL)
    else:
        network_list.insert(tk.END, "No networks found.")
        connect_button.config(state=tk.DISABLED)

def connect():
    networks = scan_networks()
    connect_to_strongest_network(networks)

root = tk.Tk()
root.title("Wi-Fi Network Scanner")

frame = tk.Frame(root)
frame.pack(pady=10)

network_list = tk.Listbox(frame, width=50, height=10)
network_list.pack()

refresh_button = tk.Button(frame, text="Refresh Networks", command=refresh_networks)
refresh_button.pack(pady=5)

connect_button = tk.Button(frame, text="Connect to Strongest Network", command=connect)
connect_button.pack(pady=5)
connect_button.config(state=tk.DISABLED)

root.mainloop()
