# Código para seleção de docente dado a lista de docentes
import pandas as pd
import unicodedata

def remover_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def procurar_docente(df: pd.DataFrame, nome_docente: str) -> pd.DataFrame:
    # Remove espaços em branco, acentos e converte para maiúsculas
    nome_docente = remover_acentos(nome_docente.strip()).upper()
    
    try:
        return df[df['nome_docente'].str.contains(nome_docente)]
    except Exception as e:
        print('Docente não encontrado:', e)
        return pd.DataFrame()



def selecionar_docente(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        print('Docente não encontrado')
        return df

    nomes_unicos = df['nome_docente'].unique()
    
    if len(nomes_unicos) == 1:
        print('Docente encontrado:')
        print(nomes_unicos[0])
        return df[df['nome_docente'] == nomes_unicos[0]]
        
    print('Lista de docentes disponíveis:')
    index = 0
    for nome in nomes_unicos:
        print(f"{index}. {nome}")
        index += 1
    # Pede ao usuário que informe o nome do docente dentre os disponíveis
    nome_docente = input('informe o nome do docente: ')
    return df[df['nome_docente'] == nome_docente.upper()]
