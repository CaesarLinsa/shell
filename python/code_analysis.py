import sys
import os
import linecache
import inspect
from oslo_log import log
from copy import deepcopy

LOG=log.getLogger(__name__)

relevant_locals={}
past_locals = {}

ignored_variables = set([
      'file_name',
      'trace',
      'sys',
      'getattr',
      'name',
      'self',
      'object',
      'consumed',
      'data',
      'ignored_variables'])


class LineProfiler:
    """ A profiler that records the amount of memory for each line """

    def __init__(self, **kw):
        self.functions = list()
        self.code_map = {}
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
        if code not in self.code_map:
            self.code_map[code] = {}
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

    def tracer(self, frame, event, arg):
        """Callback for sys.settrace"""
        global relevant_locals,past_locals
        if event in ('line', 'return') and frame.f_code in self.code_map:
            all_locals = frame.f_locals.copy()
            LOG.info("all locals:%s" %all_locals)
            for k, v in all_locals.items():
                if not k.startswith("__") and k not in ignored_variables:
                    relevant_locals[k] = v

            if past_locals and relevant_locals != past_locals:
               diff = {}
               for k in relevant_locals:
                   if k not in past_locals:
                        diff[k]=relevant_locals[k]
               relevant_locals.clear()
               relevant_locals = deepcopy(diff)
            if past_locals and relevant_locals == past_locals:
                return
            if not past_locals:
               past_locals=deepcopy(relevant_locals)
            lineno = frame.f_lineno - 1
#            if event == 'return':
#                lineno += 1
            if not self.code_map[frame.f_code].get(lineno, None):
                self.code_map[frame.f_code][lineno] = deepcopy(relevant_locals)
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

def item_kvpairs(kvpairs):
    li = []
    if kvpairs is None:
        return ""
    for k, v in kvpairs.items():
        li.append("%s=%s" % (k, v))
    return " ".join(li)

def show_results(prof, stream=None, precision=3):
    if stream is None:
        stream = sys.stdout
    template = '{0:<6} {1:<69}{2:>}\n'
    LOG.info("strat %s" %str(prof))
    for code in prof.code_map:
        LOG.info("start code:%s" %str(prof.code_map))
        var_dic = prof.code_map[code]
        if not var_dic:
            LOG.info("var_dic is None")
            continue
        filename = code.co_filename
        if filename.endswith((".pyc", ".pyo")):
            filename = filename[:-1]
        LOG.info('Filename: %s'  % filename)
        if not os.path.exists(filename):
            LOG.info('ERROR: Could not find file %s' %filename)
            if filename.startswith("ipython-input") or filename.startswith("<ipython-input"):
                print("NOTE: %mprun can only be used on functions defined in "
                      "physical files, and not in the IPython environment.")
            continue
        all_lines = linecache.getlines(filename)
        sub_lines = inspect.getblock(all_lines[code.co_firstlineno - 1:])
        linenos = range(code.co_firstlineno, code.co_firstlineno +
                        len(sub_lines))
        LOG.info("lineno:%s" %str(linenos))
        header = template.format('Line #', 'Line Contents', 'var')
        LOG.info(header + '\n')
        LOG.info("%s" %'=' * len(header))
        for i, l in enumerate(linenos):
            LOG.info("%s" %template.format(l, sub_lines[i][:-1],item_kvpairs(var_dic.get(l,None))))
        LOG.info('\n\n')


def profile(func, stream=None):
    """
    Decorator that will run the function and print a line-by-line profile
    """

    def wrapper(*args, **kwargs):
        prof = LineProfiler()
        LOG.info("profle:%s" %str(prof))
        val = prof(func)(*args, **kwargs)
        show_results(prof, stream=stream)
        return val

    return wrapper
