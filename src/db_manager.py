import sqlite3
from sqlite3 import Error
from util.logger import print_log
from util.directory import get_root_path, join_path, go_up
from settings import get_database_file_name

def create_database():  
    """ Method to create a data base. """
    sql_create_cameras_table = """ 
                CREATE TABLE IF NOT EXISTS cameras ( 
                    id integer PRIMARY KEY,
                    id_camera text NOT NULL,
                    reg_date text NOT NULL, 
                    path text NOT NULL); """
    sql_create_events_table = """
                CREATE TABLE IF NOT EXISTS events (
                    id integer PRIMARY KEY,
                    date text NOT NULL,
                    type text NOT NULL,
                    camera_id integer NOT NULL,
                    FOREIGN KEY (camera_id) REFERENCES cameras (id));"""
    sql_create_log_table = """
                CREATE TABLE IF NOT EXISTS log (
                    id integer PRIMARY KEY,
                    date text NOT NULL,
                    status text NOT NULL,
                    camera_id integer NOT NULL,
                    FOREIGN KEY (camera_id) REFERENCES cameras (id));"""
    try:
        # db_path = join_path(get_root_path(), get_database_file_name())
        go_up() # to save db file
        db_conn = sqlite3.connect(get_database_file_name())
        c = db_conn.cursor()
        c.execute(sql_create_cameras_table)
        c.execute(sql_create_events_table)
        c.execute(sql_create_log_table)
        print_log('i', 'Database created')
    except Error:
        print_log('w', 'Error! cannot create the database connection.')
    return db_conn

def insert_camera(conn, camera):
    """ Create a new camera reg into the cameras table. Return: camera id """
    sql = ''' INSERT INTO cameras(id_camera,reg_date,path)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, camera)
    conn.commit()
    return cur.lastrowid

def insert_event(conn, event):
    """ Create a new event log to db into event log. """
    sql = ''' INSERT INTO events(date, type, camera_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()
    return cur.lastrowid

def insert_log(conn, camera_log):
    """ Create a new event camera connection connect/disconnect to db. """
    sql = ''' INSERT INTO regs(date, status, camera_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, camera_log)
    conn.commit()
    return cur.lastrowid

def select_all_cameras(conn):
    """ Query all rows in the tasks table """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cameras")
    rows = cur.fetchall()
    return rows

def select_cameras_by_id_camera(conn, id_camera):
    """ Query tasks by priority param conn: the Connection object. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cameras WHERE id_camera=?", (id_camera,))
    rows = cur.fetchall()
    return rows

def select_logs_by_id_camera(conn, id_camera):
    """ Query tasks by priority param conn: the Connection object. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM log WHERE id_camera=?", (id_camera,))
    rows = cur.fetchall()
    return rows

def select_events_by_id_camera(conn, id_camera):
    """ Query tasks by priority param conn: the Connection object. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cameras WHERE id_camera=?", (id_camera,))
    rows = cur.fetchall()
    return rows

# import datetime
# conn = create_database()
# id_camera_reg = insert_new_camera(conn, ('5540408016', datetime.datetime.now(), '/user/mac/'))
# print(id_camera_reg)
# select_camera_by_id(conn, '5540408017')

# def main():
#     database = r"C:\sqlite\db\pythonsqlite.db"

#     # create a database connection
#     conn = create_connection(database)
#     with conn:
#         print("1. Query task by priority:")
#         select_task_by_priority(conn, 1)

#         print("2. Query all tasks")
#         select_all_tasks(conn)

# def main2():
#     database = r"C:\sqlite\db\pythonsqlite.db"

#     # create a database connection
#     conn = create_connection(database)
#     with conn:
#         # create a new project
#         project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
#         project_id = create_project(conn, project)

#         # tasks
#         task_1 = ('Analyze the requirements of the app', 1,
#                   1, project_id, '2015-01-01', '2015-01-02')
#         task_2 = ('Confirm with user about the top requirements',
#                   1, 1, project_id, '2015-01-03', '2015-01-05')

#         # create tasks
#         create_task(conn, task_1)
#         create_task(conn, task_2)