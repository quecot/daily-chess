import chess.pgn

def games_to_codes():
    """
    Takes games.pgn file and extracts the lichess codes of the ones that don't end in a draw,
    by time forfeit, have no titled players or have less than 30 moves
    Saves the codes to data/codes.txt
    """

    pgn = open('data/games.pgn')
    codes = open('data/codes.txt','w')
    c = 0
    while c < 100:
        game = chess.pgn.read_game(pgn)
        game_len = str(game.mainline_moves()).count('.')
        if game.headers['Result'] != '1/2-1/2' and game.headers['Termination'] != 'Time forfeit' and game_len >= 30:
            if 'WhiteTitle' in game.headers and 'BlackTitle' in game.headers:
                url = game.headers['LichessURL']
                codes.write(url[url.rfind('/')+1:] + "\n")
                c+=1

    pgn.close()
    codes.close()

games_to_codes()