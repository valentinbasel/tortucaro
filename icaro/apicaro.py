#!/usr/bin/env python
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import serial
from os import system
import time
# Configuracion de los valores iniciales del puerto serie
# estos valores son los que necesita la placa icaro np03 para poder recibir informacion desde el puerto
# el valor de PUERTO es el que puede variar en funcion de la configuracion de la pc donde se conecte

#-- valores por defecto de configuracion
class puerto():
    PUERTO='/dev/ttyUSB0' # valor inicial por defecto
    BAUDIOS=9600
    BYTESIZE=8
    PARITY='N'
    STOPBIT=1
    TIMEOUT=1
    XONXOFF=False
    RTSCTS=False
    DSRDTR=False
    RS232=serial.Serial()
    def __init__(self):
        pass

    def iniciar(self):
        try:
            self.RS232.port = self.PUERTO
            self.RS232.baudrate = self.BAUDIOS
            self.RS232.bytesize = self.BYTESIZE
            self.RS232.parity=self.PARITY
            self.RS232.stopbit=self.STOPBIT
            self.RS232.timeout=self.TIMEOUT
            self.RS232.xonxoff=self.XONXOFF
            self.RS232.rtscts=self.RTSCTS
            self.RS232.dsrdtr=self.DSRDTR
            self.RS232.open()
            return True
        except:
            return False 


    def cerrar(self):
        try:
            self.RS232.close()
            return True
        except:
            return False


       
    def activar(self,valor):
        """ 
            la funcion activar envia el caracter s al puerto serie para preparar la placa
            icaro para leer el siguiente caracter (valor) y demultiplexarlo en sus 8 pines de salida.
        """
        if self.RS232.isOpen():   
            self.RS232.write("s")
            self.RS232.write(chr(int(valor)))
            return True
        else:
            return False

    def leer(self,sensor):
        """ 
            la funcion leer envia el caracter e al puerto serie para preparar la placa
            icaro para leer el siguiente caracter (valor) que representa uno de los 6 sensores de la placa.
            devuelve 0 o el valor del sensor (1,2,3,4,5 o 6) si este esta activado.
        """
        if sensor > 7 or sensor <1:
            return False
        dato= "e" + str(sensor)
        try:
            self.RS232.write(dato)
            respuesta=self.RS232.read()
            return respuesta
        except:
            return False

    def activar_servo(self,valor,servo):
        """ 
            la funcion activar envia el caracter s al puerto serie para preparar la placa
            icaro para leer el siguiente caracter (valor) y demultiplexarlo en sus 8 pines de salida.
        """
        if self.RS232.isOpen():   
            self.RS232.write("m")
            self.RS232.write(chr(int(valor)))
            self.RS232.write(chr(int(servo))) 
            return True
        else:
            return False

    def sonido(self,audio,valor_puerto):
        """ 
            la funcion activar envia el caracter s al puerto serie para preparar la placa
            icaro para leer el siguiente caracter (valor) y demultiplexarlo en sus 8 pines de salida.
        """
        if self.RS232.isOpen():   
            self.RS232.write("a")
            self.RS232.write(chr(int(audio)))            
            self.RS232.write(chr(int(valor_puerto)))
            time.sleep(0.01)
            self.RS232.write("s")
            self.RS232.write(chr(0))              
            return True
        else:
            return False
