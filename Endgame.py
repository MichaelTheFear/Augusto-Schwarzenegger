#EndGame is an exception that has two ints, score and genetics
class EndGame(Exception):
    def __init__(self, score, genetics):
        self.score = score
        self.genetics = genetics