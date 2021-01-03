# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 00:27:54 2021

@author: Anthony Terrones
"""
#LIBRERIAS
import time
import wikipedia
import os
from datetime import datetime

#VARIABLES
Tienda = [['001','LED',500,'0.20'],['002','Resistor',200,'0.50'],['003','Potenciometro',350,'1.00'],
          ['004','Capacitor',150,'1.50'],['005','Triac',100,'2.50'],['006','Transistor',250,'5.00'],
          ['007','Servomotor',50,'25.00'],['008','LDR',150,'3.00'],['009','Arduino UNO',30,'30.00']]

#CLASES
class Usuario:
    
    def __init__(self,nombre,DNI):
        self.nombre = nombre
        self.DNI = DNI
        
    def Comprar(self,Carrito):
        prod = input("Ingrese el código y cantidad del producto que quiere comprar separados por un espacio: ")
        compra_n = prod.split()
        Carrito.append(compra_n)
    
    def Cancelar_compra(self):
        print("Algo salió mal... El programa se cerrará en 5 segundos...")
        time.sleep(5)
        
class Producto:
    
    def Comprar(self,cant,indice):
        Tienda[indice][2] = Tienda[indice][2]-cant
        
    def Info(self,indice):
        wikipedia.set_lang("es")
        alfa = Tienda[indice][1]
        busqueda = wikipedia.summary(alfa , sentences = 5 , chars = 0 , auto_suggest = True , redirect = True ) 
        print(busqueda)   
        
        
#FUNCIONES
def Borrar_Pantalla():
    os.system("cls")
    
def Presentacion(Cliente):
    print(" Buen día señor(a) {} \n BIENVENIDO A ATERRE ELECTRONICS S.A.C".format(Cliente.nombre))
    print(" A continuación tiene el cátalago de productos disponibles: \n")

def Catalogo(Tienda):
    Tabla = """\
╒═════════════════════════════════════════════════════════════╕
| CÓD      PRODUCTO           UNIDADES           PRECIO       |
| IGO                        DISPONIBLES      UNITARIO(S/.)   |
|═════════════════════════════════════════════════════════════|
{}
╘═════════════════════════════════════════════════════════════╛\
"""
    Tabla = (Tabla.format('\n'.join("|  {:<4}   {:<15} {:>10} {:>18}       |".format(*fila) for fila in Tienda)))
    print(Tabla)
    print(" \n OPCIONES: \n  1. COMPRAR \n  2. INFORMACIÓN SOBRE PRODUCTOS \n  3. SALIR \n")
    
def Boleta_Imprimir(Prod,Total,Cliente):
    fecha = datetime.now()
    Boleta = """\
╒═══════════════════════════════════════════════════════════════════╕
| CANT.       PRODUCTOS            P. UNIT.         IMPORTE (S/.)   |
|═══════════════════════════════════════════════════════════════════|
{}
╘═══════════════════════════════════════════════════════════════════╛\
"""

    Totales = """\
                                 ╒══════════════════════════════════╕
{}                              
                                 ╘══════════════════════════════════╛\
"""

    Boleta = (Boleta.format('\n'.join("|  {:<6}   {:<15} {:>13} {:>18}        |".format(*fila) for fila in Prod)))

    Totales = (Totales.format('\n'.join("                                 | {:<14} |   S/. {:>8}  |".format(*fila) for fila in Total)))

    print('╒═══════════════════════════════════════════════════════════════════╕')
    print('|                    ATERRE ELECTRONICS S.A.C                       |')
    print('╘═══════════════════════════════════════════════════════════════════╛')
    print(' Usuario: {}                 DNI : {}  '.format(Cliente.nombre,Cliente.DNI))
    print(' Fecha y hora: {}'.format(fecha))
    print(Boleta)
    print(Totales)
    
def Seguir():
    rpta = input(" Si desea realizar otra operación introduzca SI, si no desea continuar presione enter. ").upper()
    if rpta == 'SI':
        Programa()
    else:
        print(" El programa se cerrará en 5 segundos...")
        time.sleep(5)
    
def OPC_1(Cliente):
    Carrito = []
    num = int(input(" Indique cuántos productos diferentes desea adquirir: "))   
    num1 = num
    while num>0:
        Cliente.Comprar(Carrito)
        num = num-1
    for i in range(num1):
        indice = int(Carrito[i][0][2])-1
        cant = int(Carrito[i][1])
        Producto().Comprar(cant,indice)
        
    Precios = []
    for i in range(num1):
        alfa = int(Carrito[i][0][2])
        pre_unit = float(Tienda[alfa-1][3])
        precio_prod = round(pre_unit*(float(Carrito[i][1])),2)
        Precios.append(precio_prod)

    pre_total_calc = sum(Precios)
    IGV_calc = pre_total_calc*0.18
    TOTAL_calc = pre_total_calc*1.18
    pre_total = "{0:.2f}".format(pre_total_calc)
    IGV = "{0:.2f}".format(IGV_calc)
    TOTAL = "{0:.2f}".format(TOTAL_calc)

    Productos_comprados = []
    for i in range(num1):
        alfa = int(Carrito[i][0][2])-1
        prod = [Carrito[i][1],Tienda[alfa][1],Tienda[alfa][3],Precios[i]]
        Productos_comprados.append(prod) 
    
    TOT = [['SUBTOTAL',pre_total],['IGV (18.00%)',IGV],['TOTAL',TOTAL]]
    
    Borrar_Pantalla()
    
    print(" Usted eligió comprar: ")
    for i in range(num1):
        print(Carrito[i])
    rpta1 = input(" Confirme su compra con un SI para imprimir su boleta... Presione enter para cancelar compra...").upper()
    Borrar_Pantalla()
    
    if rpta1 == 'SI':
        Boleta_Imprimir(Productos_comprados,TOT,Cliente)
    else:
        Cliente.Cancelar_compra()

def OPC_2():
    indice = int(input(" Ingrese el código del producto del cual desea información: "))-1
    print("\n \n")
    Producto().Info(indice)
    
def OPC_3():
    print(" Cerrando programa en 5 segundos...")
    time.sleep(5)

#PROGRAMA PRINCIPAL
def Programa():
    
    nombre = input(" Porfavor, ingrese su nombre y apellido: ")
    DNI = input(" Ingrese su número de DNI: ")
    Borrar_Pantalla()
    
    Cliente = Usuario(nombre,DNI)
    Presentacion(Cliente)
    Catalogo(Tienda)
    
    try:
        opc = int(input(" Ingrese el número de opción que desea realizar: "))
        Borrar_Pantalla()
       
        if opc == 1:
            OPC_1(Cliente)
            Seguir()
        elif opc == 2:
            OPC_2()
            Seguir()
        elif opc == 3:
            OPC_3()
    except:
       print(" Ocurrió un error durante la ejecución del programa... \n")
       Seguir()
            

if __name__=="__main__":
    Programa()