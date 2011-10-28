# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
import gst
import gtk
from fcntl import ioctl
import os
from gettext import gettext as _
from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import media_blocks_dictionary, primitive_dictionary
from TurtleArt.tautils import get_path, debug_output
import logging
_logger = logging.getLogger('turtleart-activity icaro plugin')

import apicaro
import time
puerto = apicaro.puerto()
puerto.PUERTO='/dev/ttyUSB0'
puerto.iniciar()
class Icaro(Plugin):
    def __init__(self, parent):
        self._parent = parent
        self._status = False

    def setup(self):
        palette = make_palette('icaro',
                               colors=["#006060", "#A00000"],
                               help_string=_('paleta de bloques icaro'))

        primitive_dictionary['activar'] = self._activar
        palette.add_block('activar',  
                     style='basic-style-1arg',  
                     label=_('activar'),  
                     prim_name='activar',
                     default=[1],  
                     help_string=_('activar pines de la placa'))
        self._parent.lc.def_prim('activar', 1, lambda self, valor: primitive_dictionary['activar'](valor))

        primitive_dictionary['abrir'] = self._abrir_puerto
        palette.add_block('abrir',  
                     style='basic-style-1arg',  
                     label=_('abrir puerto'),  
                     prim_name='abrir',
                     default=['/dev/ttyUSB0'],  
                     help_string=_('abre el puerto para comunicacion con la placa'))
        self._parent.lc.def_prim('abrir', 1, lambda self, valor: primitive_dictionary['abrir'](valor))

        primitive_dictionary['retardo'] = self._retardo
        palette.add_block('retardo',  
                     style='basic-style-1arg',  
                     label=_('retardo'),  
                     prim_name='retardo',  
                     default=[1],
                     help_string=_('un retardo en milisegundo'))
        self._parent.lc.def_prim('retardo', 1, lambda self, valor: primitive_dictionary['retardo'](valor))



        primitive_dictionary['servomotores'] = self._servo
        palette.add_block('servomotores',  
                     style='basic-style-2arg',  
                     label=[_('servomotores'),'servo','grados'],  
                     prim_name='servomotores',
                     default=[1,100],  
                     help_string=_('un retardo en milisegundo'))
        self._parent.lc.def_prim('servomotores', 2, lambda self, valor,servo: primitive_dictionary['servomotores'](servo,valor))



        primitive_dictionary['sensor1'] = self._sensor2
        palette.add_block('sensor1',  
                     style='box-style',  
                     label=_('sensor1'),  
                     prim_name='sensor1',  
                     help_string=_('lee el valor del sensor 1 y devuelve 0 o 1'))
        self._parent.lc.def_prim('sensor1', 0, lambda self: primitive_dictionary['sensor1'](1))


        primitive_dictionary['sensor2'] = self._sensor2
        palette.add_block('sensor2',  
                     style='box-style',  
                     label=_('sensor2'),  
                     prim_name='sensor2',  
                     help_string=_('lee el valor del sensor 2 y devuelve 0 o 2'))
        self._parent.lc.def_prim('sensor2', 0, lambda self: primitive_dictionary['sensor2'](2))

        primitive_dictionary['sensor3'] = self._sensor2
        palette.add_block('sensor3',  
                     style='box-style',  
                     label=_('sensor3'),  
                     prim_name='sensor3',  
                     help_string=_('lee el valor del sensor 3 y devuelve 0 o 3'))
        self._parent.lc.def_prim('sensor3', 0, lambda self: primitive_dictionary['sensor3'](3))

        primitive_dictionary['sensor4'] = self._sensor2
        palette.add_block('sensor4',  
                     style='box-style',  
                     label=_('sensor4'),  
                     prim_name='sensor4',  
                     help_string=_('lee el valor del sensor 4 y devuelve 0 o 4'))
        self._parent.lc.def_prim('sensor4', 0, lambda self: primitive_dictionary['sensor4'](4))

        primitive_dictionary['sensor5'] = self._sensor2
        palette.add_block('sensor5',  
                     style='box-style',  
                     label=_('sensor5'),  
                     prim_name='sensor5',  
                     help_string=_('lee el valor del sensor 5 y devuelve 0 o 5'))
        self._parent.lc.def_prim('sensor5', 0, lambda self: primitive_dictionary['sensor5'](5))

        primitive_dictionary['sensor6'] = self._sensor2
        palette.add_block('sensor6',  
                     style='box-style',  
                     label=_('sensor6'),  
                     prim_name='sensor6',  
                     help_string=_('lee el valor del sensor 6 y devuelve 0 o 6'))
        self._parent.lc.def_prim('sensor6', 0, lambda self: primitive_dictionary['sensor3'](6))

    def _servo(self,valor,servo):
        puerto.activar_servo(servo,valor)
        
    def _activar(self,valor):
        puerto.activar(valor)

    def _retardo(self,valor):
        time.sleep(valor/1000)

    def _sensor2(self,valor):
        respuesta=puerto.leer(valor)
        return respuesta
        
    def _abrir_puerto(self,valor):
        puerto.cerrar()
        puerto.PUERTO=str(valor)
        puerto.iniciar()
