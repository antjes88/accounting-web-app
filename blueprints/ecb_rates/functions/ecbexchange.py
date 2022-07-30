from CommonResources.Classes.common_resources import *
import requests as req
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from xml.etree import ElementTree as Et
from postgresql_interface.postgresql_interface import PostgreSQL
import datetime as dt
import warnings

warnings.filterwarnings('ignore')

DAYS_TO_REGISTER = 10
ECB_URL = "https://sdw-wsrest.ecb.europa.eu/service/data/EXR/D.GBP+USD.EUR.SP00.A/?startPeriod=%s&endPeriod=%s"


def from_xml_to_dataframe(response_text):
    """An example of the response can be found on tests\\data"""
    root = Et.fromstring(response_text)

    exchange_df = pd.DataFrame()
    for serie in root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Series'):
        df = pd.DataFrame()
        for obs in serie.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Obs'):
            date, exchange_rate = None, None
            for child in obs.iter():
                if 'ObsDimension' in child.tag:
                    date = child.attrib['value']
                if 'ObsValue' in child.tag:
                    exchange_rate = float(child.attrib['value'])
            if date and exchange_rate:
                df = df.append(pd.DataFrame({'Fecha': [date], 'Value': [exchange_rate]}))

        for value in serie.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic}Value'):
            if value.attrib['id'] == "CURRENCY":
                df['CurrencyISOCode'] = value.attrib['value']

        exchange_df = exchange_df.append(df).reset_index(drop=True)

    exchange_df = exchange_df.pivot(
        index='Fecha', columns='CurrencyISOCode', values='Value').reset_index(
            ).rename(columns={'GBP': 'Libra', 'USD': 'Dolar'})
    exchange_df.columns.name = None

    exchange_df['Createdby'] = 'System'
    exchange_df['Created'] = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    exchange_df = exchange_df[exchange_df['Libra'].notna()]
    exchange_df = exchange_df[exchange_df['Dolar'].notna()]

    return exchange_df


def get_exchange_rates_from_ecb():
    try:
        session = req.Session()
        retry = Retry(total=3, status_forcelist=[429, 500, 502, 504], backoff_factor=0.1)  # Reach 186 secs
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        date_from = str(dt.datetime.date(dt.datetime.now()) - dt.timedelta(DAYS_TO_REGISTER))
        date_to = str(dt.datetime.date(dt.datetime.now()))
        response = session.get(ECB_URL % (date_from, date_to))

        exchange_df = from_xml_to_dataframe(response.text)

        db_conn = PostgreSQL(os.environ['HEROKU_POSTGRESQL_PUCE_URL'])
        db_conn.delete_from_table('bce.EuroaRatio', exchange_df['Fecha'].to_frame())
        db_conn.insert_table('bce.EuroaRatio', exchange_df)

        return 'Success'

    except Exception as message:
        return message
