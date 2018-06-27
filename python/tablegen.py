#!/usr/bin/python

s_len = 256 # number of values to compute

def blep(t):
    # calculate by converting to 0-1 float and back
    t = t/256.0
    t = (t*t*t) - 0.5 * (t*t*t*t)
    return int(256*t)

# define a couple of blank arrays to hold the samples
s_blep = [] #np.zeros(s_len,np.uint8)
s_recip = [] #np.zeros(s_len,np.uint8)

# calculate the tables
for i in range(0, s_len):
    s_blep.append(blep(i))
    s_recip.append(int(255/(i+1)))


f = open("tables.h", "w")

# copyright banner
print >>f, """
// Copyright 2018 Erroneous Bosh <erroneousbosh@gmail.com>
//
// Usage of the works is permitted provided that this instrument is
// retained with the works, so that any entity that uses the works is
// notified of this instrument.
//
// DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.
"""

# blep table
print >>f, "// precalculated polyblep table"
print >>f, "PROGMEM const unsigned char blep[] = {",
for i in range(0, s_len - 1):

    if (i % 16) == 0: print >>f
    print >>f,  str(s_blep[i]) + ", ",

# minor bodgery to avoid a trailing comma
print >>f, str(s_blep[i+1])+"\n};\n"

# reciprocal table
print >>f, "// precalculated reciprocal table"
print >>f, "PROGMEM const unsigned char recip[] = {",
for i in range(0, s_len - 1):

    if (i % 16) == 0: print >>f
    print >>f,  str(s_recip[i]) + ", ",

# minor bodgery to avoid a trailing comma
print >>f, "1\n};\n"


f.close()

