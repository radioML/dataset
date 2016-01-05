#!/usr/bin/env python
from transmitters import transmitters
from source_alphabet import source_alphabet
import timeseries_slicer
from gnuradio import channels, gr, blocks
import matplotlib.pyplot as plt
import numpy as np
import numpy.fft, cPickle


for alphabet_type in transmitters.keys():
    print alphabet_type
    output = {}
    for i,mod_type in enumerate(transmitters[alphabet_type]):
        print "running test", i,mod_type

        tx_len = int(100e3)
        src = source_alphabet(alphabet_type, tx_len)
        mod = mod_type()
        #chan = channels.selective_fading_model(8, 20.0/1e6, False, 4.0, 0, (0.0,0.1,1.3), (1,0.99,0.97), 8)

        snk = blocks.vector_sink_c()

        tb = gr.top_block()
        tb.connect(src, mod, snk)
        #tb.connect(src, mod, chan, snk)
        tb.run()

        print "finished: ", len(snk.data())
        output[mod_type.modname] = np.array(snk.data(), dtype=np.complex64)

        plt.figure()
        plt.subplot(2,1,1)
        x = snk.data()
        plt.plot(10*np.log10(numpy.fft.fftshift(numpy.fft.fft(x[0:100000]))))
        plt.subplot(2,1,2)
        plt.plot(x[0:100000])
        plt.title("Modulated %s"%(mod_type.modname))

X = timeseries_slicer.slice_timeseries_dict(output, 128, 64, 1000)
#print len(X), X[X.keys()[0]].shape
X = np.vstack(X.values())
print X.shape
cPickle.dump( X, file("X_1.dat", "wb" ) )

plt.pause(5)
#plt.show()
