from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Carrega os dados
operadoras_df = pd.read_csv('../testeDeNivelamento/PostgreSQL/Relatorio_cadop.csv', delimiter=';')
print(operadoras_df.columns)  # Mostra todas as colunas do CSV



@app.route('/search', methods=['GET'])
def search_operadoras():
    # Obter o termo de busca a partir dos parâmetros da URL
    query = request.args.get('query', '').lower()

    # Filtrar as operadoras com base na busca
    resultados = operadoras_df[operadoras_df['Razao_Social'].str.contains(query, case=False, na=False)]

    # Retornar os resultados como JSON
    return jsonify(resultados.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
