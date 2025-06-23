import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
from ttkbootstrap import Style
from sat import getSat



def show_selected_item(lati, long):
    selected_item = combo_box.get()
    
    if selected_item:
	    satsep = selected_item.replace(" ", "").split(":")
	    satId = int(satsep[1])
	    satName = str(satsep[0])
	    satdata = getSat(satId, latitude=lati, longitude=long, external=True)
	    lct = satdata[0]
	    satinfo = satdata[1]
	    elv = satdata[2]
	    ts = satdata[3]
	    sname = satinfo[1]
	    combo_box.set(selected_item)
	    lat, lon = lct.get("Latitude"), lct.get("Longitude")
	    rEl, mEl, sEl = elv.get("RiseEl"), elv.get("MaxEl"), elv.get("SetEl")
	    rTs, cTs, sTs = ts.get("RiseT"), ts.get("CulmT"), ts.get("SetT")
	    mode, uLink, dLink, altN = satinfo[2], satinfo[3], satinfo[4], satinfo[5]
	    
	    #messagebox.showinfo("Selection", f"You selected: {selected_item}")
	    #text_area.insert(tk.INSERT, "  " + "="*32)
	    text_area.insert(tk.INSERT, f"  Name: {sname}")
	    text_area.insert(tk.INSERT, f"\n  Alt. name: {altN}")
	    text_area.insert(tk.INSERT, f"\n  NORAD: {satsep[1]}\n")
	    text_area.insert(tk.INSERT, f"  Lat: {lat} | Lon: {lon}\n  Up: {uLink} - Down: {dLink}\n  Mode: {mode}\n\n")
	    text_area.insert(tk.INSERT, f"  ____________ Next Pass ____________" + "\n\n")
	    text_area.insert(tk.INSERT, f" ● Rise\n  | Elevation: {rEl}°\n  | When: {rTs}\n\n")
	    text_area.insert(tk.INSERT, f" ● Max\n  | Elevation: {mEl}°\n  | When: {cTs}\n\n")
	    text_area.insert(tk.INSERT, f" ● Set\n  | Elevation: {sEl}°\n  | When: {sTs}")
	    #text_area.insert(tk.END, "  " + "="*32)
	    #text_area.config(state=tk.DISABLED)
	    
def buttonClick():
    if lat_entry.get() == "" or long_entry.get() == "":
        messagebox.showinfo("Coordinates", f"You have to enter coordinates.")
    elif combo_box.get() == "Select a Satellite":
        messagebox.showinfo("Satellite selection", f"Please select a satellite.")
    else:
        text_area.config(state=tk.NORMAL)
        text_area.delete('1.0', tk.END)
        lat = lat_entry.get()
        lon = long_entry.get()
        show_selected_item(lati=lat, long=lon)

# Create the main application window
root = Tk()
img = PhotoImage(file='images/icon.png')
root.iconphoto(False, img)
root.title("SatTracker")
root.resizable(False, False)
root.geometry("340x600")
font = Font(family="Arial", size=20)
root.option_add("*TCombobox*Listbox*Font", font)
style = Style(theme='darkly')


# === LAT/LONG ENTRY FIELDS ===
entry_frame = ttk.Frame(root)
entry_frame.pack(pady=8, padx=10, fill='x')

lat_label = ttk.Label(entry_frame, text="Latitude")
lat_label.grid(row=0, column=0, sticky='w', padx=2)
lat_entry = ttk.Entry(entry_frame)
lat_entry.grid(row=1, column=0, padx=2)

long_label = ttk.Label(entry_frame, text="Longitude")
long_label.grid(row=0, column=1, sticky='w', padx=8)
long_entry = ttk.Entry(entry_frame)
long_entry.grid(row=1, column=1, padx=8)

# === SATELLITE DROPDOWN ===
combo_box = ttk.Combobox(root, values=[
    "Diwata-2B: 43678",
    "Duchifat-1: 40021",
    "EYESAT-1: 22825",
    "Fox-1B: 43017",
    "Int.SpSt: 25544",
    "LilacSat-2: 40908",
    "ProCommSAT: 26931",
    "SaudiSat-1C: 27607"
], width=20, font=("Arial", 18), state="readonly")
combo_box.set("Select a Satellite")
combo_box.pack(pady=5, padx=8, fill=BOTH)

# === OUTPUT TEXT BOX ===
text_area = tk.Text(root, width=34, height=22, font=("Arial", 12), state=tk.DISABLED)
text_area.pack(padx=2, pady=10)

submitbutton = tk.Button(root, text="Lookup Satellite", command=buttonClick, font=("Arial", 12))
submitbutton.pack(padx=8, pady=5, fill=BOTH)

# Run the Tkinter event loop
root.mainloop()

area = tk.Text(root, width=34, height=22, font=("Arial", 12), state=tk.DISABLED)
text_area.pack(padx=2, pady=10)

submitbutton = tk.Button(root, text="Lookup Satellite", command=buttonClick, font=("Arial", 12))
submitbutton.pack(padx=8, pady=5, fill=BOTH)

# Run the Tkinter event loop
root.mainloop()