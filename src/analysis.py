import pandas as pd

def analise_docente(df: pd.DataFrame, nome_docente: str) -> dict:
    candidato = df
    
    # Verifica se encontrou algum registro
    if candidato is None or candidato.empty:
        print("Docente não encontrado!")
        return {}
    
    nome_completo = candidato['nome_docente'].values[0]
    
    # Converte os resultados numéricos para tipo float nativo do Python
    postura_media_min = float(candidato['postura_profissional_media'].min())
    postura_media_max = float(candidato['postura_profissional_media'].max())
    postura_media_mean = float(candidato['postura_profissional_media'].mean())
    
    atuacao_media_min = float(candidato['atuacao_profissional_media'].min())
    atuacao_media_max = float(candidato['atuacao_profissional_media'].max())
    atuacao_media_mean = float(candidato['atuacao_profissional_media'].mean())
    
    # Estatísticas gerais do docente
    estatisticas = {
        'nome_docente': nome_completo,
        'postura_profissional_media': {
            'min': postura_media_min,
            'max': postura_media_max,
            'mean': postura_media_mean
        },
        'atuacao_profissional_media': {
            'min': atuacao_media_min,
            'max': atuacao_media_max,
            'mean': atuacao_media_mean
        }
    }
    
    # Progressão do docente ao longo dos anos
    progressao = candidato.groupby('ano')[['postura_profissional_media', 'atuacao_profissional_media']].mean().reset_index()
    progressao = progressao.sort_values('ano')
    
    # Retorna um dicionário com os dados completos, estatísticas e progressão para uso futuro (como plots)
    return {
        'estatisticas': estatisticas,
        'progressao': progressao
    }
