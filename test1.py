#!/usr/bin/env python
from transmitters import transmitters
from source_alphabet import source_alphabet
from gnuradio import channels, gr

for alphabet_type in transmitters.keys():
    print alphabet_type
    for i,mod_type in enumerate(transmitters[alphabet_type]):
        print i,mod_type

        tx_len = int(100e3)
        src = source_alphabet(alphabet_type, tx_len)
        mod = mod_type()
        chan = channels.selective_fading_model(8, 20.0/1e6, False, 4.0, 0, (0.0,0.1,1.3), (1,0.99,0.97), 8)

        tb = gr.top_block()
        tb.connect(src, mod, chan)
        tb.run()


    
