#!/usr/bin/env python
import xlrd
import csv
import sys
import xml
import jtutils
from . import plook
import six
import json
import ast
import demjson
###
def any2csv(txt, xls_sheet=None, xls_sheet_names=None, path=[], summary=False, to_stdout=False):
    try:
        xls2csv(txt, xls_sheet, summary, to_stdout)
    except xlrd.biffh.XLRDError:
        pass

    try:
        json2csv(txt, path, summary, to_stdout)
    except (SyntaxError, demjson.JSONDecodeError):
        pass

    try:
        xml2csv(txt, path, summary, to_stdout)
    except xml.parsers.expat.ExpatError:
        pass

    try:
        python2csv(txt, path, summary, to_stdout)
    except NameError:
        pass

    raise Exception("ERROR: File doesn't match xls, json, xml or python format!" + "\n")


def xls2csv(txt, xls_sheet, summary, to_stdout=False):
    rows = read_xls(txt, xls_sheet, summary)
    return process_rows(rows, to_stdout)

def json2csv(txt, path, summary=False, to_stdout=False):
    dict_list_obj = parse_json(txt)
    if summary:
        field_summary(dict_list_obj)
        sys.exit()
    rows = [r for r in process_dict_list_obj(dict_list_obj, path)]
    return process_rows(rows, to_stdout)

def xml2csv(txt, path, summary=False, to_stdout=False):
    dict_list_obj = parse_xml(txt)
    if summary:
        field_summary(dict_list_obj)
        sys.exit()
    rows = [r for r in process_dict_list_obj(dict_list_obj, path)]
    return process_rows(rows, to_stdout)

def python2csv(txt, path, summary=False, to_stdout=False):
    dict_list_obj = eval(txt)
    if summary:
        field_summary(dict_list_obj)
        sys.exit()
    rows = [r for r in process_dict_list_obj(dict_list_obj, path)]
    return process_rows(rows, to_stdout)

def rows2csv(rows):
    """http://stackoverflow.com/a/9157370"""
    import io
    import csv
    if sys.version_info[0] <= 2:
        #python2 version of csv doesn't support unicode input
        #so use BytesIO instead
        #https://stackoverflow.com/a/13120279
        #TODO: does StringIO.StringIO work?
        output = io.BytesIO()
    else:
        output = io.StringIO()
    wr = csv.writer(output)
    for r in rows:
        if sys.version_info[0] <= 2:
            wr.writerow([unicode(s) for s in r])
        else:
            wr.writerow(r)
    return output.getvalue().strip()

# def to_unicode(s):
#     """ """
#     if isinstance(s, str):
#         s = s.decode("utf-8","ignore")
#     return s.encode("utf-8")

def row2csv(row):
    return rows2csv([row])

def csv2rows(csv_string, delimiter=","):
    f = six.StringIO(csv_string)
    reader = csv.reader(f,delimiter=delimiter)
    return [row for row in reader]

def csv2df(csv_string):
    """http://stackoverflow.com/a/22605281"""
    import pandas as pd
    return pd.read_csv(six.StringIO(csv_string),index_col=False)

def dict2csv(d):
    import pandas as pd
    df =  pd.DataFrame().append(d,ignore_index=True)
    return df2csv(df)

def dict2pretty(d):
    csv = dict2csv(d)
    pretty = csv2pretty(csv)
    return pretty

def df2pretty(df):
    csv = df2csv(df)
    pretty = csv2pretty(csv)
    return pretty

def df2csv(df):
    return df.to_csv(None,index=False)

def csv2pretty(txt, max_field_size=None):
    return plook.csv2pretty(txt, max_field_size=max_field_size)





def print_csv(rows):
    wr = csv.writer(sys.stdout, lineterminator="\n")
    if not rows: return
    for r in rows:
        wr.writerow([s for s in r]) #.encode("utf-8") for s in r])


def process_rows(rows, to_stdout):
    if to_stdout:
        print_csv(rows)
        sys.exit()
    else:
        return rows2csv(rows)
###

def parse_cell(cell, datemode):
    if cell.ctype == xlrd.XL_CELL_DATE:
        dt = xlrd.xldate.xldate_as_datetime(cell.value, datemode)
        return dt.strftime("%Y-%m-%d")
    elif cell.ctype == xlrd.XL_CELL_NUMBER and int(cell.value) == cell.value:
        return int(cell.value)
    elif cell.ctype == xlrd.XL_CELL_NUMBER:
        return float(cell.value)
    elif cell.ctype == xlrd.XL_CELL_ERROR:
        return "--PARSING-ERROR--"
    else:
        if sys.version_info[0] >= 3:
            return cell.value
        else:
            return cell.value.encode("utf-8")

def get_cell(sh,i,j):
    try:
        cell = sh.cell(i,j)
    except IndexError:
        cell = xlrd.sheet.Cell(xlrd.XL_CELL_TEXT,"")
    return cell


