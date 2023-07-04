from Bot import Bot
from sys import argv
from Genetics import Genetics

genes = Genetics().parse_to_dict(int(argv[1]))

if __name__ == "__main__":
    Bot(genes["genome"],genes)