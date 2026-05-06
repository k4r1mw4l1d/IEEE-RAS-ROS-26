import tkinter as tk
from tkinter import messagebox, ttk
from models import Drone, Package, Fleet
from navigation import navigator
from mission import Mission
from simulation import Simulation

class DroneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AeroPath Pro v2")
        self.root.geometry("500x950")
        
        self.nav = navigator()
        self.fleet = Fleet()
        self.fleet.load_from_json()
        self.setup_ui()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="System Ready", fg="blue", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=10)

        # Fleet Frame
        ff = tk.LabelFrame(self.root, text="Drone Fleet Management", padx=10, pady=10)
        ff.pack(fill="x", padx=20)
        self.drone_selector = ttk.Combobox(ff, state="readonly")
        self.drone_selector.pack(fill="x", pady=5)
        self.drone_selector.bind("<<ComboboxSelected>>", self.on_drone_selected)

        tk.Label(ff, text="ID:").pack(side="left")
        self.new_id = tk.Entry(ff, width=8); self.new_id.pack(side="left", padx=2)
        tk.Label(ff, text="Cap:").pack(side="left")
        self.new_cap = tk.Entry(ff, width=4); self.new_cap.pack(side="left", padx=2)
        tk.Button(ff, text="Add", command=self.add_drone, bg="green", fg="white").pack(side="left", padx=2)
        tk.Button(ff, text="Del", command=self.delete_drone, bg="red", fg="white").pack(side="left", padx=2)

        # Mission Frame
        mf = tk.LabelFrame(self.root, text="Mission Planning", padx=10, pady=10)
        mf.pack(fill="x", padx=20, pady=10)
        tk.Label(mf, text="Weight (kg):").grid(row=0, column=0)
        self.weight = tk.Entry(mf, width=5); self.weight.insert(0, "2"); self.weight.grid(row=0, column=1)
        tk.Label(mf, text="Dest X,Y:").grid(row=0, column=2)
        self.dest_x = tk.Entry(mf, width=4); self.dest_x.insert(0, "6"); self.dest_x.grid(row=0, column=3)
        self.dest_y = tk.Entry(mf, width=4); self.dest_y.insert(0, "6"); self.dest_y.grid(row=0, column=4)

        # Zone Frame
        zf = tk.LabelFrame(self.root, text="No-Fly Zone Management", padx=10, pady=10)
        zf.pack(fill="x", padx=20)
        self.zone_entry = tk.Entry(zf); self.zone_entry.insert(0, "2,4,2,4"); self.zone_entry.pack(fill="x")
        tk.Button(zf, text="Register Zone", command=self.add_zone).pack(fill="x", pady=2)
        self.zone_box = tk.Listbox(zf, height=4); self.zone_box.pack(fill="x")
        tk.Button(zf, text="Delete Selected", command=self.del_zone).pack(fill="x")

        tk.Button(self.root, text="LAUNCH SIMULATION", command=self.run_sim, bg="#2196F3", fg="white", height=2).pack(pady=20, fill="x", padx=20)
        self.update_drone_dropdown()

    def add_drone(self):
        try:
            self.fleet.drones.append(Drone(self.new_id.get(), capacity=float(self.new_cap.get())))
            self.fleet.save_to_json(); self.update_drone_dropdown()
        except: messagebox.showerror("Error", "Invalid Drone Data")

    def delete_drone(self):
        self.fleet.drones = [d for d in self.fleet.drones if d.drone_id != self.drone_selector.get()]
        self.fleet.save_to_json(); self.update_drone_dropdown()

    def add_zone(self):
        try:
            c = [int(x.strip()) for x in self.zone_entry.get().split(",")]
            self.nav.add_zone_rectangle(c[0], c[1], c[2], c[3])
            self.update_zone_list()
        except: messagebox.showerror("Error", "Format: x1,x2,y1,y2")

    def del_zone(self):
        sel = self.zone_box.curselection()
        if sel: self.nav.remove_zone(sel[0]); self.update_zone_list()

    def update_zone_list(self):
        self.zone_box.delete(0, tk.END)
        for z in self.nav.zones: self.zone_box.insert(tk.END, z["label"])

    def update_drone_dropdown(self):
        ids = [d.drone_id for d in self.fleet.drones]
        self.drone_selector['values'] = ids
        if ids: self.drone_selector.current(0); self.on_drone_selected(None)

    def on_drone_selected(self, e):
        selected_id = self.drone_selector.get()
        for d in self.fleet.drones:
            if d.drone_id == selected_id:
                self.cur_drone = d
                # Updated label to show both Battery and Capacity
                self.status_label.config(
                    text=f"ID: {d.drone_id} | Battery: {d.battery:.1f}% | Capacity: {d.capacity}kg",
                    fg="blue"
                )

    def run_sim(self):
        try:
            dest = [int(self.dest_x.get()), int(self.dest_y.get())]
            package = Package(float(self.weight.get()), dest)
            mission = Mission(self.cur_drone, package, self.nav)
            mission.path = self.nav.get_path(self.cur_drone.position, dest)
            
            if mission.path and mission.prepare():
                Simulation(mission).run()
                self.cur_drone.battery = 100.0 # Reset battery for repeat testing
                self.cur_drone.position = [0, 0]
                self.on_drone_selected(None)
                self.fleet.save_to_json()
            else: messagebox.showerror("Error", "No path found! Target might be blocked.")
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk(); app = DroneGUI(root); root.mainloop()