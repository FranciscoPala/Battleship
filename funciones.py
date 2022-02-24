import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import seaborn as sns
from variables import lista_barcos


def recibir_coordenadas():
    """Implementación de restricciones entorno al input de coordenadas"""
    keep_asking=True
    while(keep_asking):
        coord = input('Introduzca la coordenada a la que disparar: ')
        coord = coord.upper()
        # permitir quit
        if coord == 'QUIT':
            keep_asking=False
            return coord
        # checkear formato
        elif len(coord) != 2:
            pass
        elif (coord[0] in 'ABCDEFGHIJ') and (coord[1] in '0123456789'):
            keep_asking=False
            return coord
        else:
            print('Inserte un valor válido p.ej. A0, J9 ó D4')

def check_fin_partida(tab):
    """Checkea si el nuimero de aciertos en un tablero es igual a la suma de las
    esloras de los barcos 
    
    In:
        tablero: clase Tablero definida en clases.py
    """
    # cuenta aciertos
    num_aciertos = (tab.valores=='X').sum()
    # si el numero de aciertos es igual a la suma de esloras fin partida
    if sum(lista_barcos) == num_aciertos:
        return True
    else:
        return False

def plot_tableros(tablero_jugador, tablero_referencia):
    """Guarda en un .png una visualización de los tableros del jugador"""
    # pre-plot transformations
    player_trans = str.maketrans("ABX", "012")
    plot_tablero_jugador = np.char.translate(tablero_jugador, player_trans)
    plot_tablero_jugador =  plot_tablero_jugador.astype(int) 
    # en el tablero de referencia el map es distinto
    ref_trans = str.maketrans("UAX", "012")
    plot_tablero_referencia = np.char.translate(tablero_referencia, ref_trans)
    plot_tablero_referencia =  plot_tablero_referencia.astype(int)
    # size constants
    size_unit=np.array([3, 1])
    # set background colors
    plt.rcParams['figure.facecolor'] = 'black'
    # set palette and cmap normalization
    mypalette = sns.color_palette(['lightsteelblue', 'darkgray', 'firebrick'])
    mycmap = colors.ListedColormap(mypalette)
    mynorm = colors.BoundaryNorm([0, 1, 2, 3], 3)
    # set palete and cmap for second board
    mypalette2 = sns.color_palette(['black', 'lightsteelblue', 'firebrick'])
    mycmap2 = colors.ListedColormap(mypalette2)
    mynorm2 = colors.BoundaryNorm([0, 1, 2, 3], 3)
    custom_style = {
        'axes.labelcolor': 'white',
        'xtick.color': 'white',
        'ytick.color': 'white',
        'axes.grid': True,
        'grid.color': '#000000'
                    }
    sns.set_style(rc=custom_style)
    # create figure
    fig, axes = plt.subplots(1, 2, figsize = 5*size_unit)
    # ax0
    # create the heatmap
    sns.heatmap( plot_tablero_jugador, cmap=mycmap, norm = mynorm, ax=axes[0])
    axes[0].tick_params(left=False, bottom=False, grid_linewidth=2)
    axes[0].grid(which = 'major')
    axes[0].set_title('Tablero Jugador', color='white')
    # same for ax1
    sns.heatmap(plot_tablero_referencia, cmap=mycmap2, norm = mynorm2, ax=axes[1])
    axes[1].tick_params(
        left=False, bottom=False, grid_linewidth=2, grid_color='white')
    axes[1].grid(which = 'major')
    axes[1].set_title('Tablero Referencia Disparos', color='white')
    # hide cmaps
    fig.axes[-1].set_visible(False)
    fig.axes[-2].set_visible(False)
    plt.draw()
    # LABEL PARAMS
    # position of the grid ticks
    grid_ticks = [0,1,2,3,4,5,6,7,8,9]
    # position for the labels
    label_ticks = [0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5]
    axes[0].set_xticks(grid_ticks)
    axes[0].set_xticks(
        label_ticks, labels=grid_ticks, minor=True, fontsize = 12)
    axes[1].set_xticks(grid_ticks)
    axes[1].set_xticks(
        label_ticks, labels=grid_ticks, minor=True, fontsize = 12)
    # format the ticks
    letters = ['A','B','C','D','E','F','G','H','I','J']
    axes[0].set_yticks(grid_ticks)
    axes[0].set_yticks(
        label_ticks, labels = letters, minor=True, fontsize = 12, 
        rotation= 'horizontal')
    axes[1].set_yticks(grid_ticks)
    axes[1].set_yticks(
        label_ticks, labels = letters, minor=True, fontsize = 12, 
        rotation= 'horizontal')

    plt.savefig('tableros.png', bbox_inch='tight')
    plt.close('all')