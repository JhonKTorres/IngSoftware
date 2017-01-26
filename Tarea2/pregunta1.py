'''
Created on 25 ene. 2017

@author: jhon
'''

from datetime import date, timedelta as td
import datetime
import math
import time

import unittest

    


#datetime.datetime.today()
#datetime.datetime(2012, 3, 23, 23, 0, 0, 0)
#datetime.datetime.today().weekday()

#tiempoDeTrabajo=[date,date];
#tarifa=[10.5,12.5]
#tarifa=
#calcularPrecio(tarifa,tiempoDeServico):
#    print("algo")
def calcularPrecio(tarifa,tiempoDeServicio):
    
    if(tarifa[0]<0 or tarifa[1]<0):
        print("Las tarifas no tienen costo positivo")
        return 0
    d1 = tiempoDeServicio[0]
    d2 = tiempoDeServicio[1]
    d3 = tiempoDeServicio[0].date()
    d4 = tiempoDeServicio[1].date()
    ds = d2-d1
    delta = d4-d3
    #convertimos el tiempo a unix para obtener los minutos
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())
    minutos = int(d2_ts-d1_ts) / 60
    if (minutos<15):
        return 0
    if(ds.days>7):
        print("Tiempo de servicio invalido, tiene mas de 7 dias")
        return 0
    horas = [-1,-1,-1,-1,-1,-1,-1,-1]
    for z in range(delta.days + 1):
        if(z==0):
            if(d1.day==d2.day):
                if((d2.hour-d1.hour==0) and d2.minute-d1.minute>0):
                    horas[z]=1
                elif( int((d2_ts-d1_ts)/60)-((d2_ts-d1_ts)/60)==0 ):
                    horas[z]=d2.hour-d1.hour+1
                else:
                    horas[z]=d2.hour-d1.hour
            else:
                horas[z]=24-d1.hour
        elif(z==delta.days):
            if(d2.minute>0):
                horas[z]=d2.hour+1
            else:
                horas[z]=d2.hour
        else:
            horas[z]=24
    costo=0
    for i in range(delta.days + 1):
        ahora = d1+ td(days=i)
        if(ahora.weekday()>=5):
            costo=costo+(tarifa[1]*horas[i])
        else:
            costo=costo+(tarifa[0]*horas[i]) 
    return costo
    
class TestCalc(unittest.TestCase):
    def test_TarifasNegativas(self):
        tarifa=[-10.5,12.5]
        d1 = datetime.datetime(2017, 1, 23,3,0)
        d2 = datetime.datetime(2017, 1, 23,3,14)
        self.assertEqual(0,calcularPrecio(tarifa,[d1,d2]))
        
    def test_Menor15Minutos(self):
        tarifa=[10.5,12.5]
        d1 = datetime.datetime(2017, 1, 23,3,0)
        d2 = datetime.datetime(2017, 1, 23,3,14)
        self.assertEqual(0,calcularPrecio(tarifa,[d1,d2]))
        
    def test_Exactamente15Minutos(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 23,3,0)
        d2 = datetime.datetime(2017, 1, 23,3,30)
        self.assertEqual(1,calcularPrecio(tarifa,[d1,d2]))
                
    def test_Mas7Dias(self):
        tarifa=[10.5,12.5]
        d1 = datetime.datetime(2017, 1, 23,3,0)
        d2 = datetime.datetime(2017, 1, 31,3,0)
        self.assertEqual(0,calcularPrecio(tarifa,[d1,d2]))
        
    def test_Casi8Dias(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 23,0,0)
        d2 = datetime.datetime(2017, 1, 29,23,59)
        self.assertEqual(216,calcularPrecio(tarifa,[d1,d2]))
        
        
    def test_soloEntresemana(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 23,0,0)
        d2 = datetime.datetime(2017, 1, 27,23,59)
        self.assertEqual(120,calcularPrecio(tarifa,[d1,d2]))       

    def test_soloFinSemana(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 28,0,0)
        d2 = datetime.datetime(2017, 1, 29,23,59)
        self.assertEqual(96,calcularPrecio(tarifa,[d1,d2]))         
    def test_ViernesSabado(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 27,0,0)
        d2 = datetime.datetime(2017, 1, 28,23,59)
        self.assertEqual(72,calcularPrecio(tarifa,[d1,d2]))
    def test_UnMinutoCobra(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 27,0,0)
        d2 = datetime.datetime(2017, 1, 27,1,1)
        self.assertEqual(2,calcularPrecio(tarifa,[d1,d2]))           
    def test_ComienzaFinSemanaTerminaEntreSemana(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 29,22,0)
        d2 = datetime.datetime(2017, 1, 30,4,0)
        self.assertEqual(8,calcularPrecio(tarifa,[d1,d2]))           
    def test_ComienzaEntreSemanaTerminaFin(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 27,22,0)
        d2 = datetime.datetime(2017, 1, 28,4,0)
        self.assertEqual(10,calcularPrecio(tarifa,[d1,d2]))  
    def test_ComienzaEntreMeses(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 31,22,0)
        d2 = datetime.datetime(2017, 2, 1,4,0)
        self.assertEqual(6,calcularPrecio(tarifa,[d1,d2]))  
    def test_ComienzaEntresemanaTerminaEntresemana(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 20,0,0)
        d2 = datetime.datetime(2017, 1, 23,4,0)
        self.assertEqual(124,calcularPrecio(tarifa,[d1,d2]))     
    def test_menosde7dias8fechas(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 16,20,0)
        d2 = datetime.datetime(2017, 1, 23,20,0)
        self.assertEqual(216,calcularPrecio(tarifa,[d1,d2]))
    def test_TerminaFinDeSemanaJusto(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 22,0,0)
        d2 = datetime.datetime(2017, 1, 23,0,0)
        self.assertEqual(48,calcularPrecio(tarifa,[d1,d2]))          
    def test_TerminaEntreDeSemanaJusto(self):
        tarifa=[1,2]
        d1 = datetime.datetime(2017, 1, 20,0,0)
        d2 = datetime.datetime(2017, 1, 21,0,0)
        self.assertEqual(24,calcularPrecio(tarifa,[d1,d2]))    
if __name__== '__main__':
    unittest.main()
    #main    

    
    

    