from genericpath import exists
import imp
from django.http import JsonResponse

from .models import Rate
from .serializers import RateSerializer
from rest_framework.decorators import api_view
import urllib.request
import json


def RatesList(request):
    DownloadCsv()
    # Get all rates from csv & serialize them & return JSON object
    rates = Rate.objects.all()
    serializer = RateSerializer(rates, many=True)
    return JsonResponse({'Rates':serializer.data})

# Check if today's csv file is downloaded.
def CheckCsv():
    file_exist = exists('bocrates.csv')
    #download it if not exists
    DownloadCsv()
        

zipfileUrl = "https://www150.statcan.gc.ca/t1/wds/rest/getFullTableDownloadCSV/10100139/en"
def DownloadCsv():
    urlResponse = urllib.request.urlopen(zipfileUrl)
    jsonTxt = json.load(urlResponse)
    print(jsonTxt)

