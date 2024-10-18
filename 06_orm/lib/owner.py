# Stretch Goal: Build Out Corresponding Owner Class Methods

# Owner Attributes: 
# name: TEXT 
# phone: TEXT 
# email: TEXT 
# address: TEXT

import sqlite3

CONN = sqlite3.connect('lib/resources.db')
CURSOR = CONN.cursor()

class Owner:
    def __init__(self, name, phone, email, address, id=None):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS owners
            (id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT)
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS owners
        """
        CURSOR.execute(sql)

    def save(self):
        sql = """
        INSERT INTO owners(name, phone, email, address)
        VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.phone, self.email, self.address))

    @classmethod
    def create(cls, name, phone, email, address):

        owner = cls(name, phone, email, address)
        owner.save()

        return owner

    @classmethod
    def create_instance(cls, row):
        owner = cls(
            id = row[0],
            name = row[1],
            phone = row[2],
            email = row[3],
            address = row[4]
        )
        return owner

    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM pets
        """

        return [cls.create_instance(row) for row in CURSOR.execute(sql).fetchall()]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM owners
            WHERE name = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, )).fetchone()

        if not row:
            return None

        return Owner.create_instance(row)

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM owners
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id, )).fetchone()

        if row:
            return Owner.create_instance(row)

        return None

    @classmethod
    def find_or_create_by(cls, name=None, phone=None, email=None, address=None):
        sql = """
            SELECT * FROM owners
            WHERE (name, phone, email, address) = (?, ?, ?, ?)
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, phone, email, address)).fetchone()

        if not row:

            sql = """
            INSERT INTO pets(name, phone, email, address)
            VALUES (?,?,?,?)
        """
            CURSOR.execute(sql, (name, phone, email, address))

        return Owner.create_instance(row)


    def update(self):
        sql = """
            UPDATE owners
            SET name = ?,
                phone = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))