from neuron import h 
from neuron.units import mV, ms
import matplotlib.pyplot as plt


# Create soma and dendrites
soma = h.Section(name='soma')
dend0 = h.Section(name='dend')
dend1 = h.Section(name='dend')

# Set soma properties
soma.L = 18.8  # Length
soma.Ra = 123  # Axial resistance
soma.diam = 18.8  # Diameter
soma.insert('hh')  # Insert Hodgkin-Huxley channels
soma.gnabar_hh = 0.25  # Sodium conductance
soma.gl_hh = 0.0001666  # Leak conductance
soma.el_hh = -60  # Leak reversal potential

# Set dendrite 0 properties
dend0.nseg = 5  # Number of segments
dend0.diam = 3.18  # Diameter
dend0.L = 701.9  # Length
dend0.Ra = 123  # Axial resistance
dend0.insert('pas')  # Insert passive channels
dend0.g_pas = .0001667  # Passive conductance
dend0.e_pas = -60.0  # Passive reversal potential

# Set dendrite 1 properties
dend1.nseg = 5  # Number of segments
dend1.diam = 2  # Diameter
dend1.L = 1000  # Length
dend1.Ra = 123  # Axial resistance
dend1.insert('pas')  # Insert passive channels
dend1.g_pas = .0001667  # Passive conductance
dend1.e_pas = -60.0  # Passive reversal potential

# Connect dendrites to soma
dend0.connect(soma(0))
dend1.connect(soma(1))

# Create a current clamp
stim = h.IClamp(soma(0.5))
stim.delay = 100  # Start time of the current
stim.dur = 100  # Duration of the current
stim.amp = 0.1  # Amplitude of the current
tstop = 300  # Total simulation time

# Record the voltage and time
v = h.Vector().record(soma(0.5)._ref_v)  # Soma voltage
t = h.Vector().record(h._ref_t)  # Time stamp vector
v0 = h.Vector().record(dend0(1)._ref_v)  # Dendrite 0 voltage
v1 = h.Vector().record(dend1(1)._ref_v)  # Dendrite 1 voltage

# Initialize and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)
h.continuerun(tstop * ms)

# Plot the results
plt.figure()
plt.plot(t, v, label='Soma')
plt.plot(t, v1, label='Dendrite 1')
plt.plot(t, v0, label='Dendrite 0')
plt.xlabel('t (ms)')
plt.ylabel('v (mV)')
plt.legend()
plt.show()