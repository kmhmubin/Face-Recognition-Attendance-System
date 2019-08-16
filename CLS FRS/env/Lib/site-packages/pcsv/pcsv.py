#!/usr/bin/env python
import sys
import argparse
import csv
import re
from .pindent import pindent
from jtutils import rand, is_int, str_is_float, str_is_int, md5hash, to_years, to_days, fix_broken_pipe, GroupBy, process_cfg
from collections import Counter
import six

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--infile")
    parser.add_argument("-c","--keep_list",help="csv of column names or indices. Can include currently non-existent columns")
    parser.add_argument("-C","--drop_list",help="csv of column names or indices")
    parser.add_argument("-b","--begin_code",nargs="*")
    parser.add_argument("-g","--grep_code")
    parser.add_argument("-p","--process_code",nargs="*")
    parser.add_argument("-e","--end_code",nargs="*")
    parser.add_argument("-d","--delimiter", default=",")
    parser.add_argument("--exceptions_allowed", action="store_true")
    parser.add_argument("-n","--no_header",action="store_true")
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--autofix",action="store_true")
    parser.add_argument("--set", help="load a file with no header, storing each line as an element of a set")
    parser.add_argument("--no_print",action="store_true")

    return parser

def internal_args():
    return {"input":None}

def process_cut_csv(i,delim=","):
    if i:
        i = i.split(',')
        return list(process_cut_list(i))
    else:
        return None

def process_cut_list(l, delim=","):
    for i in l:
        if "-" in i and str_is_int(i.split("-")[0]) and str_is_int(i.split("-")[1]):
            x,y = i.split('-')
            for r in range(int(x),int(y)+1):
                yield r
        elif str_is_int(i):
            yield int(i)
        else:
            yield i

#dict_and_row function to return a tuple with both unprocessed row and csv.reader() output
def csv_row_and_raw(f_in, delimiter):
    #default max field size of ~131k crashes at times
    csv.field_size_limit(sys.maxsize)
    reader = csv.reader(f_in, delimiter=delimiter)
    for row in reader:
        output = six.StringIO()
        wr = csv.writer(output, delimiter=delimiter)
        wr.writerow(row)
        l = output.getvalue().strip()
        yield l, row


#fast-ish index dictionary:
#an ordered dictionary that can be accessed by string keys
#or index values
class IndexDict():
    def __init__(self, keyhash, values):
        self._keyhash = keyhash
        self._values = values
    def __setitem__(self, key, value):
        if is_int(key):
            #'key' is actually an index,
            #must be an already existing item
            self._values[key] = value
        else:
            len_vals = len(self._values)
            index = self._keyhash.get(key,len_vals)
            if index >= len(self._values):
                self._keyhash[key] = len(self._values)
                self._values.append(value)
            else:
                self._values[index] = value
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._values.__getitem__(key)
        elif is_int(key):
            return self._values.__getitem__(key)
        elif key in self._keyhash:
            index = self._keyhash[key]
            return self._values.__getitem__(index)
        else:
            raise Exception("Couldn't find value {0} in IndexDict".format(key))
    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except:
            if default is not None:
                return default
            else:
                raise
    def __repr__(self):
        return dict((k,self._values[v]) for k,v in self._keyhash.items() if v < len(self._values[v])).__str__()
    def __len__(self):
        return len(self._values)
    def keys(self):
        return self._keyhash.keys()
    def values(self):
        return self._values


def write_line(rout):
    if isinstance(rout, IndexDict):
        rout = rout.values()
    # sys.stdout.write(','.join(rout) + '\n')
    # csv.writer(sys.stdout, lineterminator= '\n').writerows([rout],quoting=csv.QUOTE_NONE)
    csv.writer(sys.stdout, lineterminator= '\n').writerows([rout])

def proc_field(f):
    try:
        int(f)
        return int(f)
    except:
        pass
    return f

