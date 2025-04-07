import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('clap_competition.db')
cursor = conn.cursor()

# Step 1: Create the tables (if not already created)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Person (
    PersonID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    UNIQUE (FirstName, LastName)
)
""")

cursor.execute("""
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
)
""")

# Step 2: Insert test people
cursor.execute("INSERT or IGNORE INTO Person (FirstName, LastName) VALUES (?, ?)", ("Colter", "Radke"))
cursor.execute("INSERT or IGNORE INTO Person (FirstName, LastName) VALUES (?, ?)", ("Simon", "Oliver"))

# Get their IDs
cursor.execute("SELECT * FROM Person")
taylor_id = cursor.fetchall()
print(taylor_id)

# Commit and close
conn.commit()
conn.close()
