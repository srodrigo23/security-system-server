import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ 
    create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ 
    create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_database():
    """
    Method to create a data base
    """
    database = r"../../database.db"

    sql_create_cameras_table = """ 
                CREATE TABLE IF NOT EXISTS cameras (
                    id integer PRIMARY KEY,
                    id_camera text NOT NULL,
                    reg_date text NOT NULL); """

    sql_create_events_table = """
                CREATE TABLE IF NOT EXISTS events (
                    id integer PRIMARY KEY,
                    date text NOT NULL,
                    type text NOT NULL,
                    camera_id integer NOT NULL,
                    FOREIGN KEY (camera_id) REFERENCES cameras (id));"""

    sql_create_regs_table = """
                CREATE TABLE IF NOT EXISTS regs (
                    id integer PRIMARY KEY,
                    date text NOT NULL,
                    status text NOT NULL,
                    camera_id integer NOT NULL,
                    FOREIGN KEY (camera_id) REFERENCES cameras (id));"""

    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_cameras_table)
        create_table(conn, sql_create_events_table)
        create_table(conn, sql_create_regs_table)
    else:
        print("Error! cannot create the database connection.")

def insert_new_camera(conn, camera):
    """
    Create a new camera reg into the cameras table.
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO cameras(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, camera)
    conn.commit()
    return cur.lastrowid

def insert_event_log(conn, event):
    """
    Create a new event log to db into event log.
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, event)
    conn.commit()
    return cur.lastrowid

def insert_cam_reg_log(conn, reg_cam):
    """
    Create a new event camera connection connect/disconnect to db.
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO regs(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reg_cam)
    conn.commit()
    return cur.lastrowid

def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1,
                  1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements',
                  1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)

def select_all_cameras(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by priority:")
        select_task_by_priority(conn, 1)

        print("2. Query all tasks")
        select_all_tasks(conn)


if __name__ == '__main__':
    main()