from datetime import datetime
from email.policy import default
from genericpath import exists
import datetime
from django.http import JsonResponse

from .models import Rate
from .serializers import RateSerializer
from rest_framework.decorators import api_view
import urllib.request
import json
import requests, zipfile
from io import BytesIO
import sqlite3, pandas as pd


allYearsRates = pd.DataFrame()
def GetRate(ratename):
    global allYearsRates
    connection = sqlite3.connect('bocratesDB.sqlite')
    cursor = connection.cursor()
    query = "SELECT VALUE from (SELECT `Financial market statistics`,Value, max(REF_DATE) from  rate where Value is not null group by 1) WHERE `Financial market statistics` == '" + ratename + "'"
    res = cursor.execute(query)
    rate = res.fetchall()[0][0]
    obj,_ = Rate.objects.get_or_create(InterestRate = rate, Date = datetime.date.today(), FinancialMarket = ratename)
    serialize = RateSerializer(obj)
    return JsonResponse({'Bank Of Canada Rates':serialize.data})


def GetBankRate(request):
    return GetRate('Bank rate')

def GetTargetRate(request):
    return GetRate('Target rate')

def Get10yearBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, 10 year')

def Get2yearBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, 2 year')

def Get3yearBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, 3 year')

def Get5yearBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, 5 year')

def Get7yearBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, 7 year')

def GetLongTermBondRate(request):
    return GetRate('Government of Canada benchmark bond yields, long term')

def GetMMFinancingRate(request):
    return GetRate('Overnight money market financing')


def RatesList(request):
    CheckCsv()
    ImportCsv()
    # Get all rates from csv & serialize them & return JSON object
    rates = Rate.objects.all()
    serializer = RateSerializer(rates, many=True)
    return JsonResponse({'Rates':serializer.data})

# Check if today's csv file is downloaded.
def CheckCsv():
    file_exist = exists('bocrates.csv')
    #download it if not exists
    if not file_exist:
        DownloadCsv()
        

zipfileUrl = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/10100139/en"
def DownloadCsv():
    result = requests.api.get(zipfileUrl)
    jsonDict = json.loads(result.content)
    downloadUrl = jsonDict['object']

    # Split URL to get the file name
    filename = downloadUrl.split('/')[-1]

    # Downloading the file
    req = requests.get(downloadUrl)
    print('Downloading Completed')

    # extracting the zip file contents
    file = zipfile.ZipFile(BytesIO(req.content))
    file.extractall()

def ImportCsv():
    global allYearsRates
    # read csv and import it into sqlite db (replace if existing)
    conn = sqlite3.connect('bocratesDB.sqlite')
    c = conn.cursor()
    allYearsRates = pd.read_csv('bocrates.csv')
    allYearsRates.to_sql('rate', conn, if_exists='replace', index = False)   

