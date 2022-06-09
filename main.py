from uuid import uuid4, UUID
from fastapi import FastAPI, HTTPException, Header, Depends
from typing import List
from utils import verify_etag, settings
from fastapi.encoders import jsonable_encoder
from models import GameResult, Games, GamesIN, Player, Gender, Questions, QuestionsIN, Role, PlayerUpdateRequest
import os, sys
from fastapi.openapi.utils import get_openapi
sys.path.insert(0, os.path.abspath(".."))


app = FastAPI()

db_questions: List[Questions] = [
    Questions(id=UUID("8d1b57f3-17d8-4b91-ae1b-8e8b035c037a"), question = "Kiedy byl chrzest Polski?", answers =["966"], set = [1]),
    Questions(id=UUID("367588bd-dc8a-4641-bd56-7dc606380c1a"), question = "W którym roku rozpoczęła się I wojna światowa?", answers =["1914r."], set = [1]),
    Questions(id=UUID("6d0bb124-35eb-45fb-9c10-484baa0eaa97"), question = "W którym roku rozpoczęła się II wojna światowa?", answers =["1939r."], set = [1]),
    Questions(id=UUID("348d7c70-8170-4b11-b899-f24dabcd78b3"), question = "Najstarsza osada na ziemiach polskich?", answers =["W Biskupinie"], set = [2]),
    Questions(id=UUID("ea8c83de-0ed5-4076-931c-5dbf4b8c2315"), question = "W którym roku Polska przystąpiła do Unii Europejskiej?", answers =["2004r."], set = [2]),
    Questions(id=UUID("1e82204e-f58e-4ca5-9c59-e3991f81e185"), question = "Jaka słynna kopalnia znajduje się w Wieliczce?", answers =["Kopalnia soli"], set = [2]),
    Questions(id=UUID("5bbf90db-71dc-4f21-a2b5-bf35695ea331"), question = "Jak nazywała się I epoka historyczna?", answers =["Starożytność"], set = [3]),
    Questions(id=UUID("8d350ac2-1619-4766-9c2e-514f27625077"), question = "Ile lat liczy wiek?", answers =["100"], set = [3]),
    Questions(id=UUID("113928d1-d441-43a8-92de-078abdc10ddc"), question = "Kto skonstruował pierwszy telefon?", answers =["Aleksander Bell"], set = [3]),
    Questions(id=UUID("89cb72f9-8a09-4f59-82f5-28262e9d8f0f"), question = "Jak nazywał się I król Polski?", answers =["Bolesław Chrobry"], set = [4]),
    Questions(id=UUID("af8ab92e-59ca-44fc-8be6-53464d4bb920"), question = "Jak nazywali się trzej bracia, założyciele Polski, Czech i Rosji?", answers =["Lech, Czech i Rus"], set = [4]),
    Questions(id=UUID("ecd03629-a697-44f8-822c-316885587d27"), question = "Kto był inicjatorem i założycielem ruchu społecznego „Solidarność”? ", answers =["Lech Wałęsa"], set = [4]),
    
]

db_players: List[Player] = [
    Player(id=UUID("e38bf623-1d76-419b-892d-bd38f1059179"), first_name="Jamila", last_name = "Ahmed", middle_name ="Ala",  gender= Gender.female, roles = [Role.user]), 
    Player(id=UUID("5f7d2ce4-ef82-42a1-a7cc-fe8d482b3954"), first_name="Kamil", last_name = "Nowak", gender= Gender.male, roles = [Role.user])
]

db_games: List[Games] = [
    Games(id=UUID("7b54019f-8968-4c2f-a131-f30e465e9e5c"), set_of_q = 2, round = 0, state_of_game = 0),
    Games(id=UUID("ff6e0236-f329-4cdd-ba98-57c25eb04502"), set_of_q = 3, round = 0, state_of_game = 0),
    Games(id=UUID("a3c79f0b-55dd-48b5-888c-ff2f25e30e24"), set_of_q = 1, round = 1, state_of_game = 1) #0 stopped 1 running 2 ended
]

db_games_results: List[GameResult] = [
    GameResult(id_player=UUID("e38bf623-1d76-419b-892d-bd38f1059179"), id_game=UUID("a3c79f0b-55dd-48b5-888c-ff2f25e30e24"),result = 1),
    GameResult(id_player=UUID("5f7d2ce4-ef82-42a1-a7cc-fe8d482b3954"), id_game=UUID("a3c79f0b-55dd-48b5-888c-ff2f25e30e24"),result = 0)
]

db_mergelist: List[Games] = [
     Games(id=UUID("7b54019f-8968-4c2f-a131-f30e465e9e5c"), set_of_q = 2, round = 0, state_of_game = 0)
]


################# Player endpoints #################

@app.get("/players")
def fetch_users():
    return db_players;

@app.get("/players/{player_id}")
def fetch_user(player_id: UUID):
    for player in db_players:
        if player_id == player.id:
            return player
    raise HTTPException(
        status_code = 404,
        detail="user with id {} does not exist".format(player_id)
    )


@app.post("/players")
def add_player():
    player_id = uuid4()
    db_players.append(Player(id=player_id))
    return {"player_id": player_id}

@app.put("/players/{player_id}", dependencies=[Depends(verify_etag)])
def update_player(player_update: PlayerUpdateRequest, player_id: UUID):
    for player in db_players:
        if player_id == player.id:
            player.first_name = player_update.first_name if player_update.first_name is not None else None
            player.last_name = player_update.last_name if player_update.last_name is not None else None
            player.middle_name = player_update.middle_name if player_update.middle_name is not None else None
            player.gender = player_update.gender if player_update.gender is not None else None
            player.roles = player_update.roles if player_update.roles is not None else None
            return player
    raise HTTPException(
        status_code = 404,
        detail="user with id {} does not exist".format(player_id)
    )


