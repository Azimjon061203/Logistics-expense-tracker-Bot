import sqlite3

db_name = 'hisobot.db'


def connect():
    return sqlite3.connect(db_name)


def create_table():
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS hisobot (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                full_name TEXT,
                username TEXT,
                phone TEXT,
                lat REAL,
                lon REAL,
                truck_nomi TEXT,
                truck_kabina_nomer TEXT,
                truck_pritsep_nomer TEXT,
                yonalishi_map TEXT,
                oziq_ovqat_valyuta TEXT,
                oziq_ovqat_uchun INTEGER,
                stayanka_valyuta TEXT,
                stayanka_uchun INTEGER,
                tel_valyuta TEXT,
                tel_uchun INTEGER,
                yoqilgi_valyuta TEXT,
                yoqilgi_1l_narxi INTEGER,
                yoqilgi_umumiy_hajmi INTEGER,
                yoqilgi_umumiy_narx INTEGER,
                balon_valyuta TEXT,
                balon_uchun INTEGER,
                motor_valyuta TEXT,
                motor_uchun INTEGER,
                aftol_valyuta TEXT,
                aftol_uchun INTEGER,
                antfris_valyuta TEXT,
                antfris_uchun INTEGER,
                yangi_yonalish TEXT,
                lati REAL,
                longi REAL,
                transport_toroz_joylashuvi TEXT,
                transportni_valyuta TEXT,
                transportni_toroz_uchun INTEGER
            )
        """)


        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                lang TEXT,
                state INTEGER
            )
        """)


        conn.execute("""
            CREATE TABLE IF NOT EXISTS truck_category_panel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                truck_name TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS truck_product_panel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_id INTEGER,
                kabina_nomer_davlat TEXT,
                truck_kabina_nomer TEXT,
                FOREIGN KEY (cat_id) REFERENCES truck_category_panel(id)
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS truck_product_pritsep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pritsep_nomer_davlat TEXT,
                truck_pritsep_nomer TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS CHEK (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                photo TEXT NOT NULL
            )
        """)
        conn.commit()
        print("✅ Barcha jadvalar yaratildi.")


