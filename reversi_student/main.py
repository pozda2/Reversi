from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import logging
import traceback
from fastapi.encoders import jsonable_encoder
from State import State 

# Nastavení loggingu
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class GameState(BaseModel):
    gameplan: list[list[int]]
    player: int    

@app.post("/minmax")
def get_best_move(state: GameState):
    try:
        logger.info(f"Received game state: {state.gameplan}, player: {state.player}")

        gameplan_np = np.array(state.gameplan)

        # Ověření správného formátu herního pole
        if gameplan_np.shape != (8, 8):
            message = "Invalid gameplan shape, expected 8x8 grid."
            logger.warning(message)
            return jsonable_encoder({"best_move": None, "rc": 1, "message": message})
        
        # Ověření, že obsahuje pouze hodnoty 0, 1, 2
        if not np.isin(gameplan_np, [0, 1, 2]).all():
            message = "Invalid gameplan values, expected only 0, 1, or 2."
            logger.warning(message)
            return jsonable_encoder({"best_move": None, "rc": 1, "message": message})

        # Ověření, že hráč je buď 1 nebo 2
        if state.player not in [1, 2]:
            message = "Invalid player value, expected 1 or 2."
            logger.warning(message)
            return jsonable_encoder({"best_move": None, "rc": 1, "message": message})

        game_state = State(gameplan_np, state.player)

        _, best_move = game_state.minmax()        

        if best_move is None:
            message = "No valid move found"
            logger.warning(message)
            return jsonable_encoder({"best_move": None, "rc": 0, "message": message})

        best_move = (int(best_move[0]), int(best_move[1]))                
        logger.info(f"Best move selected: {best_move}")

        return jsonable_encoder({"best_move": best_move, "rc": 0, "message": "Ok"})

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail="Internal server error")
