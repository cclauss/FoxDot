#!/usr/bin/python

""" This module manages the allocation of buffer numbers and samples """

from os.path import abspath, join, dirname
import os

def path(fn):
    return abspath(join(dirname(__file__), fn))

alpha    = "abcdefghijklmnopqrstuvwxyz"

nonalpha = {"&" : "ampersand",
            "*" : "asterix",
            "@" : "at",
            "|" : "bar",
            "^" : "caret",
            ":" : "colon",
            "$" : "dollar",
            "=" : "equals",
            "!" : "exclamation",
            "/" : "forwardslash",
            ">" : "greaterthan",
            "#" : "hash",
            "-" : "hyphen",
            "<" : "lessthan",
            "%" : "percent",
            "+" : "plus",
            "?" : "question",
            "~" : "tilde",
            "\\" :"backslash" }
            
class BufChar:
    def __init__(self, char):
        self.char    = char
        self.buffers = {}
        self.files   = []
    def addbuffer(self, fn, num):
        self.buffers[fn] = num
        self.files.append(fn)
    def __iter__(self):
        for fn, buf in self.buffers.items():
            yield fn, buf
    def bufnum(self, n):
        return self.buffers[self.files[n % len(self.files)]]

class BufferManager:
    def __init__(self):

        # ServerManager Object
        self.server = None

        # Dictionary of characters to respective buffer number
        self.symbols = {}

        # Dictionary of buffer numbers to character
        self.buffers = {}

        # Load buffers
        bufnum = 1
        root   = path("./Samples/")

        # Go through the alphabet

        for char in alpha:
            upper = join(root, char, "upper")
            lower = join(root, char, "lower")

            # Iterate over each

            self.symbols[char] = BufChar(char)

            if os.path.isdir(lower):
                try:
                    for f in sorted(os.listdir(lower)):

                        self.symbols[char].addbuffer(join(lower, f), bufnum)

                        bufnum += 1

                except:
                    del self.symbols[char]

            char = char.upper()

            self.symbols[char] = BufChar(char)

            if os.path.isdir(upper):
                try:
                    for f in sorted(os.listdir(upper)):

                        self.symbols[char].addbuffer(join(upper, f), bufnum)

                        bufnum += 1

                except:
                    del self.symbols[char]
            
        # Go through symbols

        for char in nonalpha:

            self.symbols[char] = BufChar(char)

            folder = join(root, "_", nonalpha[char])

            if (os.path.isdir(folder)):
                try:
                    for f in sorted(os.listdir(folder)):

                        self.symbols[char].addbuffer(join(folder, f), bufnum)

                        bufnum += 1

                except:
                    del self.symbols[char]

        # Define empty buffer
        self.nil = BufChar(None)
        self.nil.addbuffer(None, 0)

    def __getitem__(self, key):
        return self.symbols.get(key, self.nil)
        
    def __call__(self, server):
        self.server = server 
        return self

    def __str__(self):
        return "\n".join(["{}: {}".format(symbol, self.buffers[n]) for symbol, n in self.symbols.items()])

    def load(self):
        for char in self.symbols:
            for fn, buf in self.symbols[char]:
                self.server.bufferRead(buf, path(fn))
        return
            
##        for buf, fn in self.buffers.items():
##            self.server.bufferRead(buf, path("./Samples/" + fn))

    def bufnum(self, char):
        return self.symbols.get(char, 0)
##        b = 0
##        for ch, buf in self.symbols.items():
##            if ch == char:
##                b = buf
##        return b
