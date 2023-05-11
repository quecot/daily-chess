import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/Cellar/ffmpeg/5.0.1/bin/ffmpeg"

import chess.pgn
import lichess.api
from lichess.format import PGN


from select_game import select_code, update_uploaded
from create_frames import get_frames
from create_video import create_video, add_audio
from create_thumbnail import make_thumbnail
from upload_video import upload_video

def main():
    # Select game from codes.txt
    code = select_code()
    current_pgn = open('data/current.pgn', "w")
    current_pgn.write(lichess.api.game(code, format=PGN, literate=True))
    current_pgn.close()

    game = chess.pgn.read_game(open('data/current.pgn'))
    whitePlayer = game.headers['White']
    whiteTitle = game.headers['WhiteTitle']
    whiteElo = game.headers['WhiteElo']
    blackPlayer = game.headers['Black']
    blackTitle = game.headers['WhiteTitle']
    blackElo = game.headers['BlackElo']
    white = f'{whiteTitle} {whitePlayer} ({whiteElo})'
    black = f'{blackTitle} {blackPlayer} ({blackElo})'

    opening = game.headers['Opening']
    eco_code = game.headers['ECO']

    # Produce video frames
    get_frames(game)

    # Create video from frames and song, add endscreen
    create_video()
    add_audio()

    #Make thumbnail
    make_thumbnail(white, black)
    
    #Upload video to YouTube
    upload_video(white, black, opening, eco_code)

    # Update uploaded.txt
    update_uploaded(code)

if __name__=='__main__':
    main()