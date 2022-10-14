from genericpath import exists
import imp
from django.http import JsonResponse

from .models import Rate
from .serializers import RateSerializer
from rest_framework.decorators import api_view
import urllib.request
import json
import requests, zipfile
from io import BytesIO
import sqlite3, pandas as pd


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
    # read csv and import it into sqlite db (replace if existing)
    conn = sqlite3.connect('bocratesDB.sqlite')
    c = conn.cursor()
    lines = pd.read_csv('bocrates.csv')
    lines.to_sql('rate', conn, if_exists='replace', index = False)

