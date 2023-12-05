def contagem_progressiva(n):
    if n >= -1:
        contagem_progressiva(n-1)
        print(n)
        
contagem_progressiva(10)