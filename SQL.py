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
CREATE TABLE Person (
    PersonID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Wins INTEGER DEFAULT 0,
    Losses INTEGER DEFAULT 0,
    ELO INTEGER DEFAULT 1000,
    UNIQUE(FirstName, LastName)
);
''')

cursor.execute('''
CREATE TABLE Matches (
    MatchID INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    WinnerID INTEGER NOT NULL,
    LoserID INTEGER NOT NULL,
    CoachWinnerID INTEGER,
    CoachLoserID INTEGER,
    HypemanWinnerID INTEGER,
    HypemanLoserID INTEGER,
    FOREIGN KEY (WinnerID) REFERENCES Person(PersonID),
    FOREIGN KEY (LoserID) REFERENCES Person(PersonID),
    FOREIGN KEY (CoachWinnerID) REFERENCES Person(PersonID),
    FOREIGN KEY (CoachLoserID) REFERENCES Person(PersonID),
    FOREIGN KEY (HypemanWinnerID) REFERENCES Person(PersonID),
    FOREIGN KEY (HypemanLoserID) REFERENCES Person(PersonID)
);
''')

# Commit and close
conn.commit()
conn.close()
