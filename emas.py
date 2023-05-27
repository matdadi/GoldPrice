import numpy as np
import json
import os
from datetime import datetime as dt
import pandas as pd
from functools import reduce

class HargaEmas:

    sumber = 'harga-emas-sd 13 mei 2023.txt'
    year = 2022

    def __init__(self, sumber=sumber):
        self.sumber = sumber

    @classmethod
    def readData(self):
        '''baca isi file sumber'''
        f = open(self.sumber)
        stringData = f.read()
        jsonData = json.loads(stringData)
        HargaEmas.data = jsonData
        return jsonData
    
    def dateFormat(jsonData, toString=True):
        '''ubah format timestamp menjadi tanggal'''
        for index, array in enumerate(jsonData):
            jsonData[index][0] = dt.fromtimestamp(array[0]//1000).isoformat()
            jsonData[index][0] = dt.strptime(jsonData[index][0], '%Y-%m-%dT%H:%M:%S')
            if toString:
                jsonData[index][0] = jsonData[index][0].strftime('%d/%m/%Y')
        return jsonData

    def dataByYear(jsonData):
        result = list(filter(lambda x: int(x[0].year) == HargaEmas.year, jsonData))
        return result
    
    def dataPerMonth(jsonData):
        mean, median, maxi, mini, result = [], [], [], [], {}
        for month in range(12):
            data = np.array(list(filter(lambda x: int(x[0].month) == month+1, jsonData)))            
            count = 0
            temp = np.array([[(HargaEmas.year,month+1,x), 0] for x in range(1,32)])
            for array in data:
                while array[0].day>temp[count,0][2]:
                    count+=1
                while array[0].day<temp[count,0][2]:
                    break
                if array[0].day==temp[count,0][2]:
                    temp[count,1] = array[1]
                    count+=1
                    continue
                
            result.update({str(month+1): temp[:,1]})

            temp = [int(x) for x in np.array(data)[:,1]]
            mean.append({month+1: round(np.average(temp))})
            median.append({month+1: round(np.median(temp))})
            maxi.append({month+1: round(np.max(temp))})
            mini.append({month+1: round(np.min(temp))})

        return mean, median, maxi, mini, result

if __name__ == '__main__':
    data = HargaEmas.readData()
    cleanData = HargaEmas.dateFormat(data, toString=False)
    data2022 = HargaEmas.dataByYear(cleanData)
    mean2022, median2022, max2022, min2022, cleanData = HargaEmas.dataPerMonth(data2022)
    cleanData = pd.DataFrame(cleanData)
    print(cleanData)