def gen_grep_code(grep_code):
    if grep_code:
        grep_string = re.findall("^/(.*)/$",grep_code)
        if grep_string:
            grep_string = grep_string[0]
            grep_code = 're.findall("{grep_string}",",".join(l))'.format(**vars())
    return grep_code


def gen_outhdr(hdr, add_list, keep_list, drop_list):
    outhdr = hdr[:]
    if keep_list:
        if not add_list:
            add_list = [x for x in keep_list if x not in hdr and not is_int(x)]
        #example tmp_dict = {0:"col1",1:"col2",2:"col3","col1":"col1","col2":"col2","col3":"col3"}
        tmp_dict = dict(list(enumerate(outhdr)) + list(zip(outhdr,outhdr)) + list(zip(add_list, add_list)))
        outhdr = [tmp_dict[x] for x in keep_list] #first include already existing columns from -c argument
    if add_list:
        outhdr += [x for x in add_list  if x not in outhdr]
    if drop_list:
        outhdr = [x for ix,x in enumerate(outhdr) if (ix not in drop_list and x not in drop_list)]
    return outhdr

def print_header(in_hdr, r, keep_list, drop_list):
    add_list = [k for k in r.keys() if k not in in_hdr] #add any keys from r that aren't in the in_hdr
    out_hdr = gen_outhdr(in_hdr, add_list, keep_list, drop_list)
    #set and print header
    csv.writer(sys.stdout, lineterminator= '\n').writerows([out_hdr])
    return out_hdr

def _check_is_list(cfg, x):
    if not isinstance(cfg[x],list):
        raise Exception(str(x) + " must be a list")

def rename_duplicate_header(hdr):
    hdr_out = []
    for h in hdr:
        cnt = 1
        if h not in hdr_out:
            hdr_out.append(h)
        else:
            new_val = h + "." + str(cnt)
            while new_val in hdr_out:
                cnt += 1
                new_val = h + "." + str(cnt)
            hdr_out.append(new_val)
    return hdr_out

