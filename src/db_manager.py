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
        go_up() # to save db file
        db_conn = sqlite3.connect(
            get_database_file_name(), check_same_thread=False)
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
    sql = ''' INSERT INTO log(date, status, camera_id)
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
    cur.execute("SELECT * FROM log WHERE camera_id=?", (id_camera,))
    rows = cur.fetchall()
    return rows

def select_events_by_id_camera(conn, id_camera):
    """ Query tasks by priority param conn: the Connection object. """
    cur = conn.cursor()
    cur.execute("SELECT * FROM cameras WHERE id_camera=?", (id_camera,))
    rows = cur.fetchall()
    return rows

def get_available_cams(conn):
    ans = select_all_cameras()