import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yaml

class GUI:
    def __init__(self, main_controller):
        with open("materials.yml", "r") as file:
            self.data = yaml.safe_load(file)

        self.main = main_controller
        self.canvas = None
        self.n2 = 1.46
        self.k2 = 0

        self.root = tb.Window(themename="superhero")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # When window is closed, run on_close before closing
        self.root.title("Ellipsometer Tool")
        self.root.geometry("900x500")

        self.frame_main = tk.Frame(self.root)
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center")

        self.frame_inputs_init(self.frame_main)
        self.frame_outputs = tk.Frame(self.frame_main)
        self.frame_outputs.grid(row=0, column=1, padx=10)
        self.frame_graph = tk.Frame(self.frame_outputs)
        self.frame_graph.pack()

        d, plot = self.main.ellipsometer.getThickness2(633, 47, 81)
        self.set_graph(plot)


        self.d_label = tk.Label(self.frame_outputs, text="Thickness(d): --")
        self.d_label.pack(pady=15)
        self.d_label.config(text="Thickness(d): "+str(d))

    def frame_material_init(self, parent_root):
        frame_material = tk.Frame(parent_root)
        frame_material.pack(pady=5, fill="x")
        frame_material.grid_columnconfigure(0, minsize=160)
        frame_material.grid_columnconfigure(1, weight=1)
        tk.Label(frame_material, text="Material").grid(row=0, column=0, sticky="w")

        self.material = tk.StringVar()
        self.material.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="material"))
        
        options = list(self.data["materials"].keys())

        combo_box = tb.Combobox(
            frame_material,
            textvariable=self.material,
            values=options,
            state="readonly",
            bootstyle="info",
        )

        combo_box.current(0)

        combo_box.grid(row=0,column=1, sticky="ew")

    def frame_wavelength_init(self, parent_root):
        frame_wavelength = tk.Frame(parent_root)
        frame_wavelength.pack(pady=5, fill="x")
        frame_wavelength.grid_columnconfigure(0, minsize=160)
        frame_wavelength.grid_columnconfigure(1, weight=1)
        tk.Label(frame_wavelength, text="Wavelength").grid(row=0, column=0, sticky="w")

        self.wavelength = tk.StringVar()
        self.wavelength.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="wavelength"))

        #wavelengths in nm
        combo_box = tb.Combobox(
            frame_wavelength,
            textvariable=self.wavelength,
            values=["633", "520", "650"],
            state="readonly",
            bootstyle="info"
        )

        combo_box.current(0)

        combo_box.grid(row=0,column=1, sticky="ew")

    def frame_aoi_init(self, parent_root):
        frame_aoi = tk.Frame(parent_root)
        frame_aoi.pack(pady=5)
        frame_aoi.grid_columnconfigure(0, minsize=160)
        frame_aoi.grid_columnconfigure(1, weight=1)

        tk.Label(frame_aoi, text="Angle of Incidence").grid(row=0, column=0, sticky="w")

        # Call on_change when AoI_Var is modified
        self.AoI_Var = tk.StringVar()
        self.AoI_Var.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="aoi"))

        
        vcmd = (self.root.register(self.validate_int), "%P")

        AoI = tb.Entry(frame_aoi, textvariable=self.AoI_Var, validate="key", validatecommand=vcmd, bootstyle="info")
        AoI.grid(row=0, column=1, sticky="ew")
        AoI.insert(0, 70)

    def frame_inputs_init(self, parent_root):
        self.frame_inputs = tk.Frame(parent_root)
        self.frame_inputs.grid(row=0, column=0, padx=10)

        tk.Label(self.frame_inputs, text="Film thickness range").pack()
        self.frame_range_init(self.frame_inputs)
        
        self.frame_material_init(self.frame_inputs)
        self.frame_wavelength_init(self.frame_inputs)
        self.frame_aoi_init(self.frame_inputs)

        self.frame_voltage = tk.Frame(self.frame_inputs)
        self.frame_voltage.pack(pady=15)
        tk.Label(self.frame_voltage, text="Voltage In:").grid(row=0, column=0)
        self.voltage_label = tk.Label(self.frame_voltage, text="--")
        self.voltage_label.grid(row=0, column=1)


        # Call init for alpha angle control buttons + labels
        self.frame_alpha_angles_init(self.frame_inputs)

        calculateBtn = tb.Button(
            self.frame_inputs, 
            text="Calculate", 
            width=10, 
            command=lambda: self.calculate(),
            bootstyle="success"
        )
        calculateBtn.pack(pady=15)

        # Start continuous voltage updates
        self.update_voltage()

    def frame_alpha_angles_init(self, parent_frame):
        frame_alpha_angles = tk.Frame(parent_frame)
        frame_alpha_angles.pack(pady=15)

        label0 = tk.Label(frame_alpha_angles, text="--")
        label0.grid(row=1, column=0)
        label45 = tk.Label(frame_alpha_angles, text="--")
        label45.grid(row=1, column=1)
        label90 = tk.Label(frame_alpha_angles, text="--")
        label90.grid(row=1, column=2)
        labelNeg45 = tk.Label(frame_alpha_angles, text="--")
        labelNeg45.grid(row=1, column=3)

        # IMPORTANT: use lambda so function is not called immediately
        button0 = tb.Button(
            frame_alpha_angles,
            text="0",
            width=5,
            bootstyle="info",
            command=lambda: self.set_voltage(0, label0)
        )
        button0.grid(row=0, column=0, padx=5)
        
        button45 = tb.Button( # 45 Degree Button
            frame_alpha_angles,
            text="45",
            width=5,
            bootstyle="info",
            command=lambda: self.set_voltage(1, label45)
        )
        button45.grid(row=0, column=1, padx=5)

        button90 = tb.Button(
            frame_alpha_angles,
            text="90",
            width=5,
            bootstyle="info",
            command=lambda: self.set_voltage(2, label90)
        )
        button90.grid(row=0, column=2, padx=5)

        buttonNeg45 = tb.Button(
            frame_alpha_angles,
            text="-45",
            width=5,
            bootstyle="info",
            command=lambda: self.set_voltage(3, labelNeg45)
        )
        buttonNeg45.grid(row=0, column=3, padx=5)
        
    def frame_range_init(self, parent_frame):
        frame_range = tk.Frame(parent_frame)
        frame_range.pack(pady=15)
        frame_range.grid_columnconfigure(0, minsize=160)
        frame_range.grid_columnconfigure(1, weight=1)
        
        tk.Label(frame_range, text="Max [Angstroms]").grid(row=0, column=0, sticky="w")
        tk.Label(frame_range, text="Min [Angstroms]").grid(row=1, column=0, sticky="w")

        # Call on_change when dMax_Var is modified
        self.dMax_Var = tk.StringVar()
        self.dMax_Var.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="max"))

        self.dMin_Var = tk.StringVar()
        self.dMin_Var.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="min")
        )
        
        vcmd = (self.root.register(self.validate_int), "%P")

        dMax = tb.Entry(frame_range, textvariable=self.dMax_Var, validate="key", validatecommand=vcmd, bootstyle="info")
        dMax.insert(0, 2000)
        dMin = tb.Entry(frame_range, textvariable=self.dMin_Var, validate="key", validatecommand=vcmd, bootstyle="info")
        dMin.insert(0, 0)
        

        dMax.grid(row=0, column=1, sticky="ew")
        dMin.grid(row=1, column=1, sticky="ew")

    def calculate(self):
        self.main.ellipsometer.setVoltage(self.main.voltage_measurements)
        d, plot = self.main.ellipsometer.getThickness()
        self.d_label.config(text="Thickness(d): "+str(d))
        self.set_graph(plot)
    
    def set_graph(self, plot):
        # Remove old canvas if it exists
        if self.canvas is not None:
            self.canvas.get_tk_widget().destroy()

        # Create new canvas
        self.canvas = FigureCanvasTkAgg(plot, master=self.frame_graph)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def set_voltage(self, index, label):
        voltage = self.main.get_v_max()

        label.config(text=str(round(voltage,3)))
        self.main.voltage_measurements[index] = voltage
        
    # Continuous voltage update
    def update_voltage(self):
        voltage = self.main.get_voltage()  # your stream source

        if voltage is not None:
            self.voltage_label.config(text=f"{voltage:.3f} V")

        # write to file every reading
        with open("voltage_data.txt", "a") as f:
            f.write(f"{voltage:.6f}\n")
            f.flush()

        self.root.after(100, self.update_voltage)

    def on_change(self, *args, param=None):
        ellipsometer = self.main.ellipsometer

        if param == "max": 
            value = self.dMax_Var.get()
            ellipsometer.dmax = int(value) if value else 0
        elif param == "min":
            value = self.dMin_Var.get()
            ellipsometer.dmin = int(value) if value else 0
        elif param == "wavelength":
            value = self.wavelength.get()
            ellipsometer.wavelength = float(value) if value else 0
        elif param == "material":
            value = self.material.get()
            material = self.data["materials"].get(value)
            if material is None: return
            wave = ellipsometer.getWavelength()
            mat_wave = material[wave]
            mat_n = mat_wave["n"]
            mat_k = mat_wave["k"]
            print(mat_n, mat_k)
            ellipsometer.setSampleConstants(mat_n, mat_k)
        elif param == "aoi":
            value = self.AoI_Var.get()
            ellipsometer.setSampleAoI(int(value)) if value else 70
        else:
            print("Invalid Param")

        ellipsometer.printVals()

    def run(self):
        self.root.mainloop()

    def on_close(self):
        self.main.cleanup()
        self.root.destroy()

    def validate_float(self, value):
        if value == "":
            return True  # allow empty while typing
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_int(self, value):
        return value.isdigit() or value == ""