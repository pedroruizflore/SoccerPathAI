from fastapi import FastAPI, HTTPException
from database import get_db_connection
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key="AIzaSyBFf4eVMneX__0beSUobE-BGGWE6SiHJvI")

@app.get("/")
async def root():
    return {"status": "SoccerPath AI Active"}

@app.post("/setup-athlete")
async def setup_athlete():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO athletes (name, team, position) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        ("Pedro Henrique", "Tabor College", "Right Wing")
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Atleta configurado com sucesso!"}

@app.post("/add-match")
async def add_match(goals: int, assists: int, interceptions: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO match_stats (athlete_id, goals, assists, interceptions) VALUES (1, %s, %s, %s)",
        (goals, assists, interceptions)
    )
    conn.commit()
    
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    prompt = f"Analyze these stats for a Right Winger: Goals: {goals}, Assists: {assists}. Give a training tip."
    response = model.generate_content(prompt)
    
    cur.close()
    conn.close()
    return {"status": "Match Saved", "ai_feedback": response.text}

@app.get("/my-performance")
async def get_performance():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT goals, assists, interceptions, match_date FROM match_stats ORDER BY match_date DESC")
    history = cur.fetchall()
    cur.close()
    conn.close()
    
    performance_list = [
        {"date": row[3], "goals": row[0], "assists": row[1], "interceptions": row[2]} 
        for row in history
    ]
    return {"atleta": "Pedro Henrique", "team": "Tabor College", "history": performance_list}