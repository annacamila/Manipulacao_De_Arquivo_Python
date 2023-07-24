import os
import pandas as pd
import formatacao


CAMINHO_PASTA_ATUAL = os.path.abspath(os.path.dirname(__file__))
df_output_padrao = pd.read_excel(os.path.join(CAMINHO_PASTA_ATUAL, 'output_padrao_TRF4.xlsx'))
print(df_output_padrao)

df_output_padrao = formatacao.excluir_palavras(df_output_padrao, 'nome_credor', formatacao.EXCLUIR_PALAVRAS)
df_output_padrao = formatacao.excluir_palavras(df_output_padrao, 'advogado_nome', formatacao.EXCLUIR_PALAVRAS)

df_output_padrao['numero_processo'] = df_output_padrao['numero_processo'].str.replace(r'/(PR|RS|SC)', '', regex=True)

df_output_padrao['valor_juros'] = formatacao.preencher_celulas_vazias(df_output_padrao['valor_juros'])

for index, row in df_output_padrao.iterrows():
    df_output_padrao.loc[index, 'documento_credor'] = formatacao.formatar_cpf(row['documento_credor']) if len(str(row['documento_credor'])) <= 11 else formatacao.formatar_cnpj(row['documento_credor'])
    df_output_padrao.loc[index, 'advogado_documento'] = formatacao.formatar_cpf(row['advogado_documento']) if len(str(row['advogado_documento'])) <= 11 else formatacao.formatar_cnpj(row['advogado_documento'])
    df_output_padrao.loc[index, 'numero_processo'] = formatacao.formatar_numero_processo_judicial(row['numero_processo'])
    df_output_padrao.loc[index, 'numero_precatorio'] = formatacao.formatar_numero_processo_judicial(row['numero_precatorio'])
    df_output_padrao.loc[index, 'valor_face'] = row['valor_principal'] + row['valor_juros']
    df_output_padrao.loc[index,'url_arquivo_oficio'] = str(row['numero_precatorio']) + '.pdf'
    df_output_padrao.loc[index,'data_liquidacao'] = formatacao.formatar_data(row['data_liquidacao'])
    df_output_padrao.loc[index,'data_autuacao'] = formatacao.formatar_data(row['data_autuacao'])
    df_output_padrao.loc[index,'data_transito_conhecimento'] = formatacao.formatar_data(row['data_transito_conhecimento'])
    df_output_padrao.loc[index,'data_transito_execucao'] = formatacao.formatar_data(row['data_transito_execucao'])
    if row['advogado_nome'] is not None and str(row['advogado_nome']) != 'nan':
        row['advogado_nome'] = row['advogado_nome'].split('-')
        df_output_padrao.loc[index, 'advogado_nome'] = str(row['advogado_nome'][0]).strip()
        df_output_padrao.loc[index, 'advogado_oab'] = str(row['advogado_nome'][1]).strip()
        
df_output_padrao.to_excel('output_padrao_tratado_2.xlsx', index=False)
print(df_output_padrao, 'Output padrao tratado gerado com sucesso!')

