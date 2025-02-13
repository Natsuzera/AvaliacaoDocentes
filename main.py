from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from src.archive_load import load_data
from src.seletor_docente import procurar_docente
from src.analysis import analise_docente

app = Flask(__name__)

# Carrega os dados uma única vez ao iniciar a aplicação
df = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome_docente = request.form.get('nome_docente')
        if not nome_docente:
            error = "Por favor, insira o nome do docente."
            return render_template('index.html', error=error)
        
        # Busca candidatos usando a função procurar_docente (que utiliza .upper())
        candidatos = procurar_docente(df, nome_docente)
        if candidatos.empty:
            error = "Docente não encontrado."
            return render_template('index.html', error=error)
        
        unique_names = candidatos['nome_docente'].unique()
        
        if len(unique_names) == 1:
            teacher_name = unique_names[0]
            candidato = candidatos[candidatos['nome_docente'] == teacher_name]
            resultado = analise_docente(candidato, teacher_name)
            # Extrai dados da progressão para o gráfico de linha
            anos = list(resultado['progressao']['ano'])
            postura_values = list(resultado['progressao']['postura_profissional_media'])
            atuacao_values = list(resultado['progressao']['atuacao_profissional_media'])
            return render_template('result.html', estatisticas=resultado['estatisticas'],
                                   anos=anos, postura_values=postura_values, atuacao_values=atuacao_values)
        else:
            # Se houver mais de um candidato, encaminha para a página de seleção
            return render_template('select.html', professores=unique_names, nome_busca=nome_docente)
    return render_template('index.html')

@app.route('/select', methods=['GET'])
def select():
    teacher_name = request.args.get('teacher_name')
    if not teacher_name:
        return redirect(url_for('index'))
    
    candidato = df[df['nome_docente'] == teacher_name]
    if candidato.empty:
        error = "Docente não encontrado."
        return render_template('index.html', error=error)
    
    resultado = analise_docente(candidato, teacher_name)
    anos = list(resultado['progressao']['ano'])
    postura_values = list(resultado['progressao']['postura_profissional_media'])
    atuacao_values = list(resultado['progressao']['atuacao_profissional_media'])
    return render_template('result.html', estatisticas=resultado['estatisticas'],
                           anos=anos, postura_values=postura_values, atuacao_values=atuacao_values)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
