# una entrada comun:
# .db $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
def procesar_linea(linea, lista):
    # primero separo el db del otro string.
    lista_linea = linea.split()

    # una vez realizado el split, quedaria una lista de dos elementos.
    # lista_linea[0] = '.db'
    # lista_linea[1] = '$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00'

    # ahora creo una lista a partir del segundo elemento de lista_linea y se la inserto a la lista pasada por parametro.
    lista.extend(lista_linea[1].replace("$", "").split(","))


def leer_archivo(archivo):
    # recibe un archivo y lo abre en modo lectura
    arch = open(archivo, "r")

    # leo una linea del archivo
    linea = arch.readline()

    # armo una lista
    lista_salida = []

    # mientras haya lineas para leer en el archivo.
    while linea:
        # de cada linea, obtengo una lista de numeros, que agrego en la lista creada
        procesar_linea(linea, lista_salida)
        # leo la siguiente linea del archivo
        linea = arch.readline()
    # una vez terminado de leer el archivo, lo cierro.
    arch.close()
    # retorno la lista
    return lista_salida


def buscar_patrones(lista, lista_salida):
    # inicializo la posicion al comienzo de la lista
    pos_ini = 0
    pos_act = 0

    # me guardo el elemento contenido en esa posicion, para compararlo luego.
    elemento_actual = lista[pos_act]

    while pos_act <= len(lista) - 2:
        #si elemento actual es igual al siguiente, tengo un patron 80.
        if elemento_actual == lista[pos_act + 1]:
            #ahora tengo que recorrer la lista hasta que deje de cumplirse el patron.
            while pos_act <= len(lista) - 2 and elemento_actual == lista[pos_act + 1]:
                #actualizo posicion actual
                pos_act += 1
                #actualizo el elemento actual
                elemento_actual = lista[pos_act]
            #cuando salgo ya no se cumplio la condicion. Me guardo el slice de la lista hasta dicha posicion.
            lista_salida.append(lista[pos_ini:pos_act + 1])

            #ahora que sali, actualizo la posicion al siguiente elemento
            pos_act += 1
            #actualizo la posicion inicial a la del siguiente elemento de la lista
            pos_ini = pos_act
            # si corresponde, actualizo el elemento actual
            if pos_act < len(lista) - 1:
                elemento_actual = lista[pos_act]
        #el siguiente patron se debe cumplir que el elemento actual sea menor al siguiente y sea secuencial.
        elif int(elemento_actual, 16) < int(lista[pos_act + 1], 16) and (abs(int(elemento_actual, 16) - int(lista[pos_act + 1], 16)) == 1):
            while pos_act <= len(lista) - 2 and int(elemento_actual, 16) < int(lista[pos_act + 1], 16) and (abs(int(elemento_actual, 16) - int(lista[pos_act + 1], 16)) == 1):
                #actualizo posicion actual
                pos_act += 1
                # actualizo el elemento actual
                elemento_actual = lista[pos_act]
            #cuando salgo ya no se cumplio la condicion. Me guardo el slice de la lista hasta dicha posicion.
            lista_salida.append(lista[pos_ini:pos_act + 1])

            # ahora que sali, actualizo la posicion al siguiente elemento
            pos_act += 1
            #actualizo la posicion inicial a la del siguiente elemento de la lista
            pos_ini = pos_act
            # si corresponde, actualizo el elemento actual
            if pos_act < len(lista) - 1:
                elemento_actual = lista[pos_act]
        #si no es ninguno de los dos casos, es de insercion manual.
        else:
            lista_salida.append(lista[pos_ini:pos_act + 1])
            # ahora que sali, actualizo la posicion al siguiente elemento
            pos_act += 1
            # actualizo la posicion inicial a la del siguiente elemento de la lista
            pos_ini = pos_act


            #si corresponde, actualizo el elemento actual
            if pos_act < len(lista) - 1:
                elemento_actual = lista[pos_act]
    # print(".....................................................PRIMERA SALIDA........................................")
    # for elemento in lista_salida:
    #     print(elemento)


# recibe una lista de listas y la recorre para definir si en principio es P80, PC0 o PM. No se tienen en cuenta aun los PF7.
def definir_patrones(lista):
    for elemento in lista:
        if len(elemento) > 1:
            if elemento[0] == elemento[1]:
                elemento.append("P80")
            elif elemento[0] < elemento[1]:
                elemento.append("PC0")
        else:
            elemento.append("PM")
    # print(".....................................................SALIDA INTERMEDIA..........................................")
    # for elemento in lista:
    #     print(elemento)