@app.delete("/players/{player_id}")
def delete_player(player_id: UUID):
    for player in db_players:
        if player_id == player.id:
            db_players.remove(player)
    return 

################# Questions endpoints #################

@app.get("/questions")
def fetch_questions():
    return db_questions;

@app.post("/questions")
def add_question():
    question_id = uuid4()
    db_questions.append(Questions(id = question_id))
    return {"question_id": question_id}

@app.put("/questions")
def add_question(question_update: QuestionsIN, question_id: UUID, etagH: UUID = Header("etag")):
    if settings.etag == etagH:
        settings.etag = uuid4()
        for question in db_questions:
            if question_id == question_id.id:
                question.question = question_update.question 
                question.answers = question_update.answers
                question.set = question_update.set
                return
        raise HTTPException(
            status_code = 404,
            detail="question with id {} does not exist".format(question_id)
        )
    return {"etag" : settings.etag}

@app.delete("/questions/{question_id}")
def delete_question(question_id: UUID):
    for question in db_questions:
        if question_id == question.id:
            db_questions.remove(question)
            return
    raise HTTPException(
        status_code = 404,
        detail="question with id {} does not exist".format(question_id)
    )

################# Game endpoints #################


@app.get("/games")
def fetch_games():
    return db_games;

@app.get("/games/{game_id}")
def fetch_game_info(game_id: UUID):
    for game in db_games:
        if game.id == game_id:
          return game
    raise HTTPException(
        status_code = 404,
        detail="game with id {} does not exist".format(game_id)
    )

@app.get("/games/{game_id}/questions")
def fetch_game_info(game_id: UUID):
    questions_in_game: List[Questions]
    for game in db_games:
        if game.id == game_id:
            questions_in_game = [q for q in db_questions if q.set == game.set_of_q]
            return questions_in_game
    raise HTTPException(
        status_code = 404,
        detail="game with id {} does not exist".format(game_id)
    )

@app.post("/games")
def add_game():
    game_id = uuid4()
    db_games.append(Games(id = game_id,set_of_q = 0,round = 0,state_of_game = 0))
    return {"game_id": game_id}

@app.put("/games/{game_id}")
def update_game(game_update: GamesIN, game_id: UUID, etagH: UUID = Header("etag")):
    if etagH == settings.etag:
        settings.etag = uuid4()
        for game in db_games:
            if game_id == game.id:
                game.set_of_q = game_update.set_of_q if game_update.set_of_q is not None else None
                game.round = game_update.round if game_update.round is not None else None
                game.state_of_game = game_update.state_of_game if game_update.state_of_game is not None else None
                return 
        raise HTTPException(
            status_code = 404,
            detail="game with id {} does not exist".format(game_id)
        )   
    return {"etag" : settings.etag}

@app.put("/games/{game_id}/merge")
def add_to_merge_list(game_id: UUID, etagH: UUID = Header("etag")):
    if etagH == settings.etag:
        settings.etag = uuid4()
        for game in db_games:
            if game.id == game_id:
                db_mergelist.append(game)
                return
        raise HTTPException(
            status_code =404,
            detail="game with id {} does not exist".format(game_id)
        )
    return {"etag" : settings.etag}

@app.put("/games-merge")
def update_player(etagH: UUID = Header("etag")):
    if settings.etag == etagH:
        settings.etag == uuid4()
        new_id_of_set = max(max(x.set) for x in db_questions) + 1 #get max from list in list
        new_game_id = uuid4()
        questions_id_to_modify: UUID = []
        x = [game.set_of_q for game in db_mergelist]
        for game in db_mergelist:
            for q in db_questions:
                if game.set_of_q in q.set:
                    questions_id_to_modify.append(q.id)
            for real_game in db_games:
                if real_game.id == game.id:
                    db_games.remove(real_game)
        for q in db_questions:
            for qtm in questions_id_to_modify:
                for id in x:
                    if qtm == q.id and id not in q.set:
                        q.set.append(id)
        db_mergelist.clear()
        new_game = Games(id = new_game_id, set_of_q = new_id_of_set, round = 0, state_of_game=0)
        db_games.append(new_game)
        return
    return {"etag" : settings.etag}
#Games(id=UUID("a3c79f0b-55dd-48b5-888c-ff2f25e30e24"), set_of_q = 1, round = 1, state_of_game = 1)
    

@app.get("/games-merge")
def fetch_merge_games():
    return db_mergelist; 
    
        
@app.delete("/games/{game_id}")
def delete_game(game_id: UUID):
    for game in db_games:
        if game_id == game.id:
            db_games.remove(game)
            return
    raise HTTPException(
        status_code = 404,
        detail="game with id {} does not exist".format(game_id)
    )

################# Result endpoints #################

@app.get("/games/{game_id}/results/{player_id}")
def fetch_game_info(game_id: UUID, player_id: UUID):
    for record in db_games_results:
        if record.id_game == game_id and record.id_player== player_id:
            return record
    raise HTTPException(
        status_code = 404, 
        detail="Didnt find a record with given g_id :{}, p_id :{}".format(game_id, player_id)
    )

################# Check the question in the current game #################

@app.get("/games/{game_id}/results/{player_id}")
def fetch_game_info(game_id: UUID, player_id: UUID):
    for record in db_games_results:
        if record.id_game == game_id and record.id_player== player_id:
            return record
    raise HTTPException(
        status_code = 404,
        detail="game with id {} does not exist".format(game_id)
    )



