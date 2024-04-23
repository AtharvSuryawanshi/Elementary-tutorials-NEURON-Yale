# Import necessary modules
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

# Create a section to represent the soma
soma = h.Section('soma')

# Define membrane resistance and capacitance
RM=20000
CM=1

# Set the number of segments, diameter, length, and axial resistance of the soma
soma.nseg = 1
soma.diam = 100
soma.L = 100
soma.Ra = 123

# Insert passive properties into the soma
soma.insert("pas")
soma.e_pas = -65  # Set the passive reversal potential
soma.g_pas = 1/RM  # Set the passive conductance
soma.cm = CM  # Set the membrane capacitance

# Define the initial membrane potential and the holding potential for the voltage clamp
v_init = -65
Vhold = 40

# Set up a voltage clamp
vc = h.SEClamp(0.5)  # Create a SEClamp at the middle of the soma
vc.dur1 = 2  # Duration of the first phase
vc.amp1 = v_init  # Amplitude of the first phase
vc.dur2 = 10  # Duration of the second phase
vc.amp2 = Vhold  # Amplitude of the second phase
vc.dur3 = 8  # Duration of the third phase
vc.amp3 = v_init  # Amplitude of the third phase

# Record the membrane current, time, and membrane potential
ip = h.Vector().record(soma(0.5)._ref_i_cap)  # Membrane current vector
t = h.Vector().record(h._ref_t)  # Time stamp vector
v = h.Vector().record(soma(0.5)._ref_v)  # Membrane potential vector

# Load the standard run library and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)  # Initialize the simulation
h.continuerun(20 * ms)  # Run the simulation for 20 ms

# Prepare to plot the results
plt.figure()
plt.plot(t, ip)
plt.xlabel('Time (ms)')
plt.ylabel('Current (nA)')
plt.title('Voltage Clamp')
plt.show()
