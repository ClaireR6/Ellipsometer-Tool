import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self, main_controller):
        self.main = main_controller
        self.canvas = None

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # When window is closed, run on_close before closing
        self.root.title("Ellipsometer Tool")
        self.root.geometry("900x500")

        self.frame_inputs_init(self.root)
        self.frame_outputs = tk.Frame(self.root)
        self.frame_outputs.grid(row=0, column=1, padx=10)
        self.frame_graph = tk.Frame(self.frame_outputs)
        self.frame_graph.pack()

        d, plot = self.main.ellipsometer.getThickness2(633, 47, 81)
        self.set_graph(plot)


        self.d_label = tk.Label(self.frame_outputs, text="Thickness(d): --")
        self.d_label.pack(pady=15)
        self.d_label.config(text="Thickness(d): "+str(d))
        
    def frame_wavelength_init(self, parent_root):
        frame_wavelength = tk.Frame(parent_root)
        frame_wavelength.pack(pady=15)
        tk.Label(frame_wavelength, text="Wavelength").grid(row=0, column=0)

        self.wavelength = tk.StringVar()
        self.wavelength.trace_add(
            "write", 
            lambda *args: self.on_change(*args, param="wavelength"))

        #wavelengths in nm
        combo_box = ttk.Combobox(
            frame_wavelength,
            textvariable=self.wavelength,
            values=["650", "520", "633"],
            state="readonly"
        )

        combo_box.current(0)

        combo_box.grid(row=0,column=1)

    def frame_inputs_init(self, parent_root):
        self.frame_inputs = tk.Frame(parent_root)
        self.frame_inputs.grid(row=0, column=0, padx=10)

        tk.Label(self.frame_inputs, text="Film thickness range").pack()

        self.frame_range_init(self.frame_inputs)

        self.frame_wavelength_init(self.frame_inputs)

        self.frame_voltage = tk.Frame(self.frame_inputs)
        self.frame_voltage.pack(pady=15)
        tk.Label(self.frame_voltage, text="Voltage In:").grid(row=0, column=0)
        self.voltage_label = tk.Label(self.frame_voltage, text="--")
        self.voltage_label.grid(row=0, column=1)


        # Call init for alpha angle control buttons + labels
        self.frame_alpha_angles_init(self.frame_inputs)

        calculateBtn = tk.Button(
            self.frame_inputs, 
            text="Calculate d", 
            width=10, 
            command=lambda: self.calculate()
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
        button0 = tk.Button(
            frame_alpha_angles,
            text="0",
            width=10,
            command=lambda: self.set_voltage(0, label0)
        )
        button0.grid(row=0, column=0, padx=5)
        
        button45 = tk.Button( # 45 Degree Button
            frame_alpha_angles,
            text="45",
            width=10,
            command=lambda: self.set_voltage(1, label45)
        )
        button45.grid(row=0, column=1, padx=5)

        button90 = tk.Button(
            frame_alpha_angles,
            text="90",
            width=10,
            command=lambda: self.set_voltage(2, label90)
        )
        button90.grid(row=0, column=2, padx=5)

        buttonNeg45 = tk.Button(
            frame_alpha_angles,
            text="-45",
            width=10,
            command=lambda: self.set_voltage(3, labelNeg45)
        )
        buttonNeg45.grid(row=0, column=3, padx=5)
        
    def frame_range_init(self, parent_frame):
        frame_range = tk.Frame(parent_frame)
        frame_range.pack(pady=15)

        tk.Label(frame_range, text="Max [Angstroms]").grid(row=0, column=0)
        tk.Label(frame_range, text="Min [Angstroms]").grid(row=1, column=0)

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

        dMax = tk.Entry(frame_range, textvariable=self.dMax_Var, validate="key", validatecommand=vcmd)
        dMax.insert(0, 2000)
        dMin = tk.Entry(frame_range, textvariable=self.dMin_Var, validate="key", validatecommand=vcmd)
        dMin.insert(0, 0)
        

        dMax.grid(row=0, column=1)
        dMin.grid(row=1, column=1)

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
        voltage = self.main.get_voltage()

        label.config(text=str(voltage))
        self.main.voltage_measurements[index] = voltage
        
    # Continuous voltage update
    def update_voltage(self):
        voltage = self.main.get_voltage()  # your stream source

        if voltage is not None:
            self.voltage_label.config(text=f"{voltage:.3f} V")

        self.root.after(100, self.update_voltage)

    def on_change(self, *args, param=None):
        if param == "max": 
            value = self.dMax_Var.get()
            self.main.ellipsometer.dmax = int(value) if value else 0
        elif param == "min":
            value = self.dMin_Var.get()
            self.main.ellipsometer.dmin = int(value) if value else 0
        elif param == "wavelength":
            value = self.wavelength.get()
            self.main.ellipsometer.wavelength = float(value) if value else 0
        else:
            print("Invalid Param")

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