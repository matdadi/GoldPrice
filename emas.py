import numpy as np
import json
import os
from datetime import datetime as dt

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

    def dataByFilter(jsonData):
        result = list(filter(lambda x: int(x[0].split('/')[2]) == HargaEmas.year, jsonData))
        return result
    
    def avgMonth(jsonData):
        result = []
        for month in range(12):
            data = list(filter(lambda x: int(x[0].split('/')[1]) == month+1, jsonData))
            temp = [int(x) for x in np.array(data)[:,1]]
            result.append({month+1: round(np.average(temp))})
        return result

if __name__ == '__main__':
    data = HargaEmas.readData()
    cleanData = HargaEmas.dateFormat(data)
    data2022 = HargaEmas.dataByFilter(cleanData)
    rataRata2022 = HargaEmas.avgMonth(data2022)
    print(rataRata2022)