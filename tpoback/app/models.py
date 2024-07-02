from app.database import get_db

class Registro:
    
    def __init__(self, idRegistro=None, name=None, email=None, password=None, rol=None):
        self.idRegistro = idRegistro
        self.name = name
        self.email = email
        self.password = password
        self.rol = rol or 'user'

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.idRegistro:
            cursor.execute("""
                UPDATE registro SET name = %s, email = %s, password = %s, rol = %s
                WHERE idRegistro = %s
            """, (self.name, self.email, self.password, self.rol, self.idRegistro))
        else:
            cursor.execute("""
                INSERT INTO registro (name, email, password, rol) VALUES (%s, %s, %s, %s)
            """, (self.name, self.email, self.password, self.rol))
            self.idRegistro = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM registro")
        rows = cursor.fetchall()
        registros = [Registro(idRegistro=row[0], name=row[1], email=row[2], password=row[3], rol=row[4]) for row in rows]
        cursor.close()
        return registros

    @staticmethod
    def get_by_id(idRegistro):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM registro WHERE idRegistro = %s", (idRegistro,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Registro(idRegistro=row[0], name=row[1], email=row[2], password=row[3], rol=row[4])
        return None

    @staticmethod
    def get_by_email_and_password(email, password):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM registro WHERE email = %s AND password = %s", (email, password))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Registro(idRegistro=row[0], name=row[1], email=row[2], password=row[3], rol=row[4])
        return None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM registro WHERE idRegistro = %s", (self.idRegistro,))
        db.commit()
        cursor.close()
    
    @staticmethod
    def get_by_email(email):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM registro WHERE email = %s", (email,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Registro(idRegistro=row[0], name=row[1], email=row[2], password=row[3], rol=row[4])
        return None
    def serialize(self):
        return {
            'idRegistro': self.idRegistro,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'rol': self.rol
        }
