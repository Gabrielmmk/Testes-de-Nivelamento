--Importar os dados CSV para o Banco de dados
COPY demonstracoes_contabeis(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
FROM 'C:/Users/gabri/PyCharmProjects/testeDeNivelamento/PostgreSQL/2023/1T2023.csv'
WITH (FORMAT csv, DELIMITER ';', HEADER true, ENCODING 'UTF8');


--10 operadoras com maiores despesas
SELECT *
FROM demonstracoes_contabeis
WHERE (descricao ILIKE '%EVENTOS%'
   OR descricao ILIKE '%SINISTROS CONHECIDOS%'
   OR descricao ILIKE '%AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%')
  AND data >= date_trunc('quarter', CURRENT_DATE) - INTERVAL '3 months'
  AND data < date_trunc('quarter', CURRENT_DATE)
ORDER BY vl_saldo_final DESC
LIMIT 10;

--10 operadoras com maiores despesas no último ano
SELECT *
FROM demonstracoes_contabeis
WHERE (descricao ILIKE '%EVENTOS%'
   OR descricao ILIKE '%SINISTROS CONHECIDOS%'
   OR descricao ILIKE '%AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR%')
  AND data >= date_trunc('year', CURRENT_DATE) - INTERVAL '1 year'
  AND data < date_trunc('year', CURRENT_DATE)
ORDER BY vl_saldo_final DESC
LIMIT 10;
