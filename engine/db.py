import sqlite3

con=sqlite3.connect('Prajñāvan.db')
cursor=con.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
#cursor.execute(query)

#query = "INSERT INTO sys_command VALUES (null,'microsoft edge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')"
#cursor.execute(query)
#con.commit()

#cursor.execute("DELETE FROM sys_command WHERE name = ?", ("microsoft edge",))
#con.commit()
#con.close()

#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)


