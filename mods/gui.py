import tkinter as tk
from tkinter import ttk, messagebox, BOTH, PhotoImage
from ttkbootstrap import Style # Uncomment to use dark theme.
from tkinter.font import Font
from mods.get_sat import get_sat
from mods.import_sat import import_satellites


def start_gui():
    """Main GUI function"""
    # Grabbing satellite info from data/satinfo.txt
    sat_import = import_satellites()
    sat_options = []
    # Adds to list for combo box options
    for info_sat in sat_import:
        info_name = info_sat.get("Name")
        info_norad = info_sat.get("NORAD")
        info_con = f"{info_name}: {info_norad}"
        sat_options.append(info_con)


    def show_selected_item(in_lat, in_lon, min_elev):
        """Calls getSat function and displays returned data"""
        selected_item = combo_box.get()
        if selected_item:
            sat_sep = selected_item.replace(" ", "").split(":")
            sat_id = int(sat_sep[1])
            sat_data = get_sat(sat_id, usr_lat=in_lat, usr_lon=in_lon, usr_minalt=min_elev)
            # Parsing getSat list data into own variables
            sat_name = sat_sep[0]
            rise_data = sat_data[1]
            culm_data = sat_data[2]
            set_data = sat_data[3]
            more_info = sat_data[4]
            combo_box.set(selected_item)
            # Setting variables from getSat
            d_lat, d_lon = float(in_lat), float(in_lon)
            r_el, m_el, s_el = rise_data.get("Elev"), culm_data.get("Elev"), set_data.get("Elev")
            r_dx, c_dx, s_dx = rise_data.get("Distance"), culm_data.get("Distance"), set_data.get("Distance")
            r_dt, c_dt, s_dt = rise_data.get("When"), culm_data.get("When"), set_data.get("When")
            u_link, d_link, mode = more_info.get("Uplink"), more_info.get("Downlink"), more_info.get("Mode")
            # Displayed Info ================
            text_area.insert(tk.INSERT, f"  Name: {sat_name}")
            text_area.insert(tk.INSERT, f"\n  NORAD: {sat_id}\n")
            text_area.insert(tk.INSERT, f"  Lat: {d_lat} | Lon: {d_lon}\n")
            text_area.insert(tk.INSERT, f"  Up: {u_link}  |  Down: {d_link}\n")
            text_area.insert(tk.INSERT, f"  Mode: {mode}\n")
            text_area.insert(tk.INSERT, "____________ Next Pass ___________" + "\n\n")
            text_area.insert(tk.INSERT, f" ● Rise\n  | Elevation: {r_el}\n  | Distance: {r_dx}\n  | When: {r_dt}\n\n")
            text_area.insert(tk.INSERT, f" ● Max\n  | Elevation: {m_el}\n  | Distance: {c_dx}\n  | When: {c_dt}\n\n")
            text_area.insert(tk.INSERT, f" ● Set\n  | Elevation: {s_el}\n  | Distance: {s_dx}\n  | When: {s_dt}")
            text_area.config(state=tk.DISABLED)


    def button_click():
        """Button command function"""
        # Check if Lat/Lon is entered & if Satellite is selected
        if lat_entry.get() == "" or long_entry.get() == "":
            messagebox.showinfo("Coordinates", "You have to enter coordinates.")
        elif combo_box.get() == "Select a Satellite":
            messagebox.showinfo("Satellite selection", "Please select a satellite.")
        elif elev_entry.get() == "":
            messagebox.showinfo("Minimum Elevation", "Please enter a minimum elevation.")
        else:
            text_area.config(state=tk.NORMAL)
            text_area.delete('1.0', tk.END)
            e_lat = lat_entry.get()
            e_lon = long_entry.get()
            e_ele = elev_entry.get()
            show_selected_item(in_lat=e_lat, in_lon=e_lon, min_elev=e_ele)

    # Create the main application window
    root = tk.Tk()
    img = PhotoImage(file='images/icon.png')
    root.iconphoto(False, img)
    root.title("Satellite Tracker")
    root.resizable(False, False)
    root.geometry("360x650")
    font = Font(family="Arial", size=20)
    root.option_add("*TCombobox*Listbox*Font", font)
    Style(theme='darkly') # Enables dark theme

    # === LAT/LONG/MIN.ELEV ENTRY FIELDS ===
    entry_frame = ttk.Frame(root)
    entry_frame.pack(pady=8, padx=10, fill='x')
    # Lat
    lat_label = ttk.Label(entry_frame, text="Latitude")
    lat_label.grid(row=0, column=0, sticky='w', padx=8)
    lat_entry = ttk.Entry(entry_frame, width=35)
    lat_entry.grid(row=1, column=0, padx=8)
    # Lon
    long_label = ttk.Label(entry_frame, text="Longitude")
    long_label.grid(row=2, column=0, sticky='w', padx=8)
    long_entry = ttk.Entry(entry_frame, width=35)
    long_entry.grid(row=3, column=0, padx=8)
    # Min. Elevation
    elev_label = ttk.Label(entry_frame, text="Min Elevation")
    elev_label.grid(row=1, column=1, sticky='w', padx=8)
    elev_entry = ttk.Entry(entry_frame, width=10)
    elev_entry.grid(row=2, column=1, padx=8)
    elev_entry.insert(tk.INSERT, "20.0")

    # === SATELLITE DROPDOWN ===
    combo_box = ttk.Combobox(root, values=sat_options, width=20, font=("Arial", 18), state="readonly")
    combo_box.set("Select a Satellite")
    combo_box.pack(pady=5, padx=8, fill=BOTH)

    # === OUTPUT TEXT BOX ===
    text_area = tk.Text(root, width=36, height=22, font=("Arial", 12), state=tk.DISABLED)
    text_area.pack(padx=2, pady=10)
    submitbutton = tk.Button(root, text="Lookup Satellite", command=button_click, font=("Arial", 12))
    submitbutton.pack(padx=8, pady=5, fill=BOTH)

    # Run the Tkinter event loop
    root.mainloop()