def unificar_elementos(lista, lista_salida):
    # inicializo la posicion al comienzo de la lista
    pos_act = 0

    # me guardo el elemento contenido en esa posicion, para compararlo luego.
    elemento_actual = lista[pos_act]

    # voy a recorrer la lista hasta el anteúltimo elemento
    while pos_act < len(lista) - 1:
        #cada vez que se cumple un ciclo reinicio la lista de joins
        lista_joins = []
        #si el elemento actual tiene más de 5 elementos, lo inserto en la lista final sin modificar nada.
        if len(elemento_actual) >= 6:
            lista_salida.append(elemento_actual)

        #sino, tengo que verificar si puedo unificar el elemento con uno siguiente.
        else:
            #incializo un contador para verificar si tuve que unir elementos
            cont = 0
            #puedo unificar mientras la suma de los elementos de la lista actual con la siguiente sea menor o igual a 5
            #o si el elemento siguiente se inserta manualmente.
            while len(elemento_actual) - 1 + len(lista[pos_act + 1]) - 1 <= 5 or lista[pos_act + 1][-1] == "PM":
                #concateno ambos elementos sin su tipo ya que ahora van a ser PM
                lista_joins = elemento_actual[:len(elemento_actual) - 1] + lista[pos_act + 1][:len(lista[pos_act + 1]) - 1]
                #aumento el contador
                cont += 1

                #si puedo actualizar el contador, continuo, sino salgo
                if pos_act + 2 < len(lista) - 1:
                    pos_act += 2
                else:
                    break
            #si al salir del bucle no actualicé
            if cont == 0:
                #me guardo el elemento actual en la lista join
                lista_joins = elemento_actual

                #probablemente acá tenga que hacer un append de "PM". Revisar

            #sino, a la lista que arme, le agrego al final el tipo ingreso manual
            else:
                lista_joins.append("PM")

            #al terminar, agrego la lista unida a la final.
            lista_salida.append(lista_joins)

        # me voy al siguiente elemento
        pos_act += 1
        # actualizo elemento_actual
        elemento_actual = lista[pos_act]

    # for elemento in lista_salida:
    #    print(elemento)

def procesar_elemento(tipo, lista_elemento, lista_final, instruccion, max_posicion_mem):
#le resto un elemento a cada lista porque el ultimo es de identificacion
    lista_temporal = []
    if len(lista_elemento) - 1 > int(max_posicion_mem, 16):
        lista_temporal.append(str(format(int(instruccion, 16) + int(max_posicion_mem, 16), '02x')))
        if tipo == "PM":
            lista_temporal.extend(lista_elemento[:int(max_posicion_mem, 16) + 1])
        else:
            lista_temporal.append(lista_elemento[0])
        lista_final.append(lista_temporal[:])
        lista_temporal.clear()
        lista_temporal.append(str(format(int(instruccion, 16) + (len(lista_elemento) - 1) - int(max_posicion_mem, 16), '02x')))
        if tipo == "PM":
            lista_temporal.extend(lista_elemento[int(max_posicion_mem, 16):len(lista_elemento) - 1])
        else:
            lista_temporal.append(lista_elemento[0])
        lista_final.append(lista_temporal[:])
        lista_temporal.clear()
    else:
        lista_temporal.append(str(format(int(instruccion, 16) + (len(lista_elemento) - 1), '02x')))
        if tipo == "PM":
            lista_temporal.extend(lista_elemento[:len(lista_elemento) - 1])
        else:
            lista_temporal.append(lista_elemento[0])
        lista_final.append(lista_temporal[:])
        lista_temporal.clear()

def comprimir_elementos(lista, lista_final):
    # print(format(126, 'x'))
    #voy a recorrer la lista elemento a elemento
    for elemento in lista:
        #me fijo el ultimo elemento. Si es PM, cuento los elementos se los sumo a 00. Si es mayor a 7E el resultado,lo divido en dos instrucciones.
        if elemento[-1] == "PM":
            procesar_elemento("PM", elemento, lista_final, "00", "7e")
        if elemento[-1] == "P80":
            procesar_elemento("P80", elemento, lista_final, "80", "3f")
        if elemento[-1] == "PC0":
            procesar_elemento("PC0", elemento, lista_final, "C0", "3e")

def guardar_salida(lista_final):
    # recibe un archivo y lo abre en modo lectura
    arch = open("./salida_comprimida.txt", "w")

    for elemento in lista_final:
        arch.write(str(elemento[0]).upper() + ' | ' + ' '.join(elemento[1:]).upper() + '\n')
    arch.close()




def armar_salida():
    # armo la lista con todos los elementos del archivo
    print("ingrese nombre de archivo y ubicacion:")
    archivo = input()
    if (archivo):
        lista = leer_archivo(archivo)
        lista_salida = []
        lista_final = []
        lista_comprimida = []

        buscar_patrones(lista, lista_salida)
        definir_patrones(lista_salida)
        unificar_elementos(lista_salida, lista_final)
        comprimir_elementos(lista_final, lista_comprimida)
        guardar_salida(lista_comprimida)
    else:
        print("ERROR: el archivo no puede ser nulo.")


armar_salida()
