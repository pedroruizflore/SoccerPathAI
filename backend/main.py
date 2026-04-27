from fastapi import FastAPI, HTTPException
from .database import get_db_connection
import google.generativeai as genai
from typing import List, Optional
import os
import google.generativeai as genai

app = FastAPI()

# --- ENGINEERING & DESIGN: OOP IMPLEMENTATION ---
class SoccerPathAI:
    def __init__(self):
        # AI Configuration
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def save_match_to_db(self, goals: int, assists: int, interceptions: int):
        """Encapsulates database logic for saving match statistics."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO match_stats (athlete_id, goals, assists, interceptions) VALUES (1, %s, %s, %s)",
                (goals, assists, interceptions)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Database Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def generate_tactical_feedback(self, goals: int, assists: int):
        """Integrates AI to provide real-time tactical analysis."""
        prompt = (
            f"Act as a professional soccer coach. Analyze these stats for a Right Winger: "
            f"Goals: {goals}, Assists: {assists}. Provide a concise, high-impact tactical tip."
        )
        response = self.model.generate_content(prompt)
        return response.text

    def get_athlete_history(self):
        """Retrieves historical data for performance tracking."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, goals, assists, interceptions, match_date FROM match_stats ORDER BY match_date DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    def update_match_stats(self, match_id: int, goals: int, assists: int, interceptions: int):
        """Updates an existing match record (The 'U' in CRUD)."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "UPDATE match_stats SET goals = %s, assists = %s, interceptions = %s WHERE id = %s",
                (goals, assists, interceptions, match_id)
            )
            conn.commit()
            return cur.rowcount > 0 
        except Exception as e:
            print(f"Update Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

    def delete_match_record(self, match_id: int):
        """Deletes a match record from the database (The 'D' in CRUD)."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM match_stats WHERE id = %s", (match_id,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print(f"Delete Error: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# --- INSTANTIATING THE OBJECT ---
soccer_service = SoccerPathAI()

# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {"message": "SoccerPath AI System Active", "version": "2.0 (OOP)"}

@app.post("/add-match")
async def add_match(goals: int, assists: int, interceptions: int):
    db_success = soccer_service.save_match_to_db(goals, assists, interceptions)
    if not db_success:
        raise HTTPException(status_code=500, detail="Failed to save data.")
    ai_feedback = soccer_service.generate_tactical_feedback(goals, assists)
    return {"status": "Success", "coach_feedback": ai_feedback}

@app.get("/my-performance")
async def get_performance():
    history = soccer_service.get_athlete_history()
    performance_data = [
        {"id": row[0], "date": row[4], "goals": row[1], "assists": row[2], "interceptions": row[3]} 
        for row in history
    ]
    return {"athlete": "Pedro Henrique", "college": "Tabor College", "stats_history": performance_data}

@app.put("/update-match/{match_id}")
async def update_match(match_id: int, goals: int, assists: int, interceptions: int):
    success = soccer_service.update_match_stats(match_id, goals, assists, interceptions)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found.")
    return {"message": "Update successful"}

@app.delete("/delete-match/{match_id}")
async def delete_match(match_id: int):
    success = soccer_service.delete_match_record(match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found.")
    return {"message": "Delete successful"}