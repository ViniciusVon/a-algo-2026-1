# Tive que adicionar isso porque recebi erros de limite de recusão atingidos
import sys
sys.setrecursionlimit(10000)

def substrings(string):
    length = len(string)
    print(string)
    
    if length == 0:
        return string    

    return substrings(string[:-1])

print(substrings("Vinicius"))