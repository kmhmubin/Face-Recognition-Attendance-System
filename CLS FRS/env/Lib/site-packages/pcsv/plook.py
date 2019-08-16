#!/usr/bin/env python
import six
import csv
import sys
import codecs
import itertools
from six.moves import zip_longest

def csv2pretty(s, max_field_size=None):
    f_in = six.StringIO(s)
    return "\n".join(get_all_lines(f_in, 100, False, ",", max_field_size))

def width(string, max_field_size):
    """
    compute the length of the string as printed by less
    which can be complicated for unicode characters

    chinese characters are twice the normal width
    http://stackoverflow.com/questions/2476953/python-utf-8-howto-align-printout
    """
    #invalid unicode characters are usually printed like '<E6>'
    #ie they take up *four characters*
    #replace them with four spaces to calculate width correctly
    codecs.register_error('four_space',lambda x: (u"    ",x.start+1))
    string = preprocess_field(string, max_field_size)
    if sys.version_info[0] <= 2:
        string = string.decode("utf8", "four_space")


    #some unicode characters are printed like <U+052A>
    #ie they take up *eight characters*
    #replace them with eight spaces
    bad_unicode = u'\u052a' + u'\u0377' + u'\u037f' + u'\ufeff' + u'\u200b'
    string = "".join([u" "*8 if (c in bad_unicode) else c for c in string])


    #early ascii characters are printed like ^W
    #ie take up *two characters*
    #replace them with two spaces
    early_unicode = [chr(i) for i in range(0,9)] + \
                    [chr(11) + chr(12)] + \
                    [chr(i) for i in range(14,27)] + \
                    [chr(i) for i in range(28,32)]
    string = "".join([u" "*2 if (c in early_unicode) else c for c in string])


    #chinese characters take up double the width of normal characters
    import unicodedata
    return sum(1 + (unicodedata.east_asian_width(c) in "WF") for c in string)

def spacing_line(widths):
    """
    special string printed three times:
    before hdr, between hdr and first row, and after last row
    """
    return '|-' + '+'.join(['-'*(w+2) for w in widths]) + '-|'

def preprocess_field(field, max_field_size):
    field = field.replace("\t"," "*4)
    field = field.replace("\n","")
    field = field.replace("\r","")
    if max_field_size and len(field) > max_field_size:
        field = field[:(max_field_size - 3)] + "..."
    return field

def pretty_print_field(full_width, field, max_field_size):
    """
    pad the field string to have len full_width
    "fieldvalue" --> " fieldvalue     "
    """
    field = preprocess_field(field, max_field_size)
    extra_spaces = full_width - width(field, max_field_size)
    return " " + field + " "*extra_spaces + " "

def pretty_print_row(col_full_widths, row, max_field_size):
    """
    pretty print a row such that each column is padded to have the widths in the col_full_widths vector
    """
    start = "| "
    if len(row) == len(col_full_widths):
        end = " |"
    else:
        end = "|"
    return start + "|".join(pretty_print_field(full_width, field, max_field_size) for full_width, field in zip(col_full_widths, row)) + end


def compute_full_widths(hdr, cached_lines, max_field_size):
    """
    input a hdr and a list of rows and compute the maximum printed width of each column
    """
    full_widths = []
    for l in (cached_lines + [hdr]):
        if not l: continue #skip hdr if empty
        l_widths = [width(f, max_field_size) for f in l]
        if not full_widths:
            full_widths = l_widths
        else:
            full_widths = [max([x for x in [x1,x2] if x is not None]) for x1,x2 in zip_longest(full_widths, l_widths)]
    return full_widths


def update_full_widths(full_widths, r, max_field_size):
    """
    input a list of maximum column widths and update that list given a new row
    """
    l_widths = [width(f, max_field_size) for f in r]
    full_widths_new = [max([x for x in [x1,x2] if x is not None]) for x1,x2 in zip_longest(full_widths, l_widths)]
    return full_widths_new


def print_cache(full_widths, hdr, cached_lines, max_field_size):
    if hdr:
        yield spacing_line(full_widths)
        yield pretty_print_row(full_widths, hdr, max_field_size)
    yield spacing_line(full_widths)
    for r in cached_lines:
        yield pretty_print_row(full_widths, r, max_field_size)



def get_all_lines(f_in, cache_freq, no_header, delimiter, max_field_size):
    """
    cache_freq: number of rows before the field widths are recomputed
    no_header: boolean for whether to print the first row as a header line
    delimiter
    max_field_size: trim fields with ellipsis after this width
    """
    cache_freq = int(cache_freq)
    hdr = None
    cached_lines = []
    full_widths = None
    #default max field size of ~131k crashes at times
    csv.field_size_limit(sys.maxsize)
    for i,r in enumerate(csv.reader(f_in, delimiter=delimiter)):
        if not hdr and not no_header:
            hdr = r
        elif i <= cache_freq:
            #cache first few lines
            cached_lines.append(r)
        else:
            #print cached lines all at once
            if not full_widths:
                full_widths = compute_full_widths(hdr, cached_lines, max_field_size)
                full_widths_new = full_widths
                for l in print_cache(full_widths, hdr, cached_lines, max_field_size):
                    yield l
            #continue updating full_widths with each row
            full_widths_new = update_full_widths(full_widths_new, r, max_field_size)
            if i % cache_freq == 0:
                full_widths = full_widths_new
            #print current row
            yield (pretty_print_row(full_widths,r,max_field_size))


    #if we never printed the cache above
    if not full_widths:
        full_widths = compute_full_widths(hdr, cached_lines, max_field_size)
        full_widths_new = full_widths
        for l in print_cache(full_widths, hdr, cached_lines, max_field_size):
            yield l
    yield spacing_line(full_widths_new)


if __name__ == "__main__":
    pass
