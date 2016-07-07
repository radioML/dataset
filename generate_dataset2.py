#!/usr/bin/env python
from transmitters import transmitters
from source_alphabet import source_alphabet
import timeseries_slicer
from gnuradio import channels, gr, blocks
import numpy as np
import numpy.fft, cPickle, gzip

# Simple model 
# AWGN only

apply_channel = True

output = {}
for alphabet_type in transmitters.keys():
    print alphabet_type
    for i,mod_type in enumerate(transmitters[alphabet_type]):
        print "running test", i,mod_type

        tx_len = int(400e3)
        src = source_alphabet(alphabet_type, tx_len, True)
        mod = mod_type()
        #chan = channels.selective_fading_model(8, 20.0/1e6, False, 4.0, 0, (0.0,0.1,1.3), (1,0.99,0.97), 8)
        fD = 1
        delays = [0.0, 0.9, 1.7]
        mags = [1, 0.8, 0.3]
        ntaps = 8
        noise_amp = 0.1
        f_off = 0
        epsilon = 1+1e-3
        #chan = channels.channel_model( noise_amp, f_off, epsilon, [1] )
        chan = channels.channel_model( noise_amp, 0, 1, [1] )
#        chan = channels.dynamic_channel_model( 200e3, 0.01, 1e3, 0.01, 1e3, 8, fD, True, 4, delays, mags, ntaps, noise_amp, 0x1337 )
        #chan = channels.dynamic_channel_model( 200e3, 0, 1e3, 0, 1e3, 8, fD, True, 4, delays, mags, ntaps, noise_amp, 0x1337 )
        #chan = channels.dynamic_channel_model( 200e3, 0.1, 1e3, 0.1, 1e3, 8, fD, True, 4, delays, mags, ntaps, noise_amp, 0x1337 )

        snk = blocks.vector_sink_c()

        tb = gr.top_block()

        # connect blocks
        if apply_channel:
            tb.connect(src, mod, chan, snk)
        else:
            tb.connect(src, mod, snk)
        tb.run()

        print "finished: ", len(snk.data())
        output[mod_type.modname] = np.array(snk.data(), dtype=np.complex64)

        x = snk.data()

#X = timeseries_slicer.slice_timeseries_dict(output, 64, 32, 1000)
X = timeseries_slicer.slice_timeseries_dict(output, 128, 64, 1000)
cPickle.dump( X, file("X_2_dict.dat", "wb" ) )
#cPickle.dump( X, gzip.open("X_1_dict.pkl.gz", "wb" ) )
print X.keys()
#print len(X), X[X.keys()[0]].shape
X = np.vstack(X.values())
print X.shape
cPickle.dump( X, file("X_2.dat", "wb" ) )
#cPickle.dump( X, gzip.open("X_1.pkl.gz", "wb" ) )

