from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clap_competition.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Models
# -----------------------------

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    elo = db.Column(db.Float, default=1000)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant1_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    participant2_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    timestamp = db.Column(db.DateTime, default=db.func.now())

# -----------------------------
# Helper Function
# -----------------------------

def update_elo(winner, loser, k=32):
    expected_win = 1 / (1 + 10 ** ((loser.elo - winner.elo) / 400))
    winner.elo += k * (1 - expected_win)
    loser.elo -= k * (1 - expected_win)
    db.session.commit()

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def index():
    participants = Participant.query.order_by(Participant.elo.desc()).all()
    return render_template('index.html', participants=participants)

@app.route('/add_match', methods=['POST'])
def add_match():
    try:
        p1_id = int(request.form['p1'])
        p2_id = int(request.form['p2'])
        winner_id = int(request.form['winner'])

        p1 = Participant.query.get(p1_id)
        p2 = Participant.query.get(p2_id)
        winner = Participant.query.get(winner_id)

        if not p1 or not p2 or not winner:
            return "Invalid player ID(s). Make sure all participants exist.", 400

        if winner_id != p1_id and winner_id != p2_id:
            return "Winner must be one of the two participants.", 400

        loser = p2 if winner_id == p1_id else p1

        update_elo(winner, loser)

        match = Match(participant1_id=p1_id, participant2_id=p2_id, winner_id=winner_id)
        db.session.add(match)
        db.session.commit()

        return redirect('/')

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# -----------------------------
# Create Tables on Startup
# -----------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
