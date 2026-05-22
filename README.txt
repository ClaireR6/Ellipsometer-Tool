Companion tool to the low-cost Ellipsometer. 

Key Features:
* User input fields for material selection, thickness range, angle of incidence, and wavelength. 
* Direct light sensor readings via light_sensor.py
* Automatic Psi and Delta calculation with resulting model-fitted thickness and accompanying graph.
* materials.yml containing presets for common materials at 520, 633, and 650 nm wavelengths.

Dependencies: 
* Python ver 3.13.12
* labquest for light_sensor.py
* ttkbootstrap for gui.py

Installation: 
1. Open cmd prompt and navigated to desired folder.
2. In the cmd prompt run:
    git clone https://github.com/ClaireR6/Ellipsometer-Tool.git
    cd Ellipsometer-Tool
* (Recommended) Create virtual environment to house dependencies with:
    python -m venv venv
    and activate the environment:
    .\venv\Scripts\activate
3. Install Dependencies: 
    python -m pip install -r requirements.txt
4. Run python main.py
