from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SiteSerializer, CustomerSerializer, CircuitSerializer
from rest_framework.renderers import JSONRenderer

from django.shortcuts import render
from django.http import HttpResponse
import csv
import io
import re
from .models import Customer, Circuit, Site


def ipCheck(detail_info):
    if detail_info[10] == detail_info[11]:
        return False
    else:
        return True

def circuitFormateCheck(circuitId):
    return bool(re.match('\d{2}\.[A-Z]\d[A-Z]{2}\.\d{4}\.[A-Z]{4}', circuitId[4]))


def csvFileUplaod(request):
    if request.method == 'POST':
        rows_Failed=[]
        csv_file = request.FILES['uploadFile']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=';', quotechar='|'):
            info = line[0].split(',')
            validationFlage = True
            validationFlage=ipCheck(info)
            if validationFlage == True:
                validationFlage=circuitFormateCheck(info)

            if validationFlage == False:
                print(info)
            else:
                cus = Customer(customer_name=info[3] ,city=info[7] ,state= info[8],address=info[9])
                cus.save()
                cir = Circuit(customer_fk=cus ,circuit_id=info[4] ,mep_id= info[0],cir_AtoZ=info[1], cir_ZtoA=info[2])
                cir.save()
                try:
                    siteDict = {"A":5,"Z":6}
                    for key,value in siteDict.items():
                        site = Site(ip=info[value] ,hw_version=info[value] ,ip_type=key)
                        site.save()
                        cir.add_site(site)
                except:
                    print("ERROR: More than two Site ip for one circuit !")
                    
        return HttpResponse('its  done pls check the database')

    return render(request, "csvUpload.html")

def toDict(data):
    d = {}
    d['MEP_ID'] = data[0]['circuit']['mep_id']
    d['CIR_AZ'] = data[0]['circuit']['cir_az']
    d['CIR_ZA']  = data[0]['circuit']['cir_za']
    d['CUSTOMER']  = data[0]['circuit']['customer']['customer_name']
    d['CIRCUITID'] = data[0]['circuit']['circuit_id']
    d['A_HW_VERSION'] = data[0]['hw_version']
    d['Z_HW_VERSION'] = data[1]['hw_version'] 
    d['STATE']  = data[0]['circuit']['customer']['state']
    d['CITY']  = data[0]['circuit']['customer']['city']
    d['ADDRESS']  = data[0]['circuit']['customer']['address']
    d['A_IP']  = data[0]['ip']
    d['Z_IP']= data[1]['ip']              
    return d

class GetCircuit(APIView):
    def get(self,request,circuit):
        try:
            circuitID=circuit[:-1]
            print(circuitID)
            circuitObj = Circuit.objects.filter(circuit_id=circuitID)
            siteObj = Site.objects.filter(circuit__in=circuitObj)
            serializer = SiteSerializer(siteObj, many=True)
            data = serializer.data
            return Response(toDict(data))

        except Exception as e:
            return Response(e)




class GetCircuits(APIView):
        def get(self, request, name):   
           try:  
                cus_name=name[:-1]
                print(cus_name)
                customer = Customer.objects.filter(customer_name=cus_name) 
                circuits = Circuit.objects.filter(customer__in=customer)
                data_list = []
                for circuit in circuits:
                    sites = Site.objects.filter(circuit=circuit)
                    serializer = SiteSerializer(sites, many=True)
                    data = serializer.data            
                    data_list.append(toDict(data))   
                return Response(data_list)
           except Exception as e:
                 return Response(e)
 















