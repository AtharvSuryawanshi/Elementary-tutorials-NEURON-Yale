# importing files
from neuron import h    
from neuron.units import ms, mV
import matplotlib.pyplot as plt

# creating a soma section
soma = h.Section(name='soma') 

# initializing dimensions
soma.diam = 100
soma.L = 50 

# inserting passive ions 
soma.insert('pas') # "hh" for active HH channels

# defining R,C,vm
soma.e_pas = -65
soma.g_pas = 1/20000
soma.cm = 1
stamp = 0.1
stim = h.IClamp(soma(0.5)) # stim at half of soma
# stimulation parameters
stim.delay = 50
stim.dur = 700
stim.amp = stamp

# recording variables
v = h.Vector().record(soma(0.5)._ref_v)  # Membrane potential vector
t = h.Vector().record(h._ref_t)  # Time stamp vector

# running variables 
h.load_file("stdrun.hoc") # load file for running
h.finitialize(-65 * mV) # initial voltage
h.continuerun(1000 * ms) # duration of running


# plotting result
plt.figure()
plt.plot(t,v)
plt.xlabel("t (ms)")
plt.ylabel("v (mV)")
plt.show()
# h.t = 1000