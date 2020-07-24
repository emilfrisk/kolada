from kolada import kolada
import pandas as pd
from matplotlib import pyplot as plt

api = kolada.API()

municipality = [api.get_municipalities(search_string='Eskilstuna'),api.get_municipalities(search_string='Västerås')]
kpis = api.get_kpi(search_string='Kostnad särskilt boende äldreomsorg, kr/inv 65+')

data = api.get_dataframe( kpi=kpis, municipalities=municipality, show_kpi_title=False)

print( data )
