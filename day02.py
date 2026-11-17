import numpy as np

# 1. Creating a 1D array (like a vector)
scores = np.array([85, 90, 78, 92, 88])
print("Scores:", scores)

# 2. Creating a 2D array (like a matrix or table)
matrix = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
print("\nMatrix shape:", matrix.shape)  # Output: (2 rows, 3 columns)

# 3. Element-wise operations (no loops needed!)
doubled_scores = scores * 2
print("\nDoubled Scores:", doubled_scores)

# 4. Basic aggregations
print("Average Score:", np.mean(scores))
print("Highest Score:", np.max(scores))
print("Highest Score:", np.min(scores))

# 5. Creating a 3D array (like a matrix or table)
matrix1 = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print("\nMatrix transpose:", matrix1.T)  # Output: (3 rows, 3 columns)
print("\nMatrix mean:", np.mean(matrix1))

import sqlite3

# 1. Connect to a temporary database in memory
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# 2. Create a simple table called 'friends'
cursor.execute('''
    CREATE TABLE friends (
        name TEXT,
        age INTEGER,
        city TEXT
    )
''')

# 3. Add some rows of data
cursor.execute("INSERT INTO friends VALUES ('Aarav', 21, 'Mumbai')")
cursor.execute("INSERT INTO friends VALUES ('Priya', 24, 'Delhi')")
cursor.execute("INSERT INTO friends VALUES ('Rahul', 22, 'Mumbai')")
conn.commit()

# --- 4. Let's run SQL queries ---

# Query A: Show everyone
print("--- Everyone in the table ---")
cursor.execute("SELECT * FROM friends")
for row in cursor.fetchall():
    print(row)

# Query B: Filter using WHERE (Only show people from Mumbai)
print("\n--- Only people from Mumbai ---")
cursor.execute("SELECT name FROM friends WHERE city = 'Mumbai'")
for row in cursor.fetchall():
    print(row)

print("\n--- Sorted by City, then Age ---")
cursor.execute("SELECT name, city, age FROM friends ORDER BY city ASC, age ASC")
for row in cursor.fetchall():
    print(row)

print("\n--- Age between 22 and 24 ---")
cursor.execute("SELECT name, age FROM friends WHERE age BETWEEN 22 AND 24")
for row in cursor.fetchall():
    print(row)

print("--- From Mumbai AND Age > 21 ---")
cursor.execute("SELECT name, age, city FROM friends WHERE city = 'Mumbai' AND age > 21")
for row in cursor.fetchall():
    print(row)

# --- FIND FRIENDS WITH A UNIQUE CITY ---
print("--- Friends living in a unique city ---")

query = '''
    SELECT name, city 
    FROM friends 
    WHERE city IN (
        SELECT city 
        FROM friends 
        GROUP BY city 
        HAVING COUNT(*) = 1
    )
'''

cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# A. AVG, MIN, MAX: Find the average, oldest, and youngest age
print("--- Age Statistics ---")
cursor.execute("SELECT AVG(age), MIN(age), MAX(age) FROM friends")
avg_age, min_age, max_age = cursor.fetchone()
print(f"Average Age: {avg_age} | Youngest: {min_age} | Oldest: {max_age}")

# B. LIKE: Search for names starting with the letter 'A' (% means wildcard)
print("\n--- Names starting with 'A' ---")
cursor.execute("SELECT name FROM friends WHERE name LIKE 'A%'")
for row in cursor.fetchall():
    print(row)

# C. UPDATE: Change a friend's city
print("\n--- Updating Data ---")
cursor.execute("UPDATE friends SET city = 'Pune' WHERE name = 'Rahul'")
conn.commit()

# Close the database connection
conn.close()
