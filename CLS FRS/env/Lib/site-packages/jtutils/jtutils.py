#!/usr/bin/env python
from __future__ import absolute_import
from . import date
import itertools
import re
import os
import sys
import io
import codecs
import requests
import bs4
import six
try:
    from shlex import quote as cmd_quote #since 3.3
except ImportError:
    from pipes import quote as cmd_quote


def open_py2_py3(f):
    if f == sys.stdin:
        if sys.version_info[0] >= 3:
            f_in = codecs.getreader('utf8')(sys.stdin.detach(), errors='ignore')
        else:
            f_in = sys.stdin
    else:
        if sys.version_info[0] >= 3:
            f_in = open(f, errors='ignore')
        else:
            f_in = open(f)
    return f_in

def pd_read_csv(f, **args):
    #In python3 pd.read_csv is breaking on utf8 encoding errors
    #Solving this by reading the file into StringIO first and
    #then passing that into the pd.read_csv() method
    import pandas as pd
    f = six.StringIO(open_py2_py3(f).read())
    return pd.read_csv(f, **args)

#trying to deprecate / stop using this function
# def df_to_bytestrings(df):
#     #avoid bug where pandas applymap() turns length 0 dataframe into a series
#     if len(df) == 0:
#         return df
#     else:
#         #convert the columns as well
#         df.columns = [to_bytestring(c) for c in df.columns]
#         return df.applymap(to_bytestring)

#trying to deprecate / stop using this function
# def to_bytestring(obj):
#     """avoid encoding errors when writing!"""
#     if isinstance(obj, str):
#         return unicode(obj, errors="ignore").encode("ascii","ignore")
#     elif isinstance(obj, unicode):
#         return obj.encode("ascii","ignore")
#     elif isinstance(obj, list):
#         return str([to_bytestring(e) for e in obj])
#     else:
#         return obj

def to_days(dt_str):
    if dt_str == "": return ""
    return date.Date(dt_str).to_days()

def to_years(dt_str):
    if dt_str == "": return ""
    return date.Date(dt_str).to_years()

def to_YYYYMMDD(dt_str):
    if dt_str == "": return ""
    return date.Date(dt_str).to_YYYYMMDD()

def days_to_YYYYMMDD(days):
    return date.Date.from_days(days).to_YYYYMMDD()

def years_to_YYYYMMDD(years):
    return date.Date.from_years(years).to_YYYYMMDD()

def today_YYYYMMDD():
    import datetime
    return datetime.datetime.now().strftime("%Y%m%d")

def date_range(start_YYYYMMDD, end_YYYYMMDD):
    return date.Date.date_range(start_YYYYMMDD, end_YYYYMMDD)

class GroupBy:
    """
    Example usage (print all triple anagrams with at least 9 letters):
    >>> less /usr/share/dict/words | pawk -b 'g = GroupBy({},key=lambda x: tuple(sorted(Counter(x).items())))' -p 'g.update([l])' -e 'print [v for v in g.values() if len(v) > 2 and len(v[0]) > 8]'
    [['dissenter', 'residents', 'tiredness'], ['countries', 'cretinous', 'neurotics'], ['earthling', 'haltering', 'lathering'], ['beastlier', 'bleariest', 'liberates'], ['reprising', 'respiring', 'springier'], ['cratering', 'retracing', 'terracing'], ['gnarliest', 'integrals', 'triangles'], ['estranges', 'greatness', 'sergeants'], ['cattiness', 'scantiest', 'tacitness'], ['enlisting', 'listening', 'tinseling'], ["magneto's", "megaton's", "montage's"], ['auctioned', 'cautioned', 'education'], ["respect's", "scepter's", "specter's"], ["cheater's", "hectare's", "teacher's"], ['emigrants', 'mastering', 'streaming']]
    """
    def __init__(self, list_of_inputs, key, value=None):
        self.key = key
        if (not value):
            self.value = lambda x: x
        else:
            self.value = value
        self.dictionary = {}
        self.update(list_of_inputs)
    def update(self, l):
        for x in l:
            k = self.key(x)
            v = self.value(x)
            self.dictionary[k] = self[k] + [v]
        return self
    def __setitem__(self, key, value):
        raise Exception("Can't set counter items")
    def __getitem__(self, x):
        if x in self.dictionary:
            return self.dictionary[x]
        else:
            return []
    def __str__(self):
        return self.dictionary.__str__()
    def keys(self):
        return self.dictionary.keys()
    def values(self):
        return self.dictionary.values()
    def items(self):
        return self.dictionary.items()

