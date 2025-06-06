# Database handling Imports

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Scripts.partyMaster import PartyMaster
from Scripts.resultMaster import ResultMaster
from Scripts.unitMaster import UnitMaster

UnitMaster.create()
PartyMaster.create()

UnitMaster.addData('refrenceMaterial/unitMaster.xlsx')
PartyMaster.addData('refrenceMaterial/partyMaster.xlsx')
ResultMaster.createAll()