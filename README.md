# Physics Simulation Playground

An interactive physics simulation web app built using Python and Streamlit.  
The goal of this project is to make complex physics concepts intuitive through visualization and animation.

## Features

- Interactive simulations across multiple domains of physics
- Real-time parameter control using sliders
- Animated visualizations using Plotly
- Downloadable graphs (PNG)
- Automatically generated PDF reports for each simulation
- Clean and consistent user interface

## Simulations Included

### Mechanics
- Projectile Motion (with animation and comparison)

### Electromagnetism
- Lorentz Force (charged particle motion)

### Relativity
- Time Dilation
- Twin Paradox

### Thermodynamics
- Carnot Engine (P–V cycle with efficiency visualization)

### Signals and Waves
- Fourier Series (square, sawtooth, and triangle wave approximation)

## Tech Stack

- Python
- Streamlit
- NumPy
- Plotly
- Matplotlib
- ReportLab

## How to Run Locally

1. Clone the repository:
   git clone ([https://soumyasengupta2005-rgb.github.io/Physics_Simulator_Lab/](https://github.com/soumyasengupta2005-rgb/Physics_Simulator_Lab.git))
   cd Physics_Simulator_Lab

2. Create a virtual environment:
   python -m venv venv

3. Activate the environment:
   Windows:
   venv\Scripts\activate

   Mac/Linux:
   source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run the app:
   streamlit run Home.py

## Project Structure

.
├── Home.py
├── styles.css
├── requirements.txt
├── pages/
│   ├── projectile.py
│   ├── lorentz.py
│   ├── carnot_engine.py
│   ├── relativity_time.py
│   ├── relativity_twin.py
│   ├── fourier_series.py

## Motivation

Physics is often taught in a highly abstract way.  
This project aims to bridge that gap by turning equations into interactive experiences.

## Future Improvements

- Additional simulations (optics, quantum systems, wave interference)
- Improved animations and visual effects
- User-driven input and custom scenarios
- Performance optimizations

## Author

Soumya Sengupta  
Physics student and developer interested in building interactive scientific tools.

## License

This project is open-source and available under the MIT License.
