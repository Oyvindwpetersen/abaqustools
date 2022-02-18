# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 11:47:19 2022

@author: oyvinpet
"""

#%%

try:
    from line_profiler import LineProfiler

    def do_profile(follow=[]):
        def inner(func):
            def profiled_func(*args, **kwargs):
                try:
                    profiler = LineProfiler()
                    profiler.add_function(func)
                    for f in follow:
                        profiler.add_function(f)
                    profiler.enable_by_count()
                    return func(*args, **kwargs)
                finally:
                    profiler.print_stats()
            return profiled_func
        return inner

except ImportError:
    def do_profile(follow=[]):
        "Helpful if you accidentally leave in production!"
        def inner(func):
            def nothing(*args, **kwargs):
                return func(*args, **kwargs)
            return nothing
        return inner

def get_number():
    for x in range(50000):
        yield x

@do_profile()
def expensive_function():
    for x in get_number():
        i = x ^ x ^ x
    return 'some result!'

result = expensive_function()