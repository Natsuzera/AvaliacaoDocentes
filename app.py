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

@app.route('/compare', methods=['POST'])
def compare():
    docente1 = request.form.get('docente1')
    docente2 = request.form.get('docente2')
    
    if not docente1 or not docente2:
        error = "Por favor, insira o nome dos dois docentes."
        return render_template('index.html', error=error)
    
    # Busca candidatos para ambos os docentes
    candidatos1 = procurar_docente(df, docente1)
    candidatos2 = procurar_docente(df, docente2)
    
    if candidatos1.empty or candidatos2.empty:
        error = "Um ou mais docentes não foram encontrados."
        return render_template('index.html', error=error)
    
    # Convertendo para lista Python (evita arrays NumPy)
    unique_names1 = candidatos1['nome_docente'].unique().tolist()  # Corrigido aqui
    unique_names2 = candidatos2['nome_docente'].unique().tolist()  # Corrigido aqui
    
    # Se ambos os termos retornaram apenas um resultado cada, vai direto para a comparação
    if len(unique_names1) == 1 and len(unique_names2) == 1:
        return compare_teachers(unique_names1[0], unique_names2[0])
    
    # Caso contrário, vai para a página de seleção de docentes
    docente1_selecionado = unique_names1[0] if len(unique_names1) == 1 else None
    docente2_selecionado = unique_names2[0] if len(unique_names2) == 1 else None
    
    # Passa as listas como listas Python (não como arrays)
    return render_template('select_compare.html',
                         docente1_list=unique_names1 if not docente1_selecionado else None,
                         docente2_list=unique_names2 if not docente2_selecionado else None,
                         docente1_termo=docente1,
                         docente2_termo=docente2,
                         docente1_selecionado=docente1_selecionado,
                         docente2_selecionado=docente2_selecionado)

@app.route('/select_compare')
def select_compare():
    position = request.args.get('position')
    teacher_name = request.args.get('teacher_name')
    other_teacher = request.args.get('other_teacher')
    docente1_termo = request.args.get('docente1_termo', '')
    docente2_termo = request.args.get('docente2_termo', '')
    
    if not position or not teacher_name:
        return redirect(url_for('index'))
    
    # Se já tem os dois professores, faz a comparação
    if other_teacher:
        return compare_teachers(teacher_name, other_teacher) if position == 'first' else compare_teachers(other_teacher, teacher_name)
    
    # Busca candidatos do outro docente e converte para lista
    if position == 'first':
        candidatos2 = procurar_docente(df, docente2_termo)
        unique_names2 = candidatos2['nome_docente'].unique().tolist()  # Convertendo para lista
        
        return render_template('select_compare.html',
                             docente1_selecionado=teacher_name,
                             docente2_selecionado=None,
                             docente1_list=None,
                             docente2_list=unique_names2 if unique_names2 else None,  # Garante lista ou None
                             docente1_termo=docente1_termo,
                             docente2_termo=docente2_termo)
    else:
        candidatos1 = procurar_docente(df, docente1_termo)
        unique_names1 = candidatos1['nome_docente'].unique().tolist()  # Convertendo para lista
        
        return render_template('select_compare.html',
                             docente1_selecionado=None,
                             docente2_selecionado=teacher_name,
                             docente1_list=unique_names1 if unique_names1 else None,  # Garante lista ou None
                             docente2_list=None,
                             docente1_termo=docente1_termo,
                             docente2_termo=docente2_termo)

def compare_teachers(teacher1_name, teacher2_name):
    # Obtém os dados de cada professor
    teacher1_data = df[df['nome_docente'] == teacher1_name]
    teacher2_data = df[df['nome_docente'] == teacher2_name]
    
    if teacher1_data.empty or teacher2_data.empty:
        error = "Um ou mais docentes não foram encontrados."
        return render_template('index.html', error=error)
    
    # Analisa os dados de cada professor
    resultado1 = analise_docente(teacher1_data, teacher1_name)
    resultado2 = analise_docente(teacher2_data, teacher2_name)
    
    # Obtém os anos únicos de ambos os professores
    anos = sorted(list(set(
        list(resultado1['progressao']['ano']) + 
        list(resultado2['progressao']['ano'])
    )))
    
    # Prepara os dados para o gráfico
    postura_values1 = [resultado1['progressao'][resultado1['progressao']['ano'] == ano]['postura_profissional_media'].iloc[0] 
                      if ano in resultado1['progressao']['ano'].values else None 
                      for ano in anos]
    
    atuacao_values1 = [resultado1['progressao'][resultado1['progressao']['ano'] == ano]['atuacao_profissional_media'].iloc[0]
                       if ano in resultado1['progressao']['ano'].values else None 
                       for ano in anos]
    
    postura_values2 = [resultado2['progressao'][resultado2['progressao']['ano'] == ano]['postura_profissional_media'].iloc[0]
                       if ano in resultado2['progressao']['ano'].values else None 
                       for ano in anos]
    
    atuacao_values2 = [resultado2['progressao'][resultado2['progressao']['ano'] == ano]['atuacao_profissional_media'].iloc[0]
                       if ano in resultado2['progressao']['ano'].values else None 
                       for ano in anos]
    
    return render_template('result_compare.html',
                         estatisticas1=resultado1['estatisticas'],
                         estatisticas2=resultado2['estatisticas'],
                         anos=anos,
                         postura_values1=postura_values1,
                         atuacao_values1=atuacao_values1,
                         postura_values2=postura_values2,
                         atuacao_values2=atuacao_values2)

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

@app.route('/mais-informacoes')
def mais_informacoes():
    return render_template('mais_informacoes.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)