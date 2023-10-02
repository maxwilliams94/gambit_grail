# Current State
- FastAPI locally served
    - Swagger: http://127.0.0.1:8000/docs
- Passing a known gambit FEN into the /game=fen= api yields True and the name of the gambit

## TODO
- Test passing entire PGN in
- Setup Pylint

# TODO
- open telemetry?

# Requirements
## Front-End
- Start with basic html + javascript
- React comes next

## Back-End + fastAPI
- database of gambits
- detect gambit completion from a pgn

### API
- `/api/v1/boards`: Number of boards loaded (status)
- `/api/v1/game/position?fen=`: Is the FEN a gambit?
- `/api/v1/game/pgn`: PGN passed in body is a gambit?

## Database
- users
- user data
- permissions
- MongoDB for experience

###
- Load PGN into memory
- Analyse PGN positions
- Store Board positions for Gambit starting position

### Engine
- import user games
- identify gambit position reached


# TODO longer term
- gambit database - depth first search of gambit PGN
- representation of gambits
- chess.com/lichess game importer
- determine gambits reached
- user database
- game database (store the games as chesscom/lichess ids?)
- 
