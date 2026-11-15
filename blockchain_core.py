import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        texte = str(self.index) + str(self.timestamp) + json.dumps(self.data, sort_keys=True) + str(self.previous_hash)
        return hashlib.sha256(texte.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(d):
        b = Block(d["index"], d["timestamp"], d["data"], d["previous_hash"])
        b.hash = d["hash"]
        return b

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Bloc de genèse : index 0, previous_hash = "0"
        return Block(0, time.strftime("%Y-%m-%d %H:%M:%S"), {"message": "Bloc de genese"}, "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last = self.get_last_block()
        new_block = Block(last.index + 1, time.strftime("%Y-%m-%d %H:%M:%S"), data, last.hash)
        self.chain.append(new_block)
        return new_block

    def is_valid(self):
        # Vérifie TOUS les blocs, genèse comprise
        for i in range(len(self.chain)):
            block = self.chain[i]
            # 1. Le hash recalculé doit être égal au hash stocké
            if block.hash != block.compute_hash():
                print(f"ERREUR Block {i} : hash invalide")
                return False
            # 2. Le chaînage doit être correct (sauf genèse)
            if i > 0:
                if block.previous_hash != self.chain[i-1].hash:
                    print(f"ERREUR Block {i} : previous_hash ne correspond pas")
                    return False
            else:
                # Vérification genèse
                if block.previous_hash != "0":
                    print("ERREUR Genese : previous_hash doit etre 0")
                    return False
        return True

    def save_to_file(self, fichier="blockchain.json"):
        with open(fichier, "w") as f:
            json.dump([b.to_dict() for b in self.chain], f, indent=2)
        print(f"Sauvegarde dans {fichier}")

    @staticmethod
    def load_from_file(fichier="blockchain.json"):
        bc = Blockchain()
        try:
            with open(fichier, "r") as f:
                data = json.load(f)
            bc.chain = [Block.from_dict(d) for d in data]
        except FileNotFoundError:
            print("Fichier non trouve, nouvelle chaine creee")
        return bc
