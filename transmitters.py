#!/usr/bin/env python
import time, math
from scipy.signal import get_window
from gnuradio import gr, blocks, digital, analog, filter

class transmitter_qpsk(gr.hier_block2):
    modname = "QPSK"
    def __init__(self, const=digital.qpsk_constellation(), isps=4, ebw=0.35):
        gr.hier_block2.__init__(self, "transmitter_qpsk",
        gr.io_signature(1, 1, gr.sizeof_char),
        gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.mod = digital.generic_mod(constellation=const,
            differential=False,
            samples_per_symbol=isps,
            pre_diff_code=True,
            excess_bw=ebw,
            verbose=False,
            log=False)
        self.connect(self, self.mod, self)
        self.rate = const.bits_per_symbol()

class transmitter_fm(gr.hier_block2):
    modname = "WBFM"
    def __init__(self):
        gr.hier_block2.__init__(self, "transmitter_fm",
        gr.io_signature(1, 1, gr.sizeof_float),
        gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.mod = analog.wfm_tx( audio_rate=44100.0, quad_rate=220.5e3 )
        self.connect( self, self.mod, self )
        self.rate = 200e3/44.1e3

class transmitter_am(gr.hier_block2):
    modname = "AM"
    def __init__(self):
        gr.hier_block2.__init__(self, "transmitter_fm",
        gr.io_signature(1, 1, gr.sizeof_float),
        gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.rate = 44.1e3/200e3
        #self.rate = 200e3/44.1e3
        self.interp = filter.fractional_interpolator_ff(0.0, self.rate)
        self.cnv = blocks.float_to_complex()
        self.mul = blocks.multiply_const_cc(1.0)
        self.add = blocks.add_const_cc(1.0)
        self.src = analog.sig_source_c(200e3, analog.GR_SIN_WAVE, 0e3, 1.0)
        #self.src = analog.sig_source_c(200e3, analog.GR_SIN_WAVE, 50e3, 1.0)
        self.mod = blocks.multiply_cc()
        self.connect( self, self.interp, self.cnv, self.mul, self.add, self.mod, self )
        self.connect( self.src, (self.mod,1) )

transmitters = {
    "discrete":[transmitter_qpsk],
    "continuous":[transmitter_fm, transmitter_am]
    }
