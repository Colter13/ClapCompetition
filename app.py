from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_match", methods=["GET", "POST"])
def add_match():
    if request.method == "POST":
        date = request.form["date"]
        winner = request.form["winner"]
        loser = request.form["loser"]
        coach_winner = request.form["coach_winner"]
        coach_loser = request.form["coach_loser"]
        hypeman_winner = request.form["hypeman_winner"]
        hypeman_loser = request.form["hypeman_loser"]

        def get_or_create_person(full_name, cursor):
            if not full_name.strip():
                return None
            first, last = full_name.strip().split(" ", 1)
            cursor.execute("""
                INSERT OR IGNORE INTO Person (FirstName, LastName)
                VALUES (?, ?)
            """, (first, last))
            cursor.execute("""
                SELECT PersonID FROM Person WHERE FirstName = ? AND LastName = ?
            """, (first, last))
            return cursor.fetchone()[0]

        conn = sqlite3.connect('clap_competition.db')
        cursor = conn.cursor()

        # Get or create person IDs
        winner_id = get_or_create_person(winner, cursor)
        loser_id = get_or_create_person(loser, cursor)
        coach_winner_id = get_or_create_person(coach_winner, cursor)
        coach_loser_id = get_or_create_person(coach_loser, cursor)
        hype_winner_id = get_or_create_person(hypeman_winner, cursor)
        hype_loser_id = get_or_create_person(hypeman_loser, cursor)

        # Insert match
        cursor.execute("""
            INSERT INTO Matches (
                Date,
                CoachWinnerID, CoachLoserID,
                HypemanWinnerID, HypemanLoserID,
                WinnerID, LoserID
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            date,
            coach_winner_id, coach_loser_id,
            hype_winner_id, hype_loser_id,
            winner_id, loser_id
        ))

        # Elo calculation
        cursor.execute("SELECT ELO FROM Person WHERE PersonID = ?", (winner_id,))
        winner_rating = cursor.fetchone()[0]
        cursor.execute("SELECT ELO FROM Person WHERE PersonID = ?", (loser_id,))
        loser_rating = cursor.fetchone()[0]

        winner_probability = 1 / (1 + pow(10, (loser_rating - winner_rating) / 400))
        loser_probability = 1 - winner_probability

        winner_rating = round(winner_rating + 30 * (1 - winner_probability) + 1, 2)
        loser_rating = round(loser_rating + 30 * (0 - loser_probability) + 1, 2)

        # Update stats
        cursor.execute("UPDATE Person SET Wins = Wins + 1, ELO = ? WHERE PersonID = ?", (winner_rating, winner_id,))
        cursor.execute("UPDATE Person SET Losses = Losses + 1, ELO = ? WHERE PersonID = ?", (loser_rating, loser_id,))

        conn.commit()
        conn.close()

        return redirect(url_for("add_match"))

    return render_template("add_match.html")

@app.route("/rankings")
def list_rankings():
    conn = sqlite3.connect('clap_competition.db')
    cursor = conn.cursor()
    cursor.execute('''
                SELECT FirstName, LastName, Wins, Losses, Elo FROM Person 
                WHERE wins + losses > 0
                ORDER BY Elo Desc
                ''')
    competitors = cursor.fetchall()
    conn.close()

    return render_template("rankings.html", competitors=competitors)

@app.route("/matches")
def list_matches():
    conn = sqlite3.connect('clap_competition.db')
    cursor = conn.cursor()
    cursor.execute('''
                SELECT 
                    m.Date, 
                    pw.FirstName || ' ' || pw.LastName AS WinnerName,
                    pl.FirstName || ' ' || pl.LastName AS LoserName,
                    pcw.FirstName || ' ' || pcw.LastName AS CoachWinnerName,
                    pcl.FirstName || ' ' || pcl.LastName AS CoachLoserName,
                    phw.FirstName || ' ' || phw.LastName AS HypemanWinnerName,
                    phl.FirstName || ' ' || phl.LastName AS HypemanLoserName
                FROM Matches m
                LEFT JOIN Person pw ON m.WinnerID = pw.PersonID
                LEFT JOIN Person pl ON m.LoserID = pl.PersonID
                LEFT JOIN Person pcw ON m.CoachWinnerID = pcw.PersonID
                LEFT JOIN Person pcl ON m.CoachLoserID = pcl.PersonID
                LEFT JOIN Person phw ON m.HypemanWinnerID = phw.PersonID
                LEFT JOIN Person phl ON m.HypemanLoserID = phl.PersonID
                ORDER BY m.Date DESC;
                ''')
    matches = cursor.fetchall()
    print(matches)
    conn.close()

    return render_template("matches.html", matches=matches)

if __name__ == "__main__":
    app.run(debug=True)