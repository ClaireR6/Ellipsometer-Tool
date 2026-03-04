import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self, main_controller):
        self.main = main_controller

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close) # When window is closed, run on_close before closing
        self.root.title("Ellipsometer Tool")
        self.root.geometry("900x500")


        self.frame_inputs = tk.Frame(self.root)
        self.frame_outputs = tk.Frame(self.root)
        self.frame_inputs.grid(row=0, column=0, padx=10)
        self.frame_outputs.grid(row=0, column=1, padx=10)


        # frame_inputs items
        tk.Label(self.frame_inputs, text="Film thickness range").pack()
        frame_range = tk.Frame(self.frame_inputs)
        frame_range.pack(pady=15)

        tk.Label(frame_range, text="Max [Angstroms]").grid(row=0, column=0)
        tk.Label(frame_range, text="Min [Angstroms]").grid(row=1, column=0)

        frame_wavelength = tk.Frame(self.frame_inputs)
        frame_wavelength.pack(pady=15)
        tk.Label(frame_wavelength, text="Wavelength").grid(row=0, column=0)

        dMax = tk.Entry(frame_range)
        dMax.insert(0, 1000)
        dMin = tk.Entry(frame_range)
        dMin.insert(0, 0)
        wavelength = tk.Entry(frame_wavelength)
        wavelength.insert(0, 632.8)

        dMax.grid(row=0, column=1)
        dMin.grid(row=1, column=1)
        wavelength.grid(row=0, column=1)

        self.frame_i = tk.Frame(self.frame_inputs)
        self.frame_i.pack(pady=15)
        tk.Label(self.frame_i, text="Voltage In:").grid(row=0, column=0)
        self.voltage_label = tk.Label(self.frame_i, text="--")
        self.voltage_label.grid(row=0, column=1)

        frame_alpha_angles = tk.Frame(self.frame_inputs)
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

        # Start continuous voltage updates
        self.update_voltage()

        calculateBtn = tk.Button(text="Calculate d", width=10, command=lamda: self.calculate())


        # frame_outputs items

    def calculate(self):
        
    
    def set_graph(self, plot):
        canvas = FigureCanvasTkAgg(plot, master=self.frame_outputs)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def set_voltage(self, index, label):
        voltage = self.main.get_voltage()

        if voltage is None:
            voltage = 100

        label.config(text=str(voltage))
        self.main.voltage_measurements[index] = voltage
        self.main.ellipsometer.setIntensity(self.main.voltage_measurements)
        
    # Continuous voltage update
    def update_voltage(self):
        voltage = self.main.get_voltage()  # your stream source

        if voltage is not None:
            self.voltage_label.config(text=f"{voltage:.3f} V")

        self.root.after(100, self.update_voltage)

    def run(self):
        self.root.mainloop()

    def on_close(self):
        self.main.cleanup()
        self.root.destroy()
