# Import necessary modules
from neuron import h
from neuron.units import ms, mV
import matplotlib.pyplot as plt

# Create a section to represent the soma
dend = h.Section('dend')

stamp = 0.5 # nA
rm = 20000	# ohm cm2
ra = 150	# ohm cm
c_m = 1	# muF cm2
diameter = 4 # mu m
# Set the length of the dendrite
length = 1000 # mu m

# Set the diameter, length, axial resistance, membrane capacitance, and number of segments of the dendrite
dend.diam = diameter
dend.L = length
dend.Ra = ra
dend.cm = c_m
dend.nseg = 23 #int((length/(0.1*h.lambda_f(100))+0.9)/2)*2+1 # or 23

# Print the number of segments
print(dend.nseg)

# Insert passive properties into the dendrite
dend.insert("pas")
dend.e_pas = -65
dend.g_pas = 1/rm

# Set up a current clamp at the start of the dendrite
stim = h.IClamp(dend(0))
stim.delay = 10
stim.dur = 200
stim.amp = stamp

# Record the membrane potential and time at the start, middle, and end of the dendrite
v0 = h.Vector().record(dend(0)._ref_v)
t0 = h.Vector().record(h._ref_t)
v1 = h.Vector().record(dend(0.5)._ref_v)
t1 = h.Vector().record(h._ref_t)
v2 = h.Vector().record(dend(1)._ref_v)
t2 = h.Vector().record(h._ref_t)

# Load the standard run library and run the simulation
h.load_file("stdrun.hoc")
h.finitialize(-65 * mV)
h.continuerun(300 * ms)

# Plot the membrane potential over time at the start, middle, and end of the dendrite
plt.figure()
plt.plot(t0,v0, label='Start')
plt.plot(t1,v1, label='Middle')
plt.plot(t2,v2, label='End')
plt.xlabel("t (ms)")
plt.ylabel("v (mV)")
plt.legend()
plt.show()