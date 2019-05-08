import sys
import os
import linecache
import inspect
from oslo_log import log
from copy import deepcopy
import functools
import ast


class LineProfiler:
    """ A profiler that records the args of function for each line """
    
    def __init__(self, **kw):
        self.functions = list()
        self.code_map = {}
        self.code = None
        self.enable_count = 0

    def __call__(self, func):
        self.add_function(func)
        f = self.wrap_function(func)
        f.__module__ = func.__module__
        f.__name__ = func.__name__
        f.__doc__ = func.__doc__
        f.__dict__.update(getattr(func, '__dict__', {}))
        return f

    def add_function(self, func):
        """ Record line profiling information for the given Python function.
        """
        try:
            # func_code does not exist in Python3
            code = func.__code__
        except AttributeError:
            import warnings
            warnings.warn("Could not extract a code object for the object %r"
                          % (func,))
            return
        if code:
            self.code = code
            self.functions.append(func)

    def wrap_function(self, func):
        """ Wrap a function to profile it.
        """

        def f(*args, **kwds):
            self.enable_by_count()
            try:
                result = func(*args, **kwds)
            finally:
                self.disable_by_count()
            return result
        return f

    def enable_by_count(self):
        """ Enable the profiler if it hasn't been enabled before.
        """
        if self.enable_count == 0:
            self.enable()
        self.enable_count += 1

    def disable_by_count(self):
        """ Disable the profiler if the number of disable requests matches the
        number of enable requests.
        """
        if self.enable_count > 0:
            self.enable_count -= 1
            if self.enable_count == 0:
                self.disable()

    def get_relevant_names(self, source,tree):
        return [node for node in ast.walk(tree) if isinstance(node, ast.Name)]


    def get_relevant_values(self, source, frame, tree):
        names = self.get_relevant_names(source, tree)
        values = []
        for name in names:
            text = name.id
            col = name.col_offset
            if text in frame.f_locals:
                val = frame.f_locals.get(text, None)
                values.append((text, col, val))
            elif text in frame.f_globals:
                val = frame.f_globals.get(text, None)
                values.append((text, col, val))
        values.sort(key=lambda e: e[1])
        return values
        
    def tracer(self, frame, event, arg):
        """Callback for sys.settrace"""
        relevant_locals = {}
        if  event in ('line', 'return', 'eventcall') and self.code == frame.f_code:
            lineno = frame.f_lineno
            filename = frame.f_code.co_filename
            source = linecache.getline(filename,lineno)
            source = source.strip()
            if source.endswith(":"):
                return
            tree = ast.parse(source, mode='exec')
            values = self.get_relevant_values(source,frame,tree)
            lines = self.format_frame(values)
            if event == 'return':
                lineno += 1
            self.code_map[lineno] = lines
        return self.tracer

    def __enter__(self):
        self.enable_by_count()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disable_by_count()

    def enable(self):
        sys.settrace(self.tracer)

    def disable(self):
        self.last_time = {}
        sys.settrace(None)

    def format_frame(self, relevant_values):
        lines = []
        for i in reversed(range(len(relevant_values))):
            para, col, val = relevant_values[i]
            lines.append("%s=%s" %(para, val))
        return lines


def show_results(prof, stream=None, precision=3):
    if stream is None:
        stream = sys.stdout
    code = prof.code
    filename = code.co_filename
    if filename.endswith((".pyc", ".pyo")):
        filename = filename[:-1]
    if not os.path.exists(filename):
        sys.stdout.write('ERROR: Could not find file %s' %filename)
        if filename.startswith("ipython-input") or filename.startswith("<ipython-input"):
            sys.stdout.write("NOTE: %mprun can only be used on functions defined in "
                  "physical files, and not in the IPython environment.")
    first_line = code.co_firstlineno
    while True:
        line = linecache.getline(filename,first_line)
        if  line.startswith("\n"):
            break
        sys.stdout.write(line)
        if first_line in prof.code_map and prof.code_map.get(first_line):
            sys.stdout.write(">>>" +" ".join(prof.code_map.get(first_line))+"\n")
        first_line += 1
    sys.stdout.write('\n\n')


def profile(func, stream=None):
    """
    Decorator that will run the function and print a line-by-line profile
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        prof = LineProfiler()
        val = prof(func)(*args, **kwargs)
        show_results(prof, stream=stream)
        return val

    return wrapper
