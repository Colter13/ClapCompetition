import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('clap_competition.db')
cursor = conn.cursor()

# Drop Tables
cursor.execute('''
DROP TABLE IF EXISTS Person               
''')

cursor.execute('''
DROP TABLE IF EXISTS Matches               
''')

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
    Competitor1ID INTEGER NOT NULL,
    Competitor2ID INTEGER NOT NULL,
    Coach1ID INTEGER NOT NULL,
    Coach2ID INTEGER NOT NULL,
    Hypeman1ID INTEGER,
    Hypeman2ID INTEGER,
    WinnerID INTEGER NOT NULL,
    LoserID INTEGER NOT NULL,
    FOREIGN KEY (Competitor1ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Competitor2ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Coach1ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Coach2ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Hypeman1ID) REFERENCES Person(PersonID),
    FOREIGN KEY (Hypeman2ID) REFERENCES Person(PersonID),
    FOREIGN KEY (WinnerID) REFERENCES Person(PersonID),
    FOREIGN KEY (LoserID) REFERENCES Person(PersonID)
);
''')

# Commit and close
conn.commit()
conn.close()
