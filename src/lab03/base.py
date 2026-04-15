import sys
import os
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_path)
sys.path.append(os.path.join(src_path, 'lab01'))

from lab01.model import Apartment