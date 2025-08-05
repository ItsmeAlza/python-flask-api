from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel(db.Model):
    __tablename__ = 'flask_user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, raw_password: str):
        """Hashes and stores the password."""
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Checks if the given password matches the stored hash."""
        return check_password_hash(self.password, raw_password)

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"
