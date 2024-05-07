from neuron import h 
from neuron.units import mV, ms
import matplotlib.pyplot as plt

soma = h.Section(name='soma')
soma.L = 18.8  # Length of the soma
soma.Ra = 123  # Axial resistance of the soma
soma.diam = 18.8  # Diameter of the soma
soma.nseg = 1  # Number of segments in the soma

soma.insert('hh')  # Insert Hodgkin-Huxley mechanism in the soma
stamp = 0.1  # Amplitude of the current clamp stimulus
stim = h.IClamp(soma(0.5))  # Create a current clamp stimulus at the center of the soma

stim.delay = 100  # Delay before the stimulus starts
stim.dur = 500  # Duration of the stimulus
stim.amp = stamp  # Amplitude of the stimulus

tstop = 1000  # Duration of the simulation

v = h.Vector().record(soma(0.5)._ref_v)  # Record the membrane potential at the center of the soma
t = h.Vector().record(h._ref_t)  # Record the time

h.load_file("stdrun.hoc")  # Load the standard run library
h.finitialize(-65 * mV)  # Set the initial membrane potential
h.continuerun(tstop * ms)  # Run the simulation for the specified duration

plt.figure()
plt.plot(t, v)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()
