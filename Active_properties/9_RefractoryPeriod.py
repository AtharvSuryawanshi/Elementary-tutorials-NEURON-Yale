from neuron import h, nrn
from neuron.units import mV, ms
import matplotlib.pyplot as plt

# Create a soma section
soma = h.Section(name='soma')
soma.nseg = 1  # Number of segments
soma.L = 25  # Length of the soma
soma.diam = 25  # Diameter of the soma

# Insert Hodgkin-Huxley channels
soma.insert('hh')
soma.el_hh = -70  # Leak reversal potential

# Delay between two stimuli
delay = 2

# Create first current clamp
stim1 = h.IClamp(soma(0.5))
stim1.delay = 0  # Start time of the current
stim1.dur = 1  # Duration of the current
stim1.amp = 5  # Amplitude of the current

# Create second current clamp
stim2 = h.IClamp(soma(0.5))
stim2.delay = delay  # Start time of the current
stim2.dur = 1  # Duration of the current
stim2.amp = 5  # Amplitude of the current

# Total simulation time
tstop = 20

# Record the voltage and time
v = h.Vector().record(soma(0.5)._ref_v)  # Soma voltage
t = h.Vector().record(h._ref_t)  # Time stamp vector

# Initialize and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)
h.continuerun(tstop * ms)

# Plot the results
plt.figure()
plt.plot(t, v)
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.show()