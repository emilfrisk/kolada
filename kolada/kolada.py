import json
import requests
import pandas as pd

class API:

    def __init__(self, root_url = 'http://api.kolada.se/v2'):
        self.root_url = root_url

    def get_kpi(self, search_string):
        return [KPI(r['id'], r['title']) for r in requests.get(f'{self.root_url}/kpi?title={search_string}').json()['values']]

    def get_municipalities(self, search_string = ''):
        return [Municipality(r['id'], r['title']) for r in requests.get(f'{self.root_url}/municipality?title={search_string}').json()['values']]

    def get_ou(self, search_string = '', municipalities = [] ):
        return [OU(r['id'], r['title']) for r in requests.get(f'{self.root_url}/ou?municipality={",".join([m.id for m in municipalities])}&title={search_string}').json()['values']]

    def get_data(self, kpi = [], municipalities = [], years = []):

        query_string = '/data'

        if kpi:
            query_string += '/kpi/' + ','.join([k.id for k in kpi])

        if municipalities:
            query_string += '/municipality/' + ','.join([m.id for m in municipalities])

        if years:
            query_string += '/year/' + ','.join(years)

        try:
            data = requests.get(self.root_url + query_string).json()['values']
        except:
            data = []

        return data

    def get_dataframe(self, kpi = [], municipalities = [], years = [], show_kpi_title = True, show_municipality_title = True):

        data = self.get_data(kpi, municipalities, years)
        data_list = []

        for row in data:

            kpi = row['kpi']
            municipality = row['municipality']

            if show_kpi_title:
                kpi = KPI( kpi ).get_title()

            if show_municipality_title:
                municipality = Municipality( municipality ).get_title()

            for value in row['values']:
                gender = value['gender']
                data_list.append( { f'{kpi} ({gender})' : value['value'], 'year' : row['period'], 'municipality' : municipality } )


        return pd.DataFrame(data_list)


class BaseEntry:

    entry_type = 'base'

    def __init__(self, id, title = '', root_url='http://api.kolada.se/v2'):
        self.id = id
        self.title = title
        self.root_url = root_url

    def __str__(self):
        return f'{self.id} ({self.title})'

    def get_title(self):

        if self.title:
            return self.title

        return requests.get( f'{self.root_url}/{self.entry_type}/{self.id}').json()['values'][0]['title']

class KPI(BaseEntry):
    entry_type = 'kpi'

class Municipality(BaseEntry):
    entry_type = 'municipality'

class OU(BaseEntry):
    entry_type = 'ou'
