import sys
import os

kukulkan = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
py_kukulkan = os.path.join(kukulkan, 'python')

sys.path.append(py_kukulkan)

import autorig.
