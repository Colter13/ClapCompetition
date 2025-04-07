from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

def update_elo(winner, loser, k=32):
    expected = 1 / (1 + 10 ** ((loser.elo - winner.elo) / 400))
    winner.elo += k * (1 - expected)
    loser.elo -= k * (1 - expected)
    db.session.commit()
