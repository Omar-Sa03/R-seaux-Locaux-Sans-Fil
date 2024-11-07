import subprocess
import re
import time
import platform
import matplotlib.pyplot as plt

#----Question 2.1-----

def get_signal_strength():
    if platform.system() == 'Windows':
        p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.read().decode('utf-8').strip()
        p.communicate()
        signal_data = re.findall('SSID .*?\n.*?\n.*?Signal .*? : ([0-9]*)%', out, re.DOTALL)
        if signal_data:
            signal_strength = signal_data[0]
            return int(signal_strength)  

def display_signal_strength(interval=2):
    print("Displaying Wi-Fi signal strength. Press Ctrl+C to stop.")
    try:
        while True:
            signal_strength = get_signal_strength()
            if signal_strength is not None:
                print(f"Current Signal Strength: {signal_strength}%")
            else:
                print("Unable to retrieve signal strength.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")

#----Question 2.2-----

def plot_signal_strength(interval=0.5, duration=60):

    plt.ion()  
    fig, ax = plt.subplots()
    ax.set_title("Wi-Fi Signal Strength ")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Signal Strength (%)")
    
    signal_strengths = [] 
    times = [] 

    start_time = time.time() 
    print("Collecting Wi-Fi signal strength data for plotting. Press Ctrl+C to stop.")

    try:
        while True:
            signal_strength = get_signal_strength()
            if signal_strength is not None:
                current_time = time.time() - start_time 
                signal_strengths.append(signal_strength)
                times.append(current_time)
                ax.clear()  
                ax.plot(times, signal_strengths, label='Signal Strength', color='b', marker='.')
                ax.set_title("Wi-Fi Signal Strength")
                ax.set_xlabel("Time (seconds)")
                ax.set_ylabel("Signal Strength (%)")
                ax.set_ylim(0, 100)  
                ax.legend()
                plt.pause(interval)  
            else:
                print("Unable to retrieve signal strength.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        plt.ioff()  
        plt.show() 

plot_signal_strength()
#display_signal_strength()
