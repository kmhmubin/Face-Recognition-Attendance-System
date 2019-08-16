#!/usr/bin/env python
import csv
import itertools
from collections import OrderedDict
import re
import sys
import os
import inspect
from jtutils import pairwise

def readcsv(f):
    if isinstance(f, file):
        f_in = f
        for r in _readcsv(f_in):
            yield r
    elif isinstance(f, str):
        with open(f) as f_in:
            for r in _readcsv(f_in):
                yield r
    else:
        raise


def _readcsv(f_in):
    header = None
    for line in csv.reader(f_in):
        if not header:
            header = line
        else:
            yield OrderedDict(zip(header,line))


def regex(regex, string):
    """Takes one or a list of regex-es,
    looks for them in one or a list of strings s
    and returns the first match or else empty string
    """
    if isinstance(regex,str):
        regex_list = [regex]
    else:
        regex_list = regex

    if isinstance(string,str):
        string_list = [string]
    else:
        string_list = string

    all_matches = [i for s in string_list for regex in regex_list for i in re.findall(regex,s)]
    return get_first(all_matches,"")

def get_first(l, default=None):
    if l:
        return l[0]
    else:
        return default

def csv_string(rows):
    """http://stackoverflow.com/a/9157370"""
    import io
    import csv
    output = io.BytesIO()
    writer = csv.writer(output)
    for r in rows:
        writer.writerow(r)
    return output.getvalue()



def df2csv(df):
    return df.to_csv(None,index=False)


def df2pretty(df):
    from pcsv.plook import csv2pretty
    s = df2csv(df)
    return csv2pretty(s)


def basic_logger(name, stream=sys.stderr):
    #usually called as
    #basic_logger(__name__)
    import logging
    import sys
    logger = logging.getLogger(name)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


def group_by(l, col=None):
    """Example:
    >>> l = [{"a":1},{"a":2}]
    >>> utils.group_by(l,"a")
    {1: [{'a': 1}], 2: [{'a': 2}]}
    """
    out_dict = {}
    for i in l:
        if col != None:
            out_dict.setdefault(i[col],[]).append(i)
        else:
            out_dict.setdefault(i,[]).append(i)
    return out_dict

def aggregate(l, f, col=None):
    return dict((key,f(group)) for key,group in group_by(l,col).items())



#http://stackoverflow.com/questions/5098580/implementing-argmax-in-python
def argmax(l,f=None):
    if f:
        l = [f(i) for i in l]
    return max(enumerate(l), key=lambda x:x[1])[0]

def csv2dict(infile, key, value=None, multi=False):
    #convert a csv to a dictionary:
    #infile: file to read in
    #key: name or index of the key column in the dictionary
    #value: name or index of the value column in the dictionary.
    #       if left blank, the entire column is used as the value
    #multi: allow for multiple values corresponding to each key

    #example:
    #cat text.txt
    #a,b,c
    #1,2,3
    #2,1,3
    #3,0,0

    #csv2dict(test.txt, "a", "b") -> {1:2, 2:1, 3:0}
    #csv2dict(test.txt, "a") -> {1:{a:1,b:2,c:3}, 2:{a:2,b:1,c:3}, 3:{a:3,b:0,c:0}}
    #csv2dict(test.txt, "a", "b", True) -> {1:[2], 2:[1], 3:[0]}
    dict_out = {}
    key_is_int = is_int(key) or str_is_int(key)
    if not value is None:
        value_is_int = is_int(value) or str_is_int(value)
    for r in readcsv(infile):
        if key_is_int:
            k = r.values()[int(key)]
        else:
            k = r[key]
        if k in dict_out and not multi:
            raise Exception("ERROR in csv2dict: nonunique key")
        if not value is None:
            if value_is_int:
                v = r.values()[int(value)]
            else:
                v = r[value]
        else:
            v = r
        if multi:
            dict_out.setdefault(k,[]).append(v)
        else:
            dict_out[k] = v
    return dict_out

def run(cmd):
    import subprocess
    pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = pipes.communicate()
    return_code = pipes.returncode
    return stdout, stderr, return_code

def run_report_errors(cmd):
    import sys
    out, err, return_code = run(cmd)
    if return_code != 0:
        sys.stderr.write(err + "\n")






def run_streaming(cmd):
    """run a shell command and get a streaming result
    http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate
    """
    # """
    # to run a pipe list of commands and get a streaming result
    # example:
    # To run:
    # less a | sort | head

    # INPUT:
    # #cmdlist = ["less a", "sort", "head"]

    # from:
    # http://stackoverflow.com/questions/2715847/python-read-streaming-input-from-subprocess-communicate
    # """
    import subprocess
    # proclist = []
    # for c in cmdlist:
    #     # print c
    #     if not proclist:
    #         p = subprocess.Popen(c, stdout=subprocess.PIPE, bufsize=1, shell=True)
    #     else:
    #         p = subprocess.Popen(c, stdin=proclist[-1].stdout, stdout=subprocess.PIPE, bufsize=1, shell=True)
    #     proclist.append(p)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1, shell=True)
    # last = proclist[-1]
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            yield line #original had 'yield line,' with a comma at the end, not sure why
    p.wait() # wait for the subprocess to exit



