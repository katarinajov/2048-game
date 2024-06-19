import numpy as np

# Broj mogućih poteza u igri (levo, gore, dole, desno)
NUMBER_OF_MOVES = 4
# Broj simulacija koje će se izvesti za analizu performansi AI
SAMPLE_COUNT = 50

# Parametri za skaliranje pretraga po potezu i dužine pretrage
SPM_SCALE_PARAM = 10 # Osnovni broj pretraga po potezu
SL_SCALE_PARAM = 4 # Osnovna dužina pretrage
SEARCH_PARAM = 200 # Interval za povećanje pretraga i dužine pretrage

# Import potrebnih funkcija iz modula game_functions
from game_functions import initialize_game, random_move, \
    move_down, move_left, \
    move_right, move_up, \
    check_for_win, add_new_tile

# Funkcija za izračunavanje parametara pretrage na osnovu broja poteza
def get_search_params(move_number):
    searches_per_move = SPM_SCALE_PARAM * (1 + (move_number // SEARCH_PARAM))
    search_length = SL_SCALE_PARAM * (1 + (move_number // SEARCH_PARAM))
    return searches_per_move, search_length

def ai_move(board, searches_per_move, search_length):
    # Lista mogućih početnih poteza (funkcija koje implementiraju poteze)
    possible_first_moves = [move_left, move_up, move_down, move_right]
    # Niz za čuvanje rezultata simulacija za svaki početni potez
    first_move_scores = np.zeros(NUMBER_OF_MOVES)
    
    # Prolazi kroz svaki mogući prvi potez
    for first_move_index in range(NUMBER_OF_MOVES):
        # Izbor funkcije za trenutni prvi potez
        first_move_function = possible_first_moves[first_move_index]
        # Primena prvog poteza na trenutnu tablu igre
        board_with_first_move, first_move_made, first_move_score = first_move_function(board)
        
        # Proverava da li je potez bio validan
        if first_move_made:
            # Dodaje novu pločicu nakon prvog poteza
            board_with_first_move = add_new_tile(board_with_first_move)
            # Dodaje rezultat prvog poteza u skor za taj potez
            first_move_scores[first_move_index] += first_move_score
        else:
            # Ako potez nije bio validan, prelazi na sledeći mogući potez
            continue
        
        # Izvršava simulacije za trenutni prvi potez
        for _ in range(searches_per_move):
            move_number = 1
            # Kopira tablu igre za pretragu
            search_board = np.copy(board_with_first_move)
            game_valid = True
            
            # Simulira nasumične poteze dok igra važi i dok broj poteza ne dostigne dužinu pretrage
            while game_valid and move_number < search_length:
                # Nasumičan potez
                search_board, game_valid, score = random_move(search_board)
                if game_valid:
                    # Dodaje novu pločicu nakon nasumičnog poteza
                    search_board = add_new_tile(search_board)
                    # Dodaje rezultat nasumičnog poteza u skor za prvi potez
                    first_move_scores[first_move_index] += score
                    move_number += 1
    
    # Pronalazi indeks najboljeg početnog poteza na osnovu skora
    best_move_index = np.argmax(first_move_scores)
    # Izbor funkcije za najbolji potez
    best_move = possible_first_moves[best_move_index]
    # Primena najboljeg poteza na originalnu tablu igre
    search_board, game_valid, score = best_move(board)
    
    return search_board, game_valid
def ai_play(board):
    move_number = 0 # Brojač poteza
    valid_game = True # Flag koji označava da li je igra validna
    
    while valid_game:
        move_number += 1 # Inkrement brojača poteza
        
        # Dobijanje broja simulacija i dužine pretrage na osnovu trenutnog broja poteza
        number_of_simulations, search_length = get_search_params(move_number)
        
        # Izvođenje AI poteza koristeći trenutne parametre pretrage
        board, valid_game = ai_move(board, number_of_simulations, search_length)
        
        if valid_game:
            # Ažuriranje table igre nakon validnog poteza
            board = (board) + 2
        
        # Ispis trenutne table igre i broja poteza
        print(board)
        print(move_number)
    
    # Ispis konačne table igre
    print(board)
    # Vraća najveći broj (pločicu) postignut na kraju igre
    return np.amax(board)
