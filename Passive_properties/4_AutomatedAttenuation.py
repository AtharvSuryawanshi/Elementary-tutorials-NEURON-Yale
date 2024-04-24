# Import necessary modules
from neuron import h    
from neuron.units import ms, mV
import matplotlib.pyplot as plt

# Create a section to represent the dendrite
dend = h.Section('dend')

# Define the parameters for the dendrite and the stimulus
stamp = 0.1
rm = 20_000
ra = 150 
c_m = 1
diameter = 4 
length = 1000

# Set the diameter, length, axial resistance, membrane capacitance, and number of segments of the dendrite
dend.diam = diameter
dend.L = length
dend.Ra = ra
dend.cm = c_m
dend.nseg = 23 #int((length/(0.1*h.lambda_f(100))+0.9)/2)*2+1 # or 23

# Insert passive properties into the dendrite
dend.insert("pas")
dend.e_pas = -65
dend.g_pas = 1/rm

# Set up a current clamp at the start of the dendrite
stim = h.IClamp(dend(0))
stim.delay = 10
stim.dur = 200
stim.amp = stamp

# Initialize an empty list to store the maximum membrane potentials
v_max = []

# Create a new figure for plotting
plt.figure()

# Loop over each segment of the dendrite
for nseg in range(0,dend.nseg):
    # Record the membrane potential and time at the current segment
    v = h.Vector().record(dend(nseg/dend.nseg)._ref_v)
    t = h.Vector().record(h._ref_t)
    
    # Load the standard run library and run the simulation
    h.load_file("stdrun.hoc")
    h.finitialize(-65 * mV)
    h.continuerun(300 * ms)
    v_max.append(v.max())

plt.plot(range(0,dend.nseg),v_max)
plt.xlabel('Length')
plt.ylabel('Maximum Voltage')
plt.title('Voltage vs Length')
plt.show()
