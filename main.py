import numpy as np
import time
from PIL import Image
from funciones import plot_tableros, check_fin_partida, recibir_coordenadas
from clases import Tablero
from variables import dimensiones, lista_barcos, dict_filas

if __name__ == '__main__':
    # init tableros
    # jugador
    mitab = Tablero(dimensiones)
    for n in lista_barcos:
        mitab.colocar_barco(n)
    # mapear valores 
    mitab.valores = np.where(mitab.valores==1,'B','A')
    # referencia disparos
    mitab2 = Tablero(dimensiones)
    mitab2.valores = np.full(shape = dimensiones, fill_value = 'U')
    # maquina
    maqtab = Tablero(dimensiones)
    for n in lista_barcos:
        maqtab.colocar_barco(n)
    maqtab.valores = np.where(maqtab.valores==1,'B','A')
    # opciones de coordenadas para la maquina
    coord_disparo = []
    for (x,y),value in np.ndenumerate(mitab.valores):
        coord_disparo.append(str(x)+str(y))
    # while del juego
    turno_jugador = True
    keep_playing = True
    while(keep_playing):
        wait = time.sleep(0.5)
        # turno jugador
        if turno_jugador:
            print('-'*80)
            print('Turno del jugador')
            print('-'*80)
            # guarda el tablero como .png y lo enseña por pantalla
            plot_tableros(mitab.valores, mitab2.valores)
            img = Image.open('./tableros.png')
            # img.show()
            # input disparo
            text = recibir_coordenadas()
            if text == 'QUIT':
                break
            fila = dict_filas[text[0]]
            columna = int(text[1])
            # prompt
            print(
                'Disparando a la posición {f}{c}'.format(
                    f='ABCDEFGHIJ'[fila], 
                    c=columna
                ))
            # el tablero de la maquina recibe el disparo
            tocado = maqtab.recibir_disparo(int(fila),int(columna))
            # si acierto
            if tocado:
                # prompt
                print('¡Tocado!')
                # actualizar tablero ref
                mitab2.valores[fila, columna] = 'X'
                # comprobar si seguimos jugando
                if check_fin_partida(mitab2):
                    print('Fin de la partida, gana el jugador')
                    keep_playing=False
            # si fallo
            else:
                # actualizar tablero ref
                mitab2.valores[fila, columna] = 'A'
                print('Fallo')
                # cambio turno
                turno_jugador = False
        # turno maquina
        else:
            print('-'*80)
            print('Turno de la Máquina')
            print('-'*80)
            plot_tableros(mitab.valores, mitab2.valores)
            time.sleep(0.5)
            # elige disparo de la lista
            coord = np.random.choice(coord_disparo)
            fila = int(coord[0])
            columna = int(coord[1])
            # quita el disparo de la lsita
            coord_disparo.remove(coord)
            # prompt
            print(
                'Disparando a la posición {f}{c}'.format(
                    f='ABCDEFGHIJ'[fila], 
                    c=columna
                ))
            time.sleep(0.5)
            # el jugador recibe el disparo de la maquina
            tocado = mitab.recibir_disparo(fila, columna)
            # si falla cambia de turno
            if tocado == False:
                print('Fallo')
                turno_jugador = True
            else:
                print('¡Tocado!')
                # actualizamos el valor en mi tablero
                mitab.valores[fila, columna] = 'X'
                # comprobamos si con ese acierto se gana
                if check_fin_partida(mitab):
                    print('Fin de la partida, gana el la máquina')
                    keep_playing=False