def read_xls(txt, sheet, print_sheet_names):
    #when a filename is passed, I think xlrd reads from it twice, which breaks on /dev/stdin
    #so try passing file_contents instead of filename
    wb = xlrd.open_workbook(file_contents = txt)

    sheet_names = wb.sheet_names()
    if print_sheet_names:
        sys.stdout.write("List of xls sheets: " + "\n")
        sys.stdout.write(str(sheet_names) + "\n")
        sys.exit()

    if sheet in sheet_names:
        sh = wb.sheet_by_name(sheet)
    elif jtutils.str_is_int(sheet) and int(sheet) < len(sheet_names):
        sh = wb.sheet_by_index(int(sheet))
    else:
        raise Exception("-s argument not in xls list of sheets ({})".format(str(sheet_names)))

    wr = csv.writer(sys.stdout, lineterminator="\n")
    for i in range(sh.nrows):
        r = [parse_cell(get_cell(sh,i,j), wb.datemode) for j in range(sh.ncols)]
        wr.writerow(r)

def parse_json(txt):
    try:
        dict_list_obj = json.loads(txt)
        return dict_list_obj
    except ValueError:
        pass

    try:
        #try ast if json module doesn't work (eg if there are single quotes instead of double quotes)
        #eg: https://stackoverflow.com/a/34855065
        dict_list_obj = ast.literal_eval(txt)
        return dict_list_obj
    except (SyntaxError,ValueError):
        pass

    try:
        dict_list_obj = demjson.decode(txt)
        return dict_list_obj
    except:
        raise

def parse_xml(txt):
    import xmltodict
    dict_list_obj = xmltodict.parse(txt)
    return dict_list_obj

def field_summary(dict_list_obj):
    from collections import deque
    stack = deque([(None,dict_list_obj,-1)])
    while stack:
        key, val, depth = stack.pop()
        if key: print("|   "*depth + str(key))
        if isinstance(val, list) and len(val) > 0:
            stack.append(("["+str(len(val))+"]",val[0],depth+1))
        elif isinstance(val, dict):
            for a,b in list(val.items())[::-1]:
                stack.append((a,b,depth+1))


def process_dict_list_obj(dict_list_obj, path):
    """json-style nested objects consisting of
    a (dictionary OR list) of (dictionary OR list) of (dictionary OR list) etc
    """
    if not isinstance(path, list):
        t = type(path)
        raise Exception("process_dict_list_obj function argument path requires a list, received '{path}', type {t}".format(**vars()))
    end_node = follow_path(dict_list_obj, path)
    if isinstance(end_node, list):
        cols = set()
        for n in end_node:
            if isinstance(n, dict):
                cols = cols.union(six.viewkeys(n))
            elif isinstance(n, (list,tuple)):
                #write a csv from a list of lists
                #by using a dummy header (eg 0,1,2,...)
                #@example:
                #[["a","b"],["c","d"],["e","f"]] ->
                #0,1
                #a,b
                #c,d
                #e,f
                cols = cols.union(range(len(n)))
            else:
                raise Exception("Can't convert simple list to csv.")
            # else isinstance(n, list):
            #     raise Exception("can't convert nested lists to csv -- try using a deeper path")
        cols = sorted(list(cols))
        yield cols
        for n in end_node:
            if isinstance(n, dict):
                r = [n.get(c,"") for c in cols]
                #don't use dumps on a string or it'll create an extra pair of quotes
                r = [json.dumps(x,ensure_ascii = False) if isinstance(x,(tuple,list,dict)) else x for x in r]
                yield r
            elif isinstance(n,(list,tuple)):
                r = [n[c] if (jtutils.is_int(c) and c < len(n)) else "" for c in cols]
                #don't use dumps on a string or it'll create an extra pair of quotes
                r = [json.dumps(x,ensure_ascii = False) if isinstance(x,(tuple,list,dict)) else x for x in r]
                yield r
            else:
                raise Exception("Not a dict, list or tuple!")
    elif isinstance(end_node, dict):
        cols = list(six.viewkeys(end_node))
        yield cols
        r = [end_node.get(c,"") for c in cols]
        #don't use dumps on a string or it'll create an extra pair of quotes
        r = [json.dumps(x,ensure_ascii = False) if isinstance(x,(list,dict)) else x for x in r]
        yield r
    else:
        raise_path_error()

def raise_path_error():
    raise Exception("Invalid path: path should end in a dictionary or a list, not a single item")

def follow_path(dict_list_obj, path):
    if path == []:
        return dict_list_obj

    WILDCARD = '*'
    if path[0] == WILDCARD:
        if isinstance(dict_list_obj, list):
            out = []
            for k in dict_list_obj:
                sub_path = follow_path(k,path[1:])
                if isinstance(sub_path, list):
                    out += sub_path
                elif isinstance(sub_path, dict):
                    out.append(sub_path)
                else:
                    raise_path_error()
            return out
        elif isinstance(dict_list_obj, dict):
            raise Exception("In path, only use wildcards to handle lists")
        else:
            raise Exception("Invalid path")

    if isinstance(dict_list_obj, list):
        if jtutils.str_is_int(path[0]):
            index = int(path[0])
            return follow_path(dict_list_obj[index],path[1:])
        else:
            raise Exception("Invalid path")
    elif isinstance(dict_list_obj, dict):
        if path[0] in dict_list_obj:
            key = path[0]
            return follow_path(dict_list_obj[key],path[1:])
        elif jtutils.str_is_int(path[0]):
            index = int(path[0])
            return follow_path(list(dict_list_obj.values())[index],path[1:])
        else:
            raise Exception("Invalid path")
    else:
        raise_path_error()
