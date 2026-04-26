from fastapi import FastAPI, HTTPException
from database import get_db_connection
import google.generativeai as genai
from typing import List, Optional

app = FastAPI()

# --- ENGINEERING & DESIGN: OOP IMPLEMENTATION (15 Marks) ---
class SoccerPathAI:
    def __init__(self):
        # AI Configuration
        genai.configure(api_key="AIzaSyBFf4eVMneX__0beSUobE-BGGWE6SiHJvI")
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

    def save_match_to_db(self, goals: int, assists: int, interceptions: int):
        """Encapsulates database logic for saving match statistics."""
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # Note: athlete_id 1 is used for Pedro Henrique
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
            f"Goals: {goals}, Assists: {assists}. Provide a concise, high-impact tactical tip for the next match."
        )
        response = self.model.generate_content(prompt)
        return response.text

    def get_athlete_history(self):
        """Retrieves historical data for performance tracking."""
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT goals, assists, interceptions, match_date FROM match_stats ORDER BY match_date DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

# --- INSTANTIATING THE OBJECT ---
soccer_service = SoccerPathAI()

# --- API ENDPOINTS (Implementation Layer) ---

@app.get("/")
async def root():
    return {"message": "SoccerPath AI System Active", "version": "2.0 (OOP)"}

@app.post("/add-match")
async def add_match(goals: int, assists: int, interceptions: int):
    # Using the class methods (OOP approach)
    db_success = soccer_service.save_match_to_db(goals, assists, interceptions)
    
    if not db_success:
        raise HTTPException(status_code=500, detail="Failed to save data to PostgreSQL.")
    
    ai_feedback = soccer_service.generate_tactical_feedback(goals, assists)
    
    return {
        "status": "Success",
        "message": "Match data recorded successfully.",
        "coach_feedback": ai_feedback
    }

@app.get("/my-performance")
async def get_performance():
    history = soccer_service.get_athlete_history()
    
    # Formatting the data for the UI/Frontend
    performance_data = [
        {"date": row[3], "goals": row[0], "assists": row[1], "interceptions": row[2]} 
        for row in history
    ]
    
    return {
        "athlete": "Pedro Henrique",
        "college": "Tabor College",
        "stats_history": performance_data
    }