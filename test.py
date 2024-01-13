import sqlite3

with sqlite3.connect('crack_db.sqlite') as con:
    print(con.cursor().execute("""SELECT music_volume FROM statistics 
                    WHERE user_id = (SELECT id FROM user WHERE nickname = ?)""", ('asdf', )).fetchone())