# Pet Attributes: 
# name: TEXT 
# species: TEXT
# breed: TEXT 
# temperament: TEXT

# https://docs.python.org/3/library/sqlite3.html#tutorial
import sqlite3

# https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection
CONN = sqlite3.connect('lib/resources.db')

# https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
CURSOR = CONN.cursor()

class Pet:

    # ✅ 1. Add "__init__" with "name", "species", "breed", "temperament", and "id" (Default: None) Attributes
    def __init__(self, name, species, breed, temperament, id=None):
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.temperament = temperament

    # ✅ 2. Add "create_table" Class Method to Create "pets" Table If Doesn't Already Exist
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS pets
            (id INTEGER PRIMARY KEY,
            name TEXT,
            species TEXT,
            breed TEXT,
            temperament TEXT)
        """

        CURSOR.execute(sql)

    # ✅ 3. Add "drop_table" Class Method to Drop "pets" Table If Exists
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS pets
        """
        CURSOR.execute(sql)

    # ✅ 4. Add "save" Instance Method to Persist New "pet" Instances to DB
    def save(self):
        sql = """
        INSERT INTO pets (name, species, breed, temperament)
        VALUES (?, ?, ?, ?)
        """

        CURSOR.execute(sql, (self.name, self.species, self.breed, self.temperament))

    # ✅ 5. Add "create" Class Method to Initialize and Save New "pet" Instances to DB
    @classmethod
    def create(cls, name, species, breed, temperament):

        pet = cls(name, species, breed, temperament)
        pet.save()

        return pet

    # ✅ 6. Add "new_from_db" Class Method to Retrieve Newest "pet" Instance w/ Attributes From DB
    @classmethod
    def create_instance(cls, row):
        pet = cls(
            name = row[1],
            species = row[2],
            breed = row[3],
            temperament = row[4],
            id = row[0]
        )
        return pet


    # ✅ 7. Add "get_all" Class Method to Retrieve All "pet" Instances From DB
    @classmethod
    def get_all(cls):
        sql = """
            SELECT * FROM pets
        """

        return [cls.create_instance(row) for row in CURSOR.execute(sql).fetchall()]


    # ✅ 8. Add "find_by_name" Class Method to Retrieve "pet" Instance by "name" Attribute From DB

        # If No "pet" Found, return "None"

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT * FROM pets
            WHERE name = ?
            lIMIT 1
        """

        row = CURSOR.execute(sql, (name, )).fetchone()
        
        if not row:
            return None

        return Pet.create_instance(row)
    # ✅ 9. Add "find_by_id" Class Method to Retrieve "pet" Instance by "id" Attribute From DB

        # If No "pet" Found, return "None"

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM pets
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id, )).fetchone()

        if row:
            return Pet.create_instance(row)

        return None

    # ✅ 10. Add "find_or_create_by" Class Method to:

        #  Find and Retrieve "pet" Instance w/ All Attributes

        # If No "pet" Found, Create New "pet" Instance w/ All Attributes

    @classmethod
    def find_or_create_by(cls, name=None, species=None, breed=None, temperament=None):
        sql = """
            SELECT * FROM pets
            WHERE (name, species, breed, temperament) = (?, ?, ?, ?)
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, species, breed, temperament)).fetchone()

        if not row:

            sql = """
            INSERT INTO pets (name, species, breed, temperament)
            VALUES (?, ?, ?, ?)
        """

            CURSOR.execute(sql, (name, species, breed, temperament))

        return Pet.create_instance(row)

    # ✅ 11. Add "update" Method to Find "pet" Instance by "id" and Update All Attributes

    def update(self):
        sql = """
            UPDATE pets
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))


