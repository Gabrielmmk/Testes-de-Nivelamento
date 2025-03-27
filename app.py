from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

#Carrega os dados
operadoras_df = pd.read_csv('../testeDeNivelamento/PostgreSQL/Relatorio_cadop.csv', delimiter=';')


@app.route('/search', methods=['GET'])
def search_operadoras():
    # Obter o termo de busca a partir dos parâmetros da URL
    query = request.args.get('query', '').lower()

    # Filtrar as operadoras com base na busca
    resultados = operadoras_df[operadoras_df['NOME_OPERADORA'].str.contains(query, case=False, na=False)]

    # Retornar os resultados como JSON
    return jsonify(resultados.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
