import os
import pandas as pd

def load_data() -> pd.DataFrame:
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Monta o caminho para o arquivo dentro da pasta "data"
    file_path = os.path.normpath(os.path.join(base_path, '..', 'avaliacaodocencia.csv'))
    
    # Carrega o arquivo CSV
    df = pd.read_csv(file_path, sep=';')
    df = df[['nome_docente', 'ano', 'postura_profissional_media', 'atuacao_profissional_media']]
    return df

