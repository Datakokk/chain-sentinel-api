class Transaction:
    def __init__(self, hash, from_address, to_address, value, timestamp):
        self.hash = hash
        self.from_address = from_address
        self.to_address = to_address
        self.value = value
        self.timestamp = timestamp