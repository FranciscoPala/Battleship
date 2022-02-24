import numpy as np

class Tablero():
    """Clase de un tablero de hundir la flota
    
    Inits:
        valores: np.array de dos dimensiones con las coordenadas del tablero y cada valor 
        lado_tablero: lado del tablero cuadrado
    """

    # Constructor
    def __init__(self, medidas_tablero):
        self.valores = np.full(
            shape = medidas_tablero, fill_value = 0)

    def recibir_disparo(self, row, col):
        if self.valores[row, col] == 'B':
            self.valores[row, col] == 'X'
            return True
        elif self.valores[row, col] == 'X':
            print('Disparo repetido')
            return False
        else:
            return False

    def colocar_barco(self, eslora):
        # tablero donde cuardariamos las posiciones del barco
        tempblero = self.valores.copy()
        # tablero que considera como barco las casillas prohibidas
        checkblero = self.valores.copy()
        # obtenemos la lista de las coordenadas (x,y) en donde hay barcos
        idx=np.where(checkblero == 1)
        ones = list(zip(idx[0], idx[1]))
        # expandir a casillas colindantes
        for row, col in ones:
            if (row-1) >= 0:
                checkblero[(row-1), col] = 1
            if (row+1) < checkblero.shape[0]:
                checkblero[(row+1), col] = 1
            if (col-1) >= 0:
                checkblero[row, (col-1)] = 1
            if (col+1) < checkblero.shape[1]:
                checkblero[row, (col+1)] = 1
        # version del tablero modifica el bucle y que si no es pos valida se resetea
        checkblero_postbarco = checkblero.copy()
        # intentamos poner un barco 10000 veces
        for i in range(10000):
            # elige orientación
            orient = np.random.choice(['N', 'S', 'E', 'O'])
            # si la orientación es norte las unicas posiciones iniciales 
            # permitidas son [x,y] para x = [eslora-1,lado); y= [0,lado) 
            if orient == 'N':
                fila = np.random.randint(eslora-1, tempblero.shape[0])
                columna =  np.random.randint(0, tempblero.shape[1])
                tempblero[fila:(fila-eslora), columna] = 1
                checkblero_postbarco[fila:(fila-eslora), columna] = 1
            # si la orientación es sur las unicas posiciones iniciales permitidas 
            # son [x,y] para x = [0,lado-eslora]; y= [0,lado) 
            elif orient == 'S':
                fila = np.random.randint(0, tempblero.shape[0]-(eslora-1))
                columna = np.random.randint(0, tempblero.shape[1])
                tempblero[fila:(fila+eslora), columna] = 1
                checkblero_postbarco[fila:(fila+eslora), columna] = 1
            # si la orientación es este las unicas posiciones iniciales permitidas 
            # son [x,y] para x = [0, lado); y= [0,lado-eslora]
            elif orient == 'E':
                fila = np.random.randint(0, tempblero.shape[0])
                columna = np.random.randint(eslora-1, tempblero.shape[1])
                tempblero[fila, columna:(columna+eslora)] = 1
                checkblero_postbarco[fila, columna:(columna+eslora)] = 1
            # si la orientación es oeste las unicas posiciones iniciales permitidas 
            # son [x,y] para x = [eslora-1,lado); y= [0,lado)
            else:
                fila = np.random.randint(0, tempblero.shape[0])
                columna = np.random.randint(0, tempblero.shape[1]-(eslora-1))
                tempblero[fila, columna:(columna+eslora)] = 1
                checkblero_postbarco[fila, columna:(columna+eslora)] = 1
            # para saber si el barco esta bien colocado, la diff entre 
            diffs = checkblero_postbarco.sum() - checkblero.sum()
            if diffs == eslora:
                self.valores = tempblero
                break
            # si no suman eslora posicion incorrecta -> reset
            else:
                tempblero = self.valores.copy()
                checkblero_postbarco = checkblero.copy()
            # si llegamos al final del bucle
            if i == 9999:
                print('No se ha encontrado una posición válida')
        return None







