from neuron import h 
from neuron.units import mV, ms
import matplotlib.pyplot as plt

# Define the maximum conductances for sodium and potassium
gNaBar = 0.12
gKBar=0.036

# Create a soma section
soma = h.Section(name='soma')
soma.L = 20  # Length of the soma
soma.diam = 20  # Diameter of the soma
soma.Ra = 123  # Axial resistance
soma.nseg = 1  # Number of segments

# Insert Hodgkin-Huxley channels
soma.insert('hh')
soma.gnabar_hh = gNaBar  # Sodium conductance
soma.gkbar_hh = gKBar  # Potassium conductance

# Initial and holding voltages
v_init = -65
Vhold = 10

# Set up a voltage clamp
vc = h.SEClamp(0.5)
vc.dur1 = 2  # Duration of the first phase
vc.amp1 = v_init  # Amplitude of the first phase
vc.dur2 = 10  # Duration of the second phase
vc.amp2 = Vhold  # Amplitude of the second phase
vc.dur3 = 8  # Duration of the third phase
vc.amp3 = v_init  # Amplitude of the third phase

# Record time and current
t = h.Vector().record(h._ref_t)  # Time stamp vector
ina = h.Vector().record(soma(0.5)._ref_ina)  # Sodium current
ik = h.Vector().record(soma(0.5)._ref_ik)  # Potassium current

# Initialize and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)
h.continuerun(20 * ms)

# Plot the results
plt.figure()
plt.plot(t,ina, label='Sodium Current')
plt.plot(t,ik, label='Potassium Current')
plt.xlabel("t (ms)")
plt.ylabel("Current (mA/cm^2)")
plt.legend()
plt.show()

# TODO: Add a loop for various values of voltage and plot