# @profile
def pcsv(input_cfg=None):
    cfg = process_cfg(input_cfg, parser(), internal_args())

    if input_cfg and not cfg["input"] and not cfg["infile"]:
        raise Exception("Couldn't find input for pawk")
    if sys.stdin.isatty() and (not cfg["input"]) and (not cfg["infile"]):
        sys.stderr.write("WARNING: pcsv using /dev/stdin as default input file (-f) but nothing seems to be piped in..." + "\n")

    #for non commandline, capture the sys.stdout
    backup = None
    if input_cfg: # not running from pawk script
        backup = sys.stdout
        sys.stdout = six.StringIO()

    if cfg["input"]:
        f_in = six.StringIO(cfg["input"])
    elif not cfg["infile"]:
        f_in = sys.stdin
    else:
        if sys.version_info[0] >= 3:
            f_in = open(cfg["infile"],errors='ignore') #don't crash on invalid unicode
        else:
            f_in = open(cfg["infile"])
    if cfg["delimiter"] == "TAB":
        cfg["delimiter"] = '\t'
    elif cfg["delimiter"] == "\\t":
        cfg["delimiter"] = '\t'


    keep_list = process_cut_csv(cfg["keep_list"])
    drop_list = process_cut_csv(cfg["drop_list"])



    in_hdr = None
    out_hdr = None
    has_exceptions = False
    has_printed_incomplete_line = False
    # do_write = process_code and ("print" in process_code or "write_line" in process_code)

    begin_code = None
    process_code = None
    end_code = None
    grep_code = None

    if cfg["begin_code"]:
        _check_is_list(cfg,"begin_code")
        begin_code = [pindent(code) for code in cfg["begin_code"]]
        begin_code = [compile(code,'','exec') for code in cfg["begin_code"]]
    if cfg["grep_code"]:
        grep_code = pindent(cfg["grep_code"])
        #preprocess /.*/ syntax
        grep_code = gen_grep_code(grep_code)
        grep_code = compile(grep_code,'','eval')
    if cfg["process_code"]:
        _check_is_list(cfg,"process_code")
        process_code = [pindent(code) for code in cfg["process_code"]]
        process_code = [compile(code,'','exec') for code in process_code]
    if cfg["end_code"]:
        _check_is_list(cfg,"end_code")
        end_code = [pindent(code) for code in cfg["end_code"]]
        end_code = [compile(code,'','exec') for code in end_code]

    if begin_code:
        for code in begin_code:
            exec(code)

    if cfg["set"]:
        s = set(l.strip() for l in open(cfg["set"]))

    #main iteration loop
    for i,(l,_csvlist) in enumerate(csv_row_and_raw(f_in, delimiter = cfg["delimiter"])):
        is_header_line = (i==0 and not cfg["no_header"])
        if not in_hdr and cfg["no_header"]:
            #create a dummy header from the length of the line
            in_hdr = ["X"+str(j) for j,_ in enumerate(_csvlist)]
            hdrhash = dict((jx,j) for j,jx in enumerate(in_hdr))
            r = IndexDict(hdrhash,_csvlist) #IndexDict can be accessed by string or index (all keys must be strings)
            if not cfg["no_print"] and not out_hdr:
                out_hdr = print_header(in_hdr, r, keep_list, drop_list)
        elif not in_hdr:
            #read in the header
            in_hdr = _csvlist[:]
            if len(in_hdr) != len(set(in_hdr)):
                sys.stderr.write("WARNING: duplicated header columns. Using dummy header instead" + '\n')
                #create a dummy header from the length of the line
                in_hdr = rename_duplicate_header(_csvlist)
            hdrhash = dict((jx,j) for j,jx in enumerate(in_hdr))
            if not _csvlist:
                _csvlist = [''] * len(in_hdr)
            r = IndexDict(hdrhash,_csvlist) #IndexDict can be accessed by string or index (all keys must be strings)
            if cfg["no_print"]: #TODO: what's this block for?
                for code in process_code:
                    exec(code)

            if not cfg["no_print"]:
                out_hdr = print_header(in_hdr, r, keep_list, drop_list)
            continue #_csvlist is the header, don't continue to process as row
        else:
            #setup for regular rows
            if len(_csvlist) != len(in_hdr):
                if cfg["fix"]:
                    sys.stdout.write(l + "\n")
                    continue
                elif cfg["autofix"]:
                    continue
                elif not has_printed_incomplete_line:
                    raise Exception("ERROR: line length not equal to header length. Try running pcsv.py --fix or pcsv.py --autofix")
                    # sys.stderr.write("Header length " + str(len(hdr)) + "." + "  Row length " + str(len(_csvlist)) + "." + "\n")
                    # csv.writer(sys.stderr, lineterminator= '\n').writerows([_csvlist])
                    has_printed_incomplete_line = True
            if not _csvlist:
                _csvlist = [''] * len(in_hdr)
            r = IndexDict(hdrhash,_csvlist) #IndexDict can be accessed by string or index (all keys must be strings)

        #run process and grep code
        try:
            if grep_code and not is_header_line and not eval(grep_code):
                continue

            if process_code and (not is_header_line):
                for code in process_code:
                    exec(code)
        except:
            if not cfg["exceptions_allowed"]:
                raise
            else:
                if not has_exceptions:
                    sys.stderr.write("WARNING: exception" + '\n')
                    has_exceptions = True
                continue

        #print line
        if cfg["fix"] or cfg["no_print"]:
            pass
        else:
            rout = [str(r[h]) for h in out_hdr]
            write_line(rout)
    if end_code:
        for code in end_code:
            exec(code)
    #for sys.stdout
    if input_cfg: #not running from the script
        out = sys.stdout.getvalue()
        sys.stdout = backup
        return out