def is_int(var):
    return isinstance(var, six.integer_types)

def is_float(var):
    return isinstance(var, float)

def str_is_int(var):
    # if not isinstance(var, str) and np.isnan(var):
    #     return False
    if re.findall("^\d+$",var):
        return True
    else:
        return False

def str_is_float(var):
    try:
        f = float(var)
        # if np.isnan(f):
        #     return False
        return True
    except:
        return False

def md5hash(s):
    import md5
    return md5.md5(s).hexdigest()

def rand():
    import random
    return str(round(random.random(),4))

def fix_broken_pipe():
    #following two lines solve 'Broken pipe' error when piping
    #script output into head
    from signal import signal, SIGPIPE, SIG_DFL
    signal(SIGPIPE,SIG_DFL)

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return six.moves.zip(a,b)

def threewise(iterable):
    """s -> (None, s0, s1), (s0, s1, s2), ... (sn-1, sn, None)
    example:
    for (last, cur, next) in threewise(l):
    """
    a, b, c = itertools.tee(iterable,3)
    def prepend(val, l):
        yield val
        for i in l: yield i
    def postpend(val, l):
        for i in l: yield i
        yield val
    next(c,None)

    for _xa, _xb, _xc in six.moves.zip(prepend(None,a), b, postpend(None,c)):
        yield (_xa, _xb, _xc)

def terminal_size():
    try:
        columns = os.popen('tput cols').read().split()[0]
        return int(columns)
    except:
        return None

def lines2less(lines):
    """
    input: lines = list / iterator of strings
    eg: lines = ["This is the first line", "This is the second line"]

    output: print those lines to stdout if the output is short + narrow
            otherwise print the lines to less
    """
    lines = iter(lines) #cast list to iterator

    #print output to stdout if small, otherwise to less
    has_term = True
    terminal_cols = 100
    try:
        terminal_cols = terminal_size()
    except:
        #getting terminal info failed -- maybe it's a
        #weird situation like running through cron
        has_term = False

    MAX_CAT_ROWS = 20  #if there are <= this many rows then print to screen

    first_rows = list(itertools.islice(lines,0,MAX_CAT_ROWS))
    wide = any(len(l) > terminal_cols for l in first_rows)

    use_less = False
    if has_term and (wide or len(first_rows) == MAX_CAT_ROWS):
        use_less = True

    lines = itertools.chain(first_rows, lines)
    lines = six.moves.map(lambda x: x + '\n', lines)

    if use_less:
        lesspager(lines)
    else:
        for l in lines:
            sys.stdout.write(l)


def lesspager(lines):
    """
    Use for streaming writes to a less process
    Taken from pydoc.pipepager:
    /usr/lib/python2.7/pydoc.py
    and
    /usr/lib/python3.5/pydoc.py
    """
    cmd = "less -S"
    if sys.version_info[0] >= 3:
        """Page through text by feeding it to another program."""
        import subprocess
        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)
        try:
            with io.TextIOWrapper(proc.stdin, errors='backslashreplace') as pipe:
                try:
                    for l in lines:
                        pipe.write(l)
                except KeyboardInterrupt:
                    # We've hereby abandoned whatever text hasn't been written,
                    # but the pager is still in control of the terminal.
                    pass
        except OSError:
            pass # Ignore broken pipes caused by quitting the pager program.
        while True:
            try:
                proc.wait()
                break
            except KeyboardInterrupt:
                # Ignore ctl-c like the pager itself does.  Otherwise the pager is
                # left running and the terminal is in raw mode and unusable.
                pass

    else:
        proc = os.popen(cmd, 'w')
        try:
            for l in lines:
                proc.write(l)
        except IOError:
            proc.close()
            sys.exit()

