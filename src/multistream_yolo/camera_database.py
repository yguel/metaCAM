import sqlite3
# coding=utf-8

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("cam.db")
        return conn

    except Exception as e:
        print(e)
    
    return conn

def create_table(conn):
    
    sql_create_table = """CREATE TABLE IF NOT EXISTS cam(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        mac TEXT NOT NULL,
        ip TEXT NOT NULL,
        room TEXT NOT NULL,
        name TEXT NOT NULL,
        alive INTEGER
    )
    """
    #alive = 1 -> active ; 0 -> inactive

    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
            return c
        except Exception as e:
            print(e)

def get_active_camera():
    conn = create_connection()
    #creation de la table
    c = create_table(conn)
    query = "SELECT * FROM cam WHERE alive = 1"

    #execution de la requete
    c.execute(query)

    # Recuperation des resultats
    rows = c.fetchall()

    cam_list=[]
    #[0] = ip, [1] = location, [2] = name
    for row in rows:
        if(row[5] == 1):
            cam_list.append([row[2],row[3],row[4]])

    # Fermeture de la connexion
    conn.close()
    return cam_list

def add_a_camera(data):
    #data[0] = mac address
    #data[1] = IP
    #data[2] = Location
    #data[3] = Name
    #data[4] = Alive (normally 1) if called

    conn = create_connection()
    #On cree la table au cas ou
    c = create_table(conn)

    nouvelle_camera = (data[0].upper(),  data[1],  data[2], data[3], data[4])

    query = "INSERT INTO cam(mac, ip, room, name, alive) VALUES (?, ?, ?, ?, ?)"
    c.execute(query,nouvelle_camera)

    conn.commit()

    conn.close()


def drop_table():
    conn = create_connection()
    c = conn.cursor()

    query = "DROP TABLE IF EXISTS cam"

    c.execute(query)

    conn.commit()

    conn.close()

def get_all_mac_address():
    conn = create_connection()
    c = create_table(conn)

    query = "SELECT DISTINCT mac FROM cam"
    
    c.execute(query)

    adresses_mac = c.fetchall()

    mac_list = []
    for adresse_mac in adresses_mac:
        mac_list.append(adresse_mac[0])

    conn.close()

    return mac_list

def update_mac_ip_address(mac,ip):
    conn = create_connection()
    c = create_table(conn)

    query = "UPDATE cam SET ip = ?, alive = 1 WHERE mac = ?"

    c.execute(query, (ip, mac.upper()))

    conn.commit()

    conn.close()


def set_camera_offline(mac):
    conn = create_connection()
    c = create_table(conn)

    query = "UPDATE cam SET alive = 0 WHERE mac = ?"

    c.execute(query, (mac,))

    conn.commit()

    conn.close()

if __name__ == "__main__":
    data = ["00:11:32:b2:ca:68","10.0.0.0","chambre","bedroom 1",1]
    data2 = ["ee:cD:eF:12:34:56","10.0.0.0","Bedroom","bedroom 1",1]
    add_a_camera(data)
    add_a_camera(data2)
    print(get_all_mac_address())
    print(get_active_camera())
    #drop_table()

