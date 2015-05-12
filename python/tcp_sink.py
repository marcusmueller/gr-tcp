#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Marcus Müller.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import socket

class tcp_sink(gr.sync_block):
    """
    docstring for block tcp_sink
    """
    def __init__(self, itemsize, port, bind_addr="0.0.0.0"):
        gr.sync_block.__init__(self,
            name="tcp_sink",
            in_sig=[(numpy.byte,itemsize)],
            out_sig=None)
        self.itemsize=itemsize
        self.port = port
        self.bind_addr = bind_addr

        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind((self.bind_addr, self.port))
        self.listener.listen(1)

    def start(self):
        """
        Block start method, called when user calls tb.run/tb.start
        """
        self.connection, _ = self.listener.accept()

    def stop(self):
        self.connection.close()
        self.listener.close()


    def work(self, input_items, output_items):
        in0 = input_items[0]
        nbytes = len(in0)*self.itemsize
        nnext = nbytes // self.itemsize * self.itemsize
        last_pos = 0
        sent = 0
        remaining = nbytes
        rawbuffer = in0.data

        while nnext:
            sent = self.connection.send(rawbuffer[last_pos:last_pos+nnext]) #um, yeah.
            if not sent: ## we couldn't send a single byte --> connection is dead
                self.connection.close()
                return -1 ## We're done.
            remaining -= sent
            last_pos += sent
            nnext = remaining // self.itemsize * self.itemsize # to make sure we only send whole items
        return sent // self.itemsize

