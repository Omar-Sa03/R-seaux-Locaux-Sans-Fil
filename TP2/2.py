import platform
import subprocess
import re
import tkinter as tk
from tkinter import messagebox

def scan_networks():
    networks = []
    if platform.system() == "Windows":
        command = "netsh wlan show networks mode=Bssid"
    elif platform.system() == "Linux":
        command = "sudo iwlist scan"
    else:
        print("Unsupported OS")
        return networks
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            messagebox.showerror("Error", err.decode('utf-8').strip())
            return networks

        output = out.decode('utf-8').strip()
        
        if platform.system() == "Windows":
            
            pattern = re.compile(r"SSID\s+\d+\s+:\s+(.*?)\s+.*?Signal\s+:\s+(\d+)%", re.DOTALL)
        elif platform.system() == "Linux":
            
            pattern = re.compile(r"ESSID:\"(.*?)\".*?Signal level=(.*?) dBm", re.DOTALL)

        matches = pattern.findall(output)
        for ssid, strength in matches:
            networks.append((ssid.strip(), strength.strip()))
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    
    return networks

def display_networks():
    networks = scan_networks()
    listbox.delete(0, tk.END)  
    if networks:
        for ssid, strength in networks:
            listbox.insert(tk.END, f"SSID: {ssid}, Signal Strength: {strength}%")
    else:
        listbox.insert(tk.END, "No networks found.")

root = tk.Tk()
root.title("Wi-Fi Network Scanner")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Available Wi-Fi Networks:")
label.pack()

listbox = tk.Listbox(frame, width=50, height=10)
listbox.pack()

scan_button = tk.Button(frame, text="Scan Networks", command=display_networks)
scan_button.pack(pady=10)

root.mainloop()

    