def argmax(l,f=None):
    """http://stackoverflow.com/questions/5098580/implementing-argmax-in-python"""
    if f:
        l = [f(i) for i in l]
    return max(enumerate(l), key=lambda x:x[1])[0]

#website functions
def html_to_soup(html):
    try:
        soup = bs4.BeautifulSoup(html, "lxml")
    except:
        soup = bs4.BeautifulSoup(html, "html.parser")
    return soup

def url_to_soup(url, js=False, encoding=None, cookies={}, headers={}, params=()):
    html = _get_webpage(url, js, encoding, cookies, headers, params)
    return html_to_soup(html)

def _get_webpage(url, js=False, encoding = None, cookies={}, headers={}, params=()):
    if js:
        return _get_webpage_with_js(url)
    else:
        return _get_webpage_static(url, encoding, cookies, headers, params)

def _get_webpage_with_js(url):
    with open_driver() as driver:
        driver.get(url)
        wait_until_stable(driver)
        return driver.page_source

def _get_webpage_static(url, encoding=None, cookies={}, headers={}, params=()):
    if not isinstance(cookies,dict) or not isinstance(headers,dict):
        raise Exception("Invalid type for cookies or headers! Should be dict: {cookies},{headers}".format(**vars()))
    if not isinstance(params,tuple):
        raise Exception("Invalid type for params! Should be tuple: {params}".format(**vars()))
    if not url.startswith("http"):
        url = "http://" + url
    headers.update({'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'})
    s = requests.Session()
    RETRIES = 5
    for i in range(RETRIES):
        try:
            out = s.get(url, headers=headers, params=params, cookies=cookies, timeout=(10,10))
            if encoding:
                out.encoding = encoding
            return out.text
        except (requests.exceptions.RequestException, requests.Timeout, requests.exceptions.ReadTimeout) as e:
            if i < (RETRIES - 1):
                continue
            else:
                raise e

#a wrapper for argparse to allow either
#commandline usage or calling the function passing in a cfg
def process_cfg(input_cfg, parser, internal_args):
    #pass in input_cfg to use internally
    #or pass in parser to use with command line arguments
    def _cfgToArgs(cfg):
        out = []
        for k,v in cfg.items(): #eg "file", "myfile.avi"
            #add "--file", "myfile.avi" to the end of out
            out.append("--"+k)
            if v is True:
                continue
            else:
                out.append(str(v))
        return out

    args = {}

    if input_cfg is None:
        command_line_cfg = vars(parser.parse_args())
    else:
        #using input_cfg arguments: only populate
        #command_line_cfg with parser defaults
        command_line_cfg = vars(parser.parse_args([]))

    args.update(command_line_cfg)

    args.update(internal_args)

    if input_cfg:
        invalid_cfg = {k:v for k,v in input_cfg.items() if k not in internal_args and k not in args}
        if invalid_cfg:
            raise Exception("Invalid cfg arguments! {invalid_cfg}".format(**vars()))
        internal_cfg = {k:v for k,v in input_cfg.items() if k in internal_args or k in args}
        args.update(internal_cfg)
    return args

class CfgGen():
    def CfgGen(self):
        self.internal_args = {}
    def set_parser(parser):
        self.parser = parser
    def set_internal_args(internal_args):
        self.internal_args = internal_args
    def get_cfg(self, input_cfg=None):
        pass

class ShellCommandException(Exception):
    pass

def bash_quote(text):
    quoted = cmd_quote(text)
    if quoted[0] == "'" and quoted[-1] == "'":
        return quoted
    else:
        return "'" + quoted + "'"

def run(cmd,error=True):
    import subprocess
    pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = pipes.communicate()
    return_code = pipes.returncode
    if return_code != 0 and error:
        raise ShellCommandException("Command failed! " + "\n" + str(stderr) + "\n" + str(cmd))
    if sys.version_info[0] >= 3:
        return stdout.decode("utf-8","ignore"), stderr.decode("utf-8","ignore"), return_code
    else:
        #does this work with python2?
        return stdout.decode("utf-8"), stderr.decode("utf-8"), return_code