def add_user(
    tg_id, full_name=None, username=None, phone=None, lat=None, lon=None,
    truck_nomi=None, truck_kabina_nomer=None, truck_pritsep_nomer=None, yonalishi_map=None,
    oziq_ovqat_valyuta=None, oziq_ovqat_uchun=None,
    stayanka_valyuta=None, stayanka_uchun=None,
    tel_valyuta=None, tel_uchun=None,
    yoqilgi_valyuta=None, yoqilgi_1l_narxi=None, yoqilgi_umumiy_hajmi=None, yoqilgi_umumiy_narx=None,
    balon_valyuta=None, balon_uchun=None,
    motor_valyuta=None, motor_uchun=None,
    aftol_valyuta=None, aftol_uchun=None,
    antfris_valyuta=None, antfris_uchun=None,
    yangi_yonalish=None, lati=None, longi=None,
    transport_toroz_joylashuvi=None, transportni_valyuta=None, transportni_toroz_uchun=None
):
    with connect() as conn:
        conn.execute("""
            INSERT INTO hisobot (
                tg_id, full_name, username, phone, lat, lon,
                truck_nomi, truck_kabina_nomer, truck_pritsep_nomer, yonalishi_map,
                oziq_ovqat_valyuta, oziq_ovqat_uchun,
                stayanka_valyuta, stayanka_uchun,
                tel_valyuta, tel_uchun,
                yoqilgi_valyuta, yoqilgi_1l_narxi, yoqilgi_umumiy_hajmi, yoqilgi_umumiy_narx,
                balon_valyuta, balon_uchun,
                motor_valyuta, motor_uchun,
                aftol_valyuta, aftol_uchun,
                antfris_valyuta, antfris_uchun,
                yangi_yonalish, lati, longi,
                transport_toroz_joylashuvi, transportni_valyuta, transportni_toroz_uchun
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tg_id, full_name, username, phone, lat, lon,
            truck_nomi, truck_kabina_nomer, truck_pritsep_nomer, yonalishi_map,
            oziq_ovqat_valyuta, oziq_ovqat_uchun,
            stayanka_valyuta, stayanka_uchun,
            tel_valyuta, tel_uchun,
            yoqilgi_valyuta, yoqilgi_1l_narxi, yoqilgi_umumiy_hajmi, yoqilgi_umumiy_narx,
            balon_valyuta, balon_uchun,
            motor_valyuta, motor_uchun,
            aftol_valyuta, aftol_uchun,
            antfris_valyuta, antfris_uchun,
            yangi_yonalish, lati, longi,
            transport_toroz_joylashuvi, transportni_valyuta, transportni_toroz_uchun
        ))
        conn.commit()

def get_all():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM hisobot ORDER BY id DESC")
        return cur.fetchall()



def get_user_all(tg_id):
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM hisobot WHERE tg_id=? ORDER BY id DESC", (tg_id,))
        return [dict(row) for row in cur.fetchall()]


def get_all_users():
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM hisobot ORDER BY id DESC")
        return [dict(row) for row in cur.fetchall()]

def update_user_state(tg_id, state):
    with connect() as conn:
        conn.execute(
            "UPDATE users SET state = ? WHERE tg_id = ?",
            (state, tg_id)
        )
def get_user_first(tg_id):
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM hisobot
            WHERE tg_id = ?
            ORDER BY id ASC
            LIMIT 1
        """, (tg_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def user_truck_kabina_nomer(tg_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT truck_kabina_nomer FROM hisobot WHERE tg_id = ? ORDER BY id ASC LIMIT 1",
            (tg_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None


def user_pritsep_nomer(tg_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT truck_pritsep_nomer FROM hisobot WHERE tg_id = ? ORDER BY id ASC LIMIT 1",
            (tg_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None



def get_user_state(tg_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT state FROM users WHERE tg_id = ?", (tg_id,))
        row = cur.fetchone()
        if row and row[0] is not None:
            return int(row[0])
        return None

def add_lang(tg_id, lang):
    with connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (tg_id, lang) VALUES (?, ?)",
            (tg_id, lang)
        )

def update_user_lang(tg_id, lang):
    with connect() as conn:
        conn.execute(
            "UPDATE users SET lang = ? WHERE tg_id = ?",
            (lang, tg_id)
        )

def get_user_lang(tg_id):
    with connect() as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def add_chek(tg_id, chek_type, photo_id):
    with connect() as conn:
        conn.execute(
            "INSERT INTO CHEK (tg_id, type, photo) VALUES (?, ?, ?)",
            (tg_id, chek_type, photo_id)
        )


def get_all_chek(tg_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT photo FROM CHEK WHERE tg_id=? ORDER BY id ASC",
            (tg_id,)
        )
        return [row[0] for row in cur.fetchall()]


def add_truck_category(truck_name):
    with connect() as conn:
        conn.execute(
            "INSERT INTO truck_category_panel (truck_name) VALUES (?)",
            (truck_name,)
        )


def get_truck_category():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, truck_name FROM truck_category_panel")
        return cur.fetchall()


def add_truck_nomer(cat_id, kabina_nomer_davlat, truck_kabina_nomer):
    with connect() as conn:
        conn.execute("""
            INSERT INTO truck_product_panel
            (cat_id, kabina_nomer_davlat, truck_kabina_nomer)
            VALUES (?, ?, ?)
        """, (cat_id, kabina_nomer_davlat, truck_kabina_nomer))


def get_all_kabina_nomer(cat_id):
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT cat_id, kabina_nomer_davlat, truck_kabina_nomer
            FROM truck_product_panel
            WHERE cat_id = ?
        """, (cat_id,))
        return cur.fetchall()


def add_truck_pritsep_nomer(pritsep_nomer_davlat, truck_pritsep_nomer):
    with connect() as conn:
        conn.execute("""
            INSERT INTO truck_product_pritsep
            (pritsep_nomer_davlat, truck_pritsep_nomer)
            VALUES (?, ?)
        """, (pritsep_nomer_davlat, truck_pritsep_nomer))


def get_all_pritsep_numbers():
    with connect() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, pritsep_nomer_davlat, truck_pritsep_nomer
            FROM truck_product_pritsep
            WHERE truck_pritsep_nomer IS NOT NULL
        """)
        return cur.fetchall()