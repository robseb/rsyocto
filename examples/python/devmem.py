#!/usr/bin/env python
"""
This is designed primarily for use with accessing /dev/mem on OMAP platforms.
It should work on other platforms and work to mmap() files rather then just
/dev/mem, but these use cases aren't well tested.

All file accesses are aligned to DevMem.word bytes, which is 4 bytes on ARM
platforms to avoid data abort faults when accessing peripheral registers.

References:
    http://wiki.python.org/moin/PythonSpeed/PerformanceTips
    http://www.python.org/dev/peps/pep-0008/

"""

import os
import sys
import mmap
import struct
import optparse

""" DevMemBuffer
This class holds data for objects returned from DevMem class
It allows an easy way to print hex data
"""
class DevMemBuffer:

    def __init__(self, base_addr, data):
        self.data = data
        self.base_addr = base_addr

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def hexdump(self, word_size = 4, words_per_row = 4):
        # Build a list of strings and then join them in the last step.
        # This is more efficient then concat'ing immutable strings.

        d = self.data
        dump = []

        word = 0
        while (word < len(d)):
            dump.append('0x{0:02x}:  '.format(self.base_addr
                                              + word_size * word))

            max_col = word + words_per_row
            if max_col > len(d): max_col = len(d)

            while (word < max_col):
                # If the word is 4 bytes, then handle it and continue the
                # loop, this should be the normal case
                if word_size == 4:
                    dump.append(" {0:08x} ".format(d[word]))
                    word += 1
                    continue

                # Otherwise the word_size is not an int, pack it so it can be
                # un-packed to the desired word size.  This should blindly
                # handle endian problems (Verify?)
                packed = struct.pack('I',(d[word]))
                if word_size == 2:
                    dh = struct.unpack('HH', packed)
                    dump.append(" {0:04x}".format(dh[0]))
                    word += 1
                elif word_size == 1:
                    db = struct.unpack('BBBB', packed)
                    dump.append(" {0:02x}".format(db[0]))
                    word += 1

            dump.append('\n')

        # Chop off the last new line character and join the list of strings
        # in to a single string
        return ''.join(dump[:-1])

    def __str__(self):
        return self.hexdump()


""" DevMem
Class to read and write data aligned to word boundaries of /dev/mem
"""
class DevMem:
    # Size of a word that will be used for reading/writing
    word = 4
    mask = ~(word - 1)

    def __init__(self, base_addr, length = 1, filename = '/dev/mem',
                 debug = 0):

        if base_addr < 0 or length < 0: raise AssertionError
        self._debug = debug

        self.base_addr = base_addr & ~(mmap.PAGESIZE - 1)
        self.base_addr_offset = base_addr - self.base_addr

        stop = base_addr + length * self.word
        if (stop % self.mask):
            stop = (stop + self.word) & ~(self.word - 1)

        self.length = stop - self.base_addr
        self.fname = filename

        # Check filesize (doesn't work with /dev/mem)
        #filesize = os.stat(self.fname).st_size
        #if (self.base_addr + self.length) > filesize:
        #    self.length = filesize - self.base_addr

        self.debug('init with base_addr = {0} and length = {1} on {2}'.
                format(hex(self.base_addr), hex(self.length), self.fname))

        # Open file and mmap
        f = os.open(self.fname, os.O_RDWR | os.O_SYNC)
        self.mem = mmap.mmap(f, self.length, mmap.MAP_SHARED,
                mmap.PROT_READ | mmap.PROT_WRITE,
                offset=self.base_addr)


    """
    Read length number of words from offset
    """
    def read(self, offset, length):
        if offset < 0 or length < 0: raise AssertionError

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        self.debug('reading {0} bytes from offset {1}'.
                   format(length * self.word, hex(offset)))

        # Compensate for the base_address not being what the user requested
        # and then seek to the aligned offset.
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)

        # Read length words of size self.word and return it
        data = []
        for i in range(length):
            data.append(struct.unpack('I', mem.read(self.word))[0])

        abs_addr = self.base_addr + virt_base_addr
        return DevMemBuffer(abs_addr + offset, data)


    """
    Write length number of words to offset
    """
    def write(self, offset, din):
        if offset < 0 or len(din) <= 0: raise AssertionError

        self.debug('writing {0} bytes to offset {1}'.
                format(len(din), hex(offset)))

        # Make reading easier (and faster... won't resolve dot in loops)
        mem = self.mem

        # Compensate for the base_address not being what the user requested
        offset += self.base_addr_offset

        # Check that the operation is going write to an aligned location
        if (offset & ~self.mask): raise AssertionError

        # Seek to the aligned offset
        virt_base_addr = self.base_addr_offset & self.mask
        mem.seek(virt_base_addr + offset)

        # Read until the end of our aligned address
        for i in range(0, len(din), self.word):
            self.debug('writing at position = {0}: 0x{1:x}'.
                        format(self.mem.tell(), din[i]))
            # Write one word at a time
            mem.write(struct.pack('I', din[i]))

    def debug_set(self, value):
        self._debug = value

    def debug(self, debug_str):
        if self._debug: print('DevMem Debug: {0}'.format(debug_str))


""" Main
If this is run as a script (rather then imported as a module) it provides
some basic functionality out of the box
"""
def main():
    parser = optparse.OptionParser()

    parser.add_option("-r", "--read", dest="read", metavar="ADDR",
            type=int, help="read a value")

    parser.add_option("-w", "--write", dest="write", help="write a value",
            nargs=2, type=int, metavar="ADDR VALUE")

    parser.add_option("-n", "--num", dest="num",
            help="number of words to read",
            type=int, default=1)

    parser.add_option("-s", "--word-size", dest="word_size",
            help="size of word when displayed",
            type=int, default=4)

    parser.add_option("-m", "--mmap", dest="mmap",
            metavar="FILE",
            help="file to open with mmap()",
            type=str, default="/dev/mem")

    parser.add_option("-v", action="store_true", dest="verbose",
            help="provide more information regarding operation")

    parser.add_option("-d", action="store_true", dest="debug",
            help="provide debugging information")

    (options, args) = parser.parse_args()

    # Check for sane arguments
    if options.write is not None and options.read is not None:
        parser.print_help()
        print("\nError: Both read and write are specified")
        return -1
    elif options.write is None and options.read is None:
        parser.print_help()
        print("\nError: Neither read or write are specified")
        return -1

    if options.num < 0:
        parser.print_help()
        print("\nError: Invalid num of words specified")
        return -1

    if (options.word_size != 1 and options.word_size != 2
                               and options.word_size != 4):
        parser.print_help()
        print("\nError: Invalid word size specified")
        return -1

    # Only support writing one word at a time, force this
    if options.write is not None and options.num != 1:
        print("Warning: Forcing number of words to 1 for set operation\n")
        options.num = 1

    # Determine base address to operate on
    addr = options.read
    if options.write is not None: addr = options.write[0]

    # Create the Dev Mem object that does the magic
    mem = DevMem(addr, length=options.num, filename=options.mmap,
                 debug=options.debug)

    if options.debug:
        mem.debug_set(1)

    # Perform the actual read or write
    if options.write is not None:
        if options.verbose:
            print("Value before write:\t{0}".format(
                  mem.read(0x0, options.num).hexdump(options.word_size)))

        mem.write(0x0, [options.write[1]])

        if options.verbose:
            print("Value after write:\t{0}".format(
                  mem.read(0x0, options.num).hexdump(options.word_size)))
    else:
        print(mem.read(0x0, options.num).hexdump(options.word_size))


if __name__ ==  '__main__':

    sys.exit(main())
