import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Scripts.resultMaster import ResultMaster
x = (int(f"{(ResultMaster.getlastTCno("1235-Twintech") + 1):07d}"))
print((x))