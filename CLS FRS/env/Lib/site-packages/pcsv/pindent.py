#!/usr/bin/env python
import optparse
import csv
import sys
import re
import itertools
from six.moves import zip_longest
from jtutils import threewise

def readCL():
    usagestr = "%prog"
    parser = optparse.OptionParser(usage=usagestr)
    parser.add_option("-f","--infile")
    parser.add_option("-c","--code")
    parser.add_option("-p","--print_formatted", action="store_true")
    options, args = parser.parse_args()
    if not options.infile:
        f_in = sys.stdin
    else:
        f_in = open(options.infile)
    return f_in, options.code, options.print_formatted

def _groupby(l,n):
    return zip_longest(* ( (iter(l),) * n) )

def pindent(string):
    return '\n'.join(_pindent_iter(string.split('\n')))

def _paste_lambdas(match_list):
    """don't want newline after 'lambda x:'
    """
    for las, cur, nex  in threewise(match_list):
        #TODO: replace with regex of exactly the characters allowed in python variable names (instead of strictly alphanumeric)?
        regex = "lambda[ 0-9A-Za-z]*:$"
        if las and re.findall(regex,las):
            continue
        elif re.findall(regex,cur):
            yield cur + " " + nex
        else:
            yield cur

def _split(s):
    """
    read a string representing python code and
    'print "echo; echo;"'
    """
    out_list = []
    cur_substring = ""
    in_string_type = None
    for las, cur, nex in threewise(s):
        cur_substring += cur
        if not in_string_type:
            if cur == '"' or cur == "'":
                # out_list.append((cur_substring,in_string_type))
                in_string_type = cur
                # cur_substring = cur
            elif (cur == ":" and nex == " "):
                out_list.append(cur_substring.strip())
                cur_substring = ""
            elif (cur == ";"):
                out_list.append(cur_substring.strip())
                cur_substring = ""
        else:
            if (cur == '"' or cur == "'") and las != "\\":
                #out_list.append((cur_substring,in_string_type))
                in_string_type = None
                #cur_substring = ""
    if cur_substring:
        out_list.append(cur_substring.strip())
    return out_list


def _pindent_iter(line_iter):
    indent_level = 0
    for l in (line_iter):
        # print l

        # substrings = _split_on_pystrings(l)
        #for i in range(10): if i % 2==0: print i; end; end; for i in range(5): print i; end; print 10
        # -->
        #["for i in range(10):", "if i % 2 == 0:", "print i;", "end;", "end;", "for i in range(5):", "print i;", "end;", "print 10"]

        #jtrigg@20150804: commenting below two lines to test out the _split function which should handle string literals better?
        # l2 = [i for i in re.split('(:[ $]|;[ ])',l) if i]
        # py_lines = [''.join([i for i in g if i]).strip() for g in _groupby(l2,2)]
        py_lines =  _split(l)
        py_lines = list(_paste_lambdas(py_lines))
        for l in py_lines:
            if l == "end;":
                indent_level -= 1
                continue
            if re.findall("^elif",l) or re.findall("^else",l) or re.findall("^except",l):
                indent_level -= 1
            yield ("    "*indent_level + l)
            if re.findall(":$",l):
                indent_level += 1
        # yield ("    "*indent_level + output_text)


#jtrigg@20151105 not currently being used
# def write_line(*l):
#     import csv
#     rout = [str(i) for i in l]
#     csv.writer(sys.stdout, lineterminator= '\n').writerows([rout])


if __name__ == "__main__":
    f_in, code, print_formatted = readCL()
    if code:
        code_string = code
    else:
        code_string = f_in.read()

    if print_formatted:
        sys.stdout.write(pindent(code_string) + "\n")
    else:
        exec(pindent(code_string))
