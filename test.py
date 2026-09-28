#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import osmosdr
import time
import sip
import test_epy_block_0 as epy_block_0  # embedded python block
import test_epy_module_0 as epy_module_0  # embedded python module
import threading



class test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.thr = thr = -100
        self.samp_rate = samp_rate = 2.4e6
        self.fun_prob_1 = fun_prob_1 = 0
        self.freq = freq = 433.5
        self.out = out = epy_module_0.detect(fun_prob_1,samp_rate,thr,freq)
        self.freqmin = freqmin = freq-samp_rate/2/1e6
        self.fft_length = fft_length = 2048
        self.fch = fch = out[0]
        self.vec_length = vec_length = 2048
        self.pos = pos = int(((float(fch)-freqmin)/(samp_rate/1e6))*fft_length)
        self.gain = gain = 10
        self.found = found = fch
        self.bw = bw = out[1]

        ##################################################
        # Blocks
        ##################################################

        self._thr_range = qtgui.Range(-150, -50, 1, -100, 200)
        self._thr_win = qtgui.RangeWidget(self._thr_range, self.set_thr, "threshold", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._thr_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.prob_sig_vec = blocks.probe_signal_vf(vec_length)
        self._gain_range = qtgui.Range(0, 49, 1, 10, 200)
        self._gain_win = qtgui.RangeWidget(self._gain_range, self.set_gain, "gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._gain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("frequency" + ": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.editingFinished.connect(
            lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_vector_sink_f_0 = qtgui.vector_sink_f(
            vec_length,
            (freq*1e6-samp_rate/2),
            (samp_rate/fft_length),
            "Freq in MHz",
            "PSD",
            "",
            3, # Number of inputs
            None # parent
        )
        self.qtgui_vector_sink_f_0.set_update_time(0.10)
        self.qtgui_vector_sink_f_0.set_y_axis((-105), (-90))
        self.qtgui_vector_sink_f_0.enable_autoscale(False)
        self.qtgui_vector_sink_f_0.enable_grid(True)
        self.qtgui_vector_sink_f_0.set_x_axis_units("")
        self.qtgui_vector_sink_f_0.set_y_axis_units("")
        self.qtgui_vector_sink_f_0.set_ref_level(0)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [2, 2, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_vector_sink_f_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_vector_sink_f_0.set_line_label(i, labels[i])
            self.qtgui_vector_sink_f_0.set_line_width(i, widths[i])
            self.qtgui_vector_sink_f_0.set_line_color(i, colors[i])
            self.qtgui_vector_sink_f_0.set_line_alpha(i, alphas[i])

        self._qtgui_vector_sink_f_0_win = sip.wrapinstance(self.qtgui_vector_sink_f_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_vector_sink_f_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-90), (-80))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq((freq*1e6), 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(gain, 0)
        self.osmosdr_source_0.set_bb_gain(gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        def _fun_prob_1_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.prob_sig_vec.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_fun_prob_1,val))
              except AttributeError:
                self.set_fun_prob_1(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _fun_prob_1_thread = threading.Thread(target=_fun_prob_1_probe)
        _fun_prob_1_thread.daemon = True
        _fun_prob_1_thread.start()
        self._found_tool_bar = Qt.QToolBar(self)

        if None:
            self._found_formatter = None
        else:
            self._found_formatter = lambda x: eng_notation.num_to_str(x)

        self._found_tool_bar.addWidget(Qt.QLabel("'found'"))
        self._found_label = Qt.QLabel(str(self._found_formatter(self.found)))
        self._found_tool_bar.addWidget(self._found_label)
        self.top_layout.addWidget(self._found_tool_bar)
        self.fft_vxx_0 = fft.fft_vcc(fft_length, True, window.blackmanharris(fft_length), True, 10)
        self.epy_block_0 = epy_block_0.blk(pos_init=pos-bw//2, pos_end=pos+bw//2, veclen=vec_length)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_float*1, vec_length)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, vec_length)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, vec_length, (-100))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*vec_length, (int(round(samp_rate/fft_length/1000))))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(100, vec_length)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(vec_length)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, thr)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.prob_sig_vec, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.qtgui_vector_sink_f_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.qtgui_vector_sink_f_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_vector_sink_f_0, 2))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_thr(self):
        return self.thr

    def set_thr(self, thr):
        self.thr = thr
        self.set_out(epy_module_0.detect(self.fun_prob_1,self.samp_rate,self.thr,self.freq))
        self.analog_const_source_x_0.set_offset(self.thr)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_freqmin(self.freq-self.samp_rate/2/1e6)
        self.set_out(epy_module_0.detect(self.fun_prob_1,self.samp_rate,self.thr,self.freq))
        self.set_pos(int(((float(self.fch)-self.freqmin)/(self.samp_rate/1e6))*self.fft_length))
        self.blocks_keep_one_in_n_0.set_n((int(round(self.samp_rate/self.fft_length/1000))))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq*1e6-self.samp_rate/2), (self.samp_rate/self.fft_length))

    def get_fun_prob_1(self):
        return self.fun_prob_1

    def set_fun_prob_1(self, fun_prob_1):
        self.fun_prob_1 = fun_prob_1
        self.set_out(epy_module_0.detect(self.fun_prob_1,self.samp_rate,self.thr,self.freq))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.set_freqmin(self.freq-self.samp_rate/2/1e6)
        self.set_out(epy_module_0.detect(self.fun_prob_1,self.samp_rate,self.thr,self.freq))
        self.osmosdr_source_0.set_center_freq((self.freq*1e6), 0)
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq*1e6-self.samp_rate/2), (self.samp_rate/self.fft_length))

    def get_out(self):
        return self.out

    def set_out(self, out):
        self.out = out
        self.set_bw(self.out[1])
        self.set_fch(self.out[0])

    def get_freqmin(self):
        return self.freqmin

    def set_freqmin(self, freqmin):
        self.freqmin = freqmin
        self.set_pos(int(((float(self.fch)-self.freqmin)/(self.samp_rate/1e6))*self.fft_length))

    def get_fft_length(self):
        return self.fft_length

    def set_fft_length(self, fft_length):
        self.fft_length = fft_length
        self.set_pos(int(((float(self.fch)-self.freqmin)/(self.samp_rate/1e6))*self.fft_length))
        self.blocks_keep_one_in_n_0.set_n((int(round(self.samp_rate/self.fft_length/1000))))
        self.fft_vxx_0.set_window(window.blackmanharris(self.fft_length))
        self.qtgui_vector_sink_f_0.set_x_axis((self.freq*1e6-self.samp_rate/2), (self.samp_rate/self.fft_length))

    def get_fch(self):
        return self.fch

    def set_fch(self, fch):
        self.fch = fch
        self.set_found(self.fch)
        self.set_pos(int(((float(self.fch)-self.freqmin)/(self.samp_rate/1e6))*self.fft_length))

    def get_vec_length(self):
        return self.vec_length

    def set_vec_length(self, vec_length):
        self.vec_length = vec_length
        self.epy_block_0.veclen = self.vec_length

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos
        self.epy_block_0.pos_end = self.pos+self.bw//2
        self.epy_block_0.pos_init = self.pos-self.bw//2

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)
        self.osmosdr_source_0.set_if_gain(self.gain, 0)
        self.osmosdr_source_0.set_bb_gain(self.gain, 0)

    def get_found(self):
        return self.found

    def set_found(self, found):
        self.found = found
        Qt.QMetaObject.invokeMethod(self._found_label, "setText", Qt.Q_ARG("QString", str(self._found_formatter(self.found))))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.epy_block_0.pos_end = self.pos+self.bw//2
        self.epy_block_0.pos_init = self.pos-self.bw//2




def main(top_block_cls=test, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
