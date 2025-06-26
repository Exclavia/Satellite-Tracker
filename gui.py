import tkinter as tk
from tkinter import ttk, BOTH, messagebox
from tkinter.font import Font

# from ttkbootstrap import Style # Uncomment to use dark theme.
from data.Sat_Info import import_data
from sat import get_sat

# Grabbing satellite info from data/satinfo.txt
sat_nfo = import_data()
sat_options = []
# Adds to list for combo box options
for grab_sat in sat_nfo:
    name_sat = grab_sat.get("Name")
    norad_num = grab_sat.get("NORAD")
    sat_full = f"{name_sat}: {norad_num}"
    sat_options.append(sat_full)

# Calls getSat function and displays returned data
def show_selected_item(lati, long):
    selected_item = combo_box.get()
    i_lat, i_lon = float(lati), float(long)
    if selected_item:
        sat_sep = selected_item.replace(" ", "").split(":")
        sat_id = int(sat_sep[1])
        # Main sat.py function call - external set to True since it's imported
        sat_data = get_sat(sat_id, latitude=i_lat, longitude=i_lon, external=True)
        # Parsing getSat list data into own variables
        sat_info = sat_data[1]
        elv_data = sat_data[2]
        ts_data = sat_data[3]
        sat_name = sat_sep[0]
        combo_box.set(selected_item)

        # Setting variables from getSat
        u_lat, u_lon = i_lat, i_lon
        r_el, = elv_data.get("RiseE")
        m_el = elv_data.get("MaxE")
        s_el = elv_data.get("SetE")
        r_ts = ts_data.get("RiseT")
        c_ts = ts_data.get("CulmT")
        s_ts = ts_data.get("SetT")
        mode, u_link, d_link = sat_info[2], sat_info[3], sat_info[4]

        # Displayed Info ================
        text_area.insert(tk.INSERT, f"  Name: {sat_name}")
        text_area.insert(tk.INSERT, f"\n  NORAD: {sat_sep[1]}\n")
        text_area.insert(
            tk.INSERT,
            f"  Lat: {u_lat} | Lon: {u_lon}\n  Up: {u_link} - Down: {d_link}\n  Mode: {mode}\n\n",
        )
        text_area.insert(tk.INSERT, "____________ Next Pass ___________" + "\n\n")
        text_area.insert(
            tk.INSERT, f" ● Rise\n  | Elevation: {r_el}°\n  | When: {r_ts}\n\n"
        )
        text_area.insert(
            tk.INSERT, f" ● Max\n  | Elevation: {m_el}°\n  | When: {c_ts}\n\n"
        )
        text_area.insert(tk.INSERT, f" ● Set\n  | Elevation: {s_el}°\n  | When: {s_ts}")
        text_area.config(state=tk.DISABLED)


# Button command function
def button_click():
    # Check if Lat/Lon is entered & if Satellite is selected
    if lat_entry.get() == "" or long_entry.get() == "":
        messagebox.showinfo("Coordinates", "You have to enter coordinates.")
    elif combo_box.get() == "Select a Satellite":
        messagebox.showinfo("Satellite selection", "Please select a satellite.")
    else:
        text_area.config(state=tk.NORMAL)
        text_area.delete("1.0", tk.END)
        e_lat = lat_entry.get()
        e_lon = long_entry.get()
        show_selected_item(lati=e_lat, long=e_lon)


# Create the main application window
root = tk.Tk()
img = tk.PhotoImage(file="images/icon.png")
root.iconphoto(False, img)
root.title("SatTracker")
root.resizable(False, False)
root.geometry("340x600")
font = Font(family="Arial", size=20)
root.option_add("*TCombobox*Listbox*Font", font)
# style = Style(theme='darkly') # Uncomment to enable dark theme.


# === LAT/LONG ENTRY FIELDS ===
entry_frame = ttk.Frame(root)
entry_frame.pack(pady=8, padx=10, fill="x")

lat_label = ttk.Label(entry_frame, text="Latitude")
lat_label.grid(row=0, column=0, sticky="w", padx=2)
lat_entry = ttk.Entry(entry_frame)
lat_entry.grid(row=1, column=0, padx=2)

long_label = ttk.Label(entry_frame, text="Longitude")
long_label.grid(row=0, column=1, sticky="w", padx=8)
long_entry = ttk.Entry(entry_frame)
long_entry.grid(row=1, column=1, padx=8)

# === SATELLITE DROPDOWN ===
combo_box = ttk.Combobox(
    root, values=sat_options, width=20, font=("Arial", 18), state="readonly"
)
combo_box.set("Select a Satellite")
combo_box.pack(pady=5, padx=8, fill=BOTH)

# === OUTPUT TEXT BOX ===
text_area = tk.Text(root, width=34, height=22, font=("Arial", 12), state=tk.DISABLED)
text_area.pack(padx=2, pady=10)

submitbutton = tk.Button(
    root, text="Lookup Satellite", command=button_click, font=("Arial", 12)
)
submitbutton.pack(padx=8, pady=5, fill=BOTH)
# Run the Tkinter event loop
root.mainloop()
