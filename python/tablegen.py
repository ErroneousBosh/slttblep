#!/usr/bin/python3
# Copyright 2020 Erroneous Bosh <erroneousbosh@gmail.com>
#
# Usage of the works is permitted provided that this instrument is
# retained with the works, so that any entity that uses the works is
# notified of this instrument.
#
# DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.

from textwrap import wrap


# calculate polyblep table
def blep(t):
    # calculate by converting to 0-1 float and back
    # blep function is x^3 - 0.5*x^4
    t = t/256.0

    t = (t*t*t) - 0.5 * (t*t*t*t)
    return int(256*t)


def wraplist(csl):
    """
    Output a word-wrapped list of lines, given a list of numeric values
    """

    csl = ", ".join(str(i) for i in csl)
    return wrap(csl)


# define a couple of blank arrays to hold the samples
blep_tbl = []       # list of values of precalculated polyblep
recip_tbl = []    # list of values for reciprocal table

s_len = 256  # number of values to compute


# calculate the tables
for i in range(0, s_len):
    blep_tbl.append(blep(i))
    recip_tbl.append(int(255/(i+1)))

# begin writing them out
f = open("tables.h", "w")

# copyright banner
print("""
// Copyright 2020 Erroneous Bosh <erroneousbosh@gmail.com>
//
// Usage of the works is permitted provided that this instrument is
// retained with the works, so that any entity that uses the works is
// notified of this instrument.
//
// DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.
""",  file=f)

# blep table
print("// precalculated polyblep table", file=f)
print("PROGMEM const unsigned char blep[] = {", file=f)
print(*wraplist(blep_tbl), sep="\n", file=f)
print("};\n", file=f)

# reciprocal table
print("// precalculated reciprocal table", file=f)
print("PROGMEM const unsigned char recip[] = {", file=f)
print(*wraplist(recip_tbl), sep="\n", file=f)
print("};\n", file=f)

f.close()
