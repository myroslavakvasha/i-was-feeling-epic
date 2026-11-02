import sqlite3

con = sqlite3.connect("epic.db")
con.execute("DELETE FROM movie_subgenre")
con.execute("UPDATE movie SET classified_at = NULL")
con.commit()
con.close()
print("reset done")