def open_unix_sorted_csv(filename, keys):
    """return a generator with lines from the sorted file
    """
    ext = filename.rsplit(".",1)[-1]
    if ext == "7z":
        open_cmd = "7z e {filename} -so 2>/dev/null".format(**vars())
    else:
        open_cmd = "less {filename}".format(**vars())
    print(open_cmd)
    cmdlist = [open_cmd+"| (read -r h; echo $h; sort)"]
    for line in run_streaming(cmdlist):
        yield line


def look(obj):
    import inspect
    if hasattr(obj, '__call__'):
        print("Function arguments: ")
        print(inspect.getargspec(obj))
        print()
    print("dir: ")
    print(dir(obj))

def check_gradient(neg_llh, grad_neg_llh, initial_estimate, *args):
    from scipy.optimize import check_grad
    from numpy.linalg import norm
    error = check_grad(neg_llh, grad_neg_llh, initial_estimate, *args)
    gradient_mag = norm(grad_neg_llh(initial_estimate, *args))
    frac = error / gradient_mag
    if abs(frac) > 1e-7:
        print("WARNING: ratio shouldn't be over 1e-7: ")
    else:
        print("INFO: ratio looks good: less than 1e-7")
    print("error: ", error)
    print("gradient_mag: ", gradient_mag)
    print("ratio: ", error/gradient_mag)

def writerow(rout):
    csv.writer(sys.stdout, lineterminator= '\n').writerows([rout])



def multithread(function_to_run, list_of_items, num_threads):
    #uses thread pooling: num_threads are generated and
    #each thread is allocated one item from list_of_items
    #and runs function_to_run(item)
    #and whenever a thread is done running an item it
    #gets another item and runs that
    from multiprocessing import Pool
    pool = Pool(processes=num_threads)
    pool.map(function_to_run, list_of_items)

def multithread_chunks(function_to_run, list_of_items, num_threads):
    #Splits up the individual elements of list_of_items
    #between num_threads.

    ####Each thread runs####
    #for item in my_thread_items:
    #  function_to_run(item)
    import threading
    def multi_function(*args):
        my_thread_items = args[0]
        # print my_thread_items
        for item in my_thread_items:
            function_to_run(item)
    chunks = chunkify(list_of_items, int(num_threads))
    threads = []
    for l in chunks:
        t = threading.Thread(target=multi_function, args=[l])
        t.daemon = True
        t.start()
        threads.append(t)

    #wait for all threads to finish before closing
    for t in threads:
        t.join()


def write_object(obj, filename):
    import pickle
    pickle.dump(obj, open(filename, 'wb'))

def read_object(filename):
    import pickle
    return pickle.load(open(filename, 'rb'))

def soup(url):
    import urllib2
    import bs4
    return bs4.BeautifulSoup(urllib2.urlopen(url).read(),"lxml")


def y_n_input(message):
    out = raw_input(message)
    while True:
        if out.lower() == "y":
            return True
        elif out.lower() == "n":
            return False
        else:
            out = raw_input("Please input y or n" + '\n')

def chunkify(l, n):
    from numpy import cumsum,array
    chunks1 = [l[i::n] for i in range(n)]
    # return chunks1
    chunk_sizes = [len(c) for c in chunks1]
    sumlist = cumsum(array([0] + chunk_sizes))
    chunks2 = [l[i:j] for i,j in pairwise(sumlist)]
    return chunks2



def check_memory_usage():
    #http://stackoverflow.com/questions/938733/total-memory-used-by-python-process
    #in bytes
    import resource
    return 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_maxrss






def is_int(var):
    return isinstance( var, ( int, long ) )

def str_is_float(var):
    try:
        f = float(var)
        # if np.isnan(f):
        #     return False
        return True
    except:
        return False

def str_is_int(var):
    # if not isinstance(var, str) and np.isnan(var):
    #     return False
    if re.findall("^\d+$",var):
        return True
    else:
        return False

# def mean(l):
#     return sum(l) / float(len(l))

def var(l):
    e_x = sum(l) / float(len(l))
    e_x2 = sum(x**2 for x in l) / float(len(l))
    return e_x2 - e_x**2



class IndexDict(OrderedDict):
    #Ordered Dictionary can be indexed by integers or
    #strings. Keys cannot be integers to distinguish from indices
    def __setitem__(self, key, value):
        if is_int(key):
            #'key' is actually an index
            k = self.keys()[key]
            OrderedDict.__setitem__(self,k,value)
        else:
            OrderedDict.__setitem__(self,key,value)
    def __getitem__(self, key):
        if isinstance( key, slice):
            return self.values().__getitem__(key)
            # jtrigg@20141213: below is super slow! Above faster.
            # return [self[ii] for ii in xrange(*key.indices(len(self)))]
        elif is_int(key):
            return self.values().__getitem__(key)
        else:
            return OrderedDict.__getitem__(self,key)
    def findall(self,regex):
        return [i for v in self.values() for i in re.findall(regex,str(v))]



if __name__ == "__main__":
    print(group_by([1,2,1,3,2]))
    print(group_by([{"a":1,"b":2},{"a":0,"b":1}],"a"))
    print(group_by([[1,2],[1,3],[3,4]],1))
    print(aggregate([[1,2],[1,3],[3,4]],len,0))


    print(list(pairwise([1,2,3,4])))
