import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('clap_competition.db')
cursor = conn.cursor()

# Create Tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Person (
    PersonID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Wins INTEGER DEFAULT 0,
    Losses INTEGER DEFAULT 0,
    ELO INTEGER DEFAULT 1000
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Matches (
    MatchID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Player1ID INTEGER NOT NULL,
    Player2ID INTEGER NOT NULL,
    Player1CoachID INTEGER NOT NULL,
    Player2CoachID INTEGER NOT NULL,
    Player1HypemanID INTEGER,
    Player2HypemanID INTEGER,
    WinnerID INTEGER NOT NULL,
    LoserID INTEGER NOT NULL,
    FOREIGN KEY (Player1ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Player2ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Player1CoachID) REFERENCES Person(PersonID),
    FOREIGN KEY (Player2CoachID) REFERENCES Person(PersonID),
    FOREIGN KEY (Player1HypemanID) REFERENCES Person(PersonID),
    FOREIGN KEY (Player2HypemanID) REFERENCES Person(PersonID),
    FOREIGN KEY (WinnerID) REFERENCES Person(PersonID),
    FOREIGN KEY (LoserID) REFERENCES Person(PersonID)
);
''')

# Commit and close
conn.commit()
conn.close()
