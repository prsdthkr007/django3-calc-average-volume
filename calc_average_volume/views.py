from django.shortcuts import render, redirect
import sqlite3
from jugaad_data.nse import stock_df
from datetime import date
from sqlite3 import Error
import sys
from django.http import HttpResponse
from .models import AverageVolumeDaily, bluechip

def home(request):
    #return HttpResponse("Lets Calculate Volume Breakout")
    return render(request, 'calc_average_volume/home.html')

def fetch_volume_breakout(request):
    if request.method == 'POST':
        tradingDate = request.POST['tradingDate']
        avds = AverageVolumeDaily.objects.filter(timeCode=tradingDate).order_by('-percentChange')
        return render(request, 'calc_average_volume/fetch_volume_breakout.html', {'avds':avds})

def sql_table(request):
    if request.method == 'POST':
        tradingYear = request.POST['tradingYear']
        tradingMonth = request.POST['tradingMonth']
        tradingDay = request.POST['tradingDay']
        tradingMonthPrevious = request.POST['tradingMonthPrevious']
        ######### Variables ################
        tradingDate = request.POST['tradingDate']
        print(tradingDate)
        ####################################
        
        bluechips = bluechip.objects.all()
        
        for script_code in bluechips:
            Script_Code = script_code.scriptCode
            ############################################################################################################
            data = stock_df(symbol=Script_Code, from_date=date(int(tradingYear),int(tradingMonthPrevious),int(tradingDay)), to_date=date(int(tradingYear),int(tradingMonth),int(tradingDay)), series="EQ")
            ############################################################################################################
            Vol = 0
            O = 0
            H = 0
            L = 0
            C = 0
            prev_l = 0
            new_l = 0
            last_day_vol = 0
            Prev_List = []
            New_List = []
            num_of_days = 0
            avg_vol = 0
            precent_change = 0
            if len(data.index) > 0:
                for i in range(0,len(data.index)):
                    first = data.iloc[i]
                    Vol = float(first['VOLUME'])
                    prev_l = round(Vol, 2)
                    new_l = round(Vol, 2)
                    if i == 0:
                        prev_l = 0
                        tradingDayVol = round(Vol, 2)
                    if i == (len(data.index) - 1):
                        new_l = 0
                    Prev_List.append(prev_l)
                    New_List.append(new_l)
                    #print('previous volume {0}, new volume is {1}'.format(prev_l, new_l))
                prev_vol = round(sum(Prev_List), 2)
                new_vol = round(sum(New_List), 2)
                num_of_days = (len(Prev_List) - 1)
                avg_vol = round(sum(Prev_List)/num_of_days, 2)
                #print('Script Code {0}, avg volume {1}, last day is {2}'.format(Script_Code, avg_vol, tradingDayVol))
                if tradingDayVol > avg_vol:
                    percent_change = round((tradingDayVol - avg_vol)/avg_vol, 2)
                    AverageVolumeDaily.objects.create(scriptCode=Script_Code, timeCode=tradingDate,averageVolume=avg_vol, lastDayVolume=tradingDayVol, percentChange=percent_change)
        return redirect('home')