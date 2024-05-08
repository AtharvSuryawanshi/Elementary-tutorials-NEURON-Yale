# Using MOD files
MOD files, technically referred to as [NMODL files](https://neuronsimulator.github.io/nrn/python/modelspec/programmatic/mechanisms/nmodl2.html), are used in NEURON to create custom mechanisms. These files are saved with an extension of `.mod`. NMODL is a higher-level language, making it easier to code than usual C-based NEURON code. We write our mechanism in a MOD file as it is easier to write and compile it into a C-based file to run it in NEURON.
1. We first create a mod file and store it an a separate directory from the python file to avoid a clutter of files. 
2. Then we compile the mod file using `mknrndll.hoc` file in the NEURON directory. 
3. The output of compilation are a bunch of files in the directory of the mod file. 
4. We need to import `nrnmech.dll` into our python file. We do so using `h.nrn_load_dll(path to nrnmech.dll file)` command. 
5. Now we insert the mechanism into a compartment using `soma.insert('k3st')` for `k3st` as the name of the suffix of mechanism.

With this basic information, we are good to use MOD files.
