#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Adpative Modulation
# Author: Hemachandra
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import math
import sip
import threading



class adpative_modulation(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Adpative Modulation", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Adpative Modulation")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "adpative_modulation")

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
        self.distance = distance = 1
        self.rx_gain = rx_gain = 1/(distance**2)
        self.noise = noise = 0.01
        self.snr = snr = (rx_gain**2 / noise**2)
        self.samp_rate = samp_rate = 32e3
        self.qpsk_demod = qpsk_demod = digital.constellation_qpsk().base()
        self.qpsk_demod.set_npwr(1.0)
        self.qpsk = qpsk = [-1-1j, +1-1j, 1+1j,-1+1j]
        self.qam_demod = qam_demod = digital.constellation_16qam().base()
        self.qam_demod.set_npwr(1.0)
        self.constellation = constellation = int(0 if snr <= 10 else (1 if snr <= 20 else 2))
        self.cfo = cfo = 0.0
        self.bpsk_demod = bpsk_demod = digital.constellation_bpsk().base()
        self.bpsk_demod.set_npwr(1.0)
        self.bpsk = bpsk = [-1+0j,1+0j]
        self.QAM16 = QAM16 = [-1-1j, +1-1j, 1+1j,-1+1j,1+3j, 3+1j, 3+3j, -1+3j, -3+1j, -3+3j, 3-1j, 1-3j, 3-3j, -3-1j, -1-3j, -3-3j]

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_number_sink_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0_0.set_title("QAM16")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0_0.enable_autoscale(True)
        self._qtgui_number_sink_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_0_0_win)
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("qpsk")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_0.set_min(i, -1)
            self.qtgui_number_sink_0_0.set_max(i, 1)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(True)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_0_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("bpsk")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(True)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self._distance_range = qtgui.Range(1, 50, 1, 1, 200)
        self._distance_win = qtgui.RangeWidget(self._distance_range, self.set_distance, "Distance", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._distance_win)
        self.digital_constellation_decoder_cb_0_0_0 = digital.constellation_decoder_cb(qam_demod)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(qpsk_demod)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(bpsk_demod)
        self.digital_chunks_to_symbols_xx_1_0_0 = digital.chunks_to_symbols_bc(QAM16, 1)
        self.digital_chunks_to_symbols_xx_1_0 = digital.chunks_to_symbols_bc(qpsk, 1)
        self.digital_chunks_to_symbols_xx_1 = digital.chunks_to_symbols_bc(bpsk, 1)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bc(QAM16, 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(qpsk, 1)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(bpsk, 1)
        self._cfo_range = qtgui.Range(0, 100e3, 10, 0.0, 200)
        self._cfo_win = qtgui.RangeWidget(self._cfo_range, self.set_cfo, "Carrier Frequency Offset (Hz)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._cfo_win)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0_0_0 = blocks.sub_cc(1)
        self.blocks_sub_xx_0_0 = blocks.sub_cc(1)
        self.blocks_sub_xx_0 = blocks.sub_cc(1)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,constellation,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repeat_0_1 = blocks.repeat(gr.sizeof_gr_complex*1, 8)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, 8)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 8)
        self.blocks_packed_to_unpacked_xx_0_0_0 = blocks.packed_to_unpacked_bb(4, gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0_0 = blocks.packed_to_unpacked_bb(2, gr.GR_MSB_FIRST)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_moving_average_xx_0_0_0 = blocks.moving_average_ff(1000, (1/1000), 4000, 1)
        self.blocks_moving_average_xx_0_0 = blocks.moving_average_ff(1000, (1/1000), 4000, 1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, (1/1000), 4000, 1)
        self.blocks_keep_one_in_n_0_1_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0_1 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_mag_0_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, rx_gain)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_packed_to_unpacked_xx_0_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_keep_one_in_n_0_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_keep_one_in_n_0_1_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_constellation_decoder_cb_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.blocks_moving_average_xx_0_0, 0))
        self.connect((self.blocks_complex_to_mag_0_0_0, 0), (self.blocks_moving_average_xx_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_keep_one_in_n_0_0_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.blocks_keep_one_in_n_0_0_0_0, 0), (self.blocks_sub_xx_0_0_0, 1))
        self.connect((self.blocks_keep_one_in_n_0_1, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_1_0, 0), (self.blocks_sub_xx_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0_0_0, 0), (self.qtgui_number_sink_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_selector_0, 2))
        self.connect((self.blocks_repeat_0_1, 0), (self.blocks_selector_0, 1))
        self.connect((self.blocks_selector_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.blocks_sub_xx_0_0_0, 0), (self.blocks_complex_to_mag_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_repeat_0_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1_0, 0), (self.blocks_keep_one_in_n_0_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_1_0_0, 0), (self.blocks_keep_one_in_n_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_chunks_to_symbols_xx_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.digital_chunks_to_symbols_xx_1_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0_0, 0), (self.digital_chunks_to_symbols_xx_1_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "adpative_modulation")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance
        self.set_rx_gain(1/(self.distance**2))

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.set_snr((self.rx_gain**2 / self.noise**2))
        self.analog_const_source_x_0.set_offset(self.rx_gain)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.set_snr((self.rx_gain**2 / self.noise**2))
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_snr(self):
        return self.snr

    def set_snr(self, snr):
        self.snr = snr
        self.set_constellation(int(0 if self.snr <= 10 else (1 if self.snr <= 20 else 2)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_qpsk_demod(self):
        return self.qpsk_demod

    def set_qpsk_demod(self, qpsk_demod):
        self.qpsk_demod = qpsk_demod
        self.digital_constellation_decoder_cb_0_0.set_constellation(self.qpsk_demod)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk
        self.digital_chunks_to_symbols_xx_0_0.set_symbol_table(self.qpsk)
        self.digital_chunks_to_symbols_xx_1_0.set_symbol_table(self.qpsk)

    def get_qam_demod(self):
        return self.qam_demod

    def set_qam_demod(self, qam_demod):
        self.qam_demod = qam_demod
        self.digital_constellation_decoder_cb_0_0_0.set_constellation(self.qam_demod)

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self.blocks_selector_0.set_input_index(self.constellation)

    def get_cfo(self):
        return self.cfo

    def set_cfo(self, cfo):
        self.cfo = cfo

    def get_bpsk_demod(self):
        return self.bpsk_demod

    def set_bpsk_demod(self, bpsk_demod):
        self.bpsk_demod = bpsk_demod
        self.digital_constellation_decoder_cb_0.set_constellation(self.bpsk_demod)

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.bpsk)
        self.digital_chunks_to_symbols_xx_1.set_symbol_table(self.bpsk)

    def get_QAM16(self):
        return self.QAM16

    def set_QAM16(self, QAM16):
        self.QAM16 = QAM16
        self.digital_chunks_to_symbols_xx_0_0_0.set_symbol_table(self.QAM16)
        self.digital_chunks_to_symbols_xx_1_0_0.set_symbol_table(self.QAM16)




def main(top_block_cls=adpative_modulation, options=None):

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
