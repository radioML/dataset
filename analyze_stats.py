
import numpy as np
import cPickle

def calc_vec_energy(vec):
    isquared = np.power(vec[0],2.0)
    qsquared = np.power(vec[1], 2.0)
    inst_energy = np.sqrt(isquared+qsquared)
    return sum(inst_energy)

def calc_mod_energies(ds):
    for modulation, snr in ds:
        avg_energy = 0
        nvectors = ds[(modulation,snr)].size
        for vec in ds[(modulation, snr)]:
            avg_energy += calc_vec_energy(vec)
        avg_energy /= ds[(modulation, snr)].__len__()
        print "%s at %i has %i vectors avg energy of %2.1f" % (modulation, snr, nvectors, avg_energy)

def open_ds(location="X_3_dict.dat"):
    f = open(location)
    ds = cPickle.load(f)
    return ds

def main():
    ds = open_ds()
    calc_mod_energies(ds)

if __name__ == "__main__":
    main()
