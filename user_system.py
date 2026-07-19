import hashlib
import os
import json

from data_structures import HashTable, BST, MaxHeap


def _hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    digest = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return salt, digest


def _verify_password(password, salt, digest):
    _, new_digest = _hash_password(password, salt)
    return new_digest == digest


class User:
    __slots__ = ("username", "salt", "password_hash", "score")

    def __init__(self, username, salt, password_hash, score=0):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
        self.score = score

    def to_dict(self):
        return {
            "username": self.username,
            "salt": self.salt,
            "password_hash": self.password_hash,
            "score": self.score,
        }

    @staticmethod
    def from_dict(d):
        return User(d["username"], d["salt"], d["password_hash"], d.get("score", 0))

class UserSystem:

    def __init__(self, storage_path="users_data.json"):
        self.storage_path = storage_path
        self.users = HashTable()
        self.scores_bst = BST()
        self.leaderboard = MaxHeap()
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data.get("users", []):
                user = User.from_dict(entry)
                self.users.put(user.username, user)
                self.scores_bst.insert(user.username, user.score)
                self.leaderboard.insert(user.score, user.username)
        except (json.JSONDecodeError, OSError):
            pass

    def save(self):
        data = {"users": [u.to_dict() for _, u in self.users.items()]}
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def sign_up(self, username, password):

        username = (username or "").strip()
        if not username:
            return False, "Username cannot be empty."
        if not password:
            return False, "Password cannot be empty."
        if self.users.contains(username):
            return False, f"Username '{username}' is already taken. Please choose another one."

        salt, pwd_hash = _hash_password(password)
        user = User(username, salt, pwd_hash, score=0)
        self.users.put(username, user)
        self.scores_bst.insert(username, 0)
        self.leaderboard.insert(0, username)
        self.save()
        return True, f"Account '{username}' created successfully."

    def login(self, username, password):

        username = (username or "").strip()
        user = self.users.get(username)
        if user is None:
            return False, f"No account found with username '{username}'.", None

        if not _verify_password(password, user.salt, user.password_hash):
            return False, "Incorrect password.", None

        return True, f"Welcome, {username}!", user

    def get_score(self, username):
        return self.scores_bst.search(username)

    def add_round_score(self, username, round_score):
        user = self.users.get(username)
        if user is None:
            return
        user.score += round_score
        self.scores_bst.update(username, user.score)
        self.leaderboard.update_score(username, user.score)
        self.save()

    def top_player(self):
        return self.leaderboard.peek_max()

    def top_players(self, n=10):
        return self.leaderboard.top_n(n)
