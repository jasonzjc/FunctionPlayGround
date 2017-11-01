# -------------------------------------------------- #
#  Jeff Zhao
#  11/01/3017
#
#  turn off the output or redirect it to a log file or an object
# -------------------------------------------------- #
import os
import sys
from contextlib import contextmanager

@contextmanager
def silence_stdout(new_target=None):
    """
    Discard stdout (i.e. write to null device) or
    optionally write to given file-like object.
    """
	
    if new_target is None:
		new_target = open(os.devnull, "w")
    old_target = sys.stdout 
    try:
        sys.stdout = new_target
        yield new_target
    finally:
        sys.stdout = old_target
		
if __name__ == '__main__':
    with silence_stdout():
        print("will not print")
        print("will not print either")

    print("this will print")