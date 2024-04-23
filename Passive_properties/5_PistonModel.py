# Import necessary modules
from neuron import h    
from neuron.units import ms, mV
import matplotlib.pyplot as plt

# create two sections to represent the soma and dendrite
dend = h.Section('dend')
soma = h.Section(name='soma')
dend.connect(soma(1)) # connect dend(0) by default to 1 of soma
h.topology()

stamp= 0.1
rm=20000	
ra=150	
c_m=1	

# Set the diameter, length, axial resistance, membrane capacitance, and number of segments of the dendrite
soma.diam=50
soma.L=50
soma.Ra=ra
soma.cm=1
soma.nseg= 10 #int((L/(0.1*lambda_f(100))+0.9)/2)*2+1
soma.insert('pas')
soma.e_pas=-65 
soma.g_pas=1/rm

# Set the diameter, length, axial resistance, membrane capacitance, and number of segments of the dendrite
dend.diam = 4
dend.L = 1000
dend.Ra = ra
dend.cm = 1
dend.nseg = 10

# Insert passive properties into the dendrite
dend.insert('pas')
dend.e_pas = -65
dend.g_pas = 1 / rm

# Set up a current clamp at the middle of the soma
stim = h.IClamp(soma(0.5))
stim.delay = 10  # Delay of the stimulus
stim.dur = 200  # Duration of the stimulus
stim.amp = stamp  # Amplitude of the stimulus

# Record the membrane potential and time at the middle of the soma
v = h.Vector().record(soma(0.5)._ref_v)  # Membrane potential vector
t = h.Vector().record(h._ref_t)  # Time stamp vector

# Record the membrane potential and time at the start and end of the dendrite
v1 = h.Vector().record(dend(0)._ref_v)
t1 = h.Vector().record(h._ref_t)
v2 = h.Vector().record(dend(1)._ref_v)
t2 = h.Vector().record(h._ref_t)

# Load the standard run library and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)
h.continuerun(300 * ms)

# Plot the membrane potential over time at the middle of the soma and at the start and end of the dendrite
plt.figure()
plt.plot(t,v)
plt.plot(t1,v1)
plt.plot(t2,v2)
plt.xlabel("t (ms)")  # Label for the x-axis
plt.ylabel("v (mV)")  # Label for the y-axis
plt.legend(["Soma", "Dendrite 0", "Dendrite 1"])  # Legend for the plot
plt.show()  # Display the plot
