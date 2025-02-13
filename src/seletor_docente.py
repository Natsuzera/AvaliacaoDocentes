# Código para seleção de docente dado a lista de docentes
import pandas as pd

def procurar_docente(df: pd.DataFrame, nome_docente: str) -> pd.DataFrame:
    # Filtra o DataFrame para retornar as linhas onde 'nome_docente' contenha o texto informado
    try:
        return df[df['nome_docente'].str.contains(nome_docente.upper())]
    except:
        print('Docente não encontrado')
        df = pd.DataFrame()
        return df


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
