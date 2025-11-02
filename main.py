#points d'entrée (endpoints)

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import User, Action
from database import create_db_and_tables, get_session
import json

app = FastAPI(title="REET API")

create_db_and_tables()

#charger les actions
with open("actions.json") as f:
    actions_data = json.load(f)

@app.post("/user/")
def create_user(username:str, session: Session = Depends(get_session)):
    user = User(username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/mood/")
def set_mood(user_id: int, mood: str, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur qui n'existe pas")
    user.mood = mood
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": f"Mood ajouté à {mood}"}

@app.get("/suggestion/")
def get_suggestions(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    suggestions = [a for a in actions_data if a["mood"] == user.mood]
    return suggestions

@app.post("/complete/")
def complete_action(user_id: int, action_id: int, proof: str = None, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvable")
    
    action = next((a for a in actions_data if a["id"] == action_id), None)
    if not action:
        raise HTTPException(status_code=404, detail="Action non trouvée")
    #les points calculés selon les "preuves" fournies
    points = action["points"] if proof else int(action["points"]*0.5)
    user.points += points

    #avancement de la plantation de l'arbre ou plante
    if user.point > 50:
        user.tree_stage = 5
    elif user.points > 30:
        user.tree_stage = 4
    elif usser.points > 20:
        user.tree_stage = 3
    elif user.points > 10:
        user.tree_stage = 2
    
    #ajustement karma selon preuves fournies
    if proof:
        user.karma = min(100, user.karma + 2)
    else:
        user.karma = max(0, user.karma -1)

    session.add(user)
    session.commit()
    session.refresh(user)
    return {"points": user.points, "tree_stage": user.tree_stage, "karma": user.karma}


#lancement serveur:
#py -m uvicorn main:app --reload
#http://127.0.0.1:8000/docs
