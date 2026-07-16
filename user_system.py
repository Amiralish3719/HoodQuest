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
