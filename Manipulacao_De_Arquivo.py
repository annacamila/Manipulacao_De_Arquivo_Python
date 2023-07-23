import pandas as pd

df = pd.read_excel('Modulo_01\output_padrao_TRF4.xlsx')
print(df)

df['nome_credor'] = df['nome_credor'].str.replace(
    'ESPÓLIO DE', '').str.replace('E OUTROS', '')
print(df['nome_credor'])


def formatar_documento(cpf_cnpj):
    documento_formatado = None
    cpf_cnpj = str(cpf_cnpj)
    if len(cpf_cnpj) < 11 and len(cpf_cnpj) < 14:
        cpf_cnpj = cpf_cnpj.zfill(11)
    if len(cpf_cnpj) == 11:
        documento_formatado = '{}.{}.{}-{}'.format(
            cpf_cnpj[:3], cpf_cnpj[3:6], cpf_cnpj[6:9], cpf_cnpj[9:])
    if len(cpf_cnpj) > 11 and len(cpf_cnpj) < 14:
        cpf_cnpj = cpf_cnpj.zfill(14)
    if len(cpf_cnpj) == 14:
        documento_formatado = "{}.{}.{}/{}-{}".format(
            cpf_cnpj[0:2], cpf_cnpj[2:5], cpf_cnpj[5:8], cpf_cnpj[8:12], cpf_cnpj[12:14])
    return documento_formatado


for index, row in df.iterrows():
    df['documento_credor'][index] = formatar_documento(row['documento_credor'])
    df['advogado_documento'][index] = formatar_documento(
        row['advogado_documento'])
print(df['documento_credor'], df['advogado_documento'])


def formatar_prec_proc(prec_proc):
    prec_proc_formatado = None
    prec_proc = str(prec_proc)
    if len(prec_proc) != 28:
        prec_proc_formatado = '{}-{}.{}.{}.{}.{}'.format(
            prec_proc[:7], prec_proc[7:9], prec_proc[9:13], prec_proc[13:14], prec_proc[14:16], prec_proc[16:])
    if len(prec_proc) == 28:
        return prec_proc
    return prec_proc_formatado


for index, row in df.iterrows():
    df['numero_processo'][index] = formatar_prec_proc(row['numero_processo'])
    df['numero_precatorio'][index] = formatar_prec_proc(
        row['numero_precatorio'])
print(df['numero_processo'], df['numero_precatorio'])

df['numero_processo'] = df['numero_processo'].str.replace(
    '/PR', '').str.replace('/RS', '').str.replace('/SC', '')
print(df['numero_processo'])

# Substituindo valores faltantes por zero
df['valor_principal'].fillna(0, inplace=True)
df['valor_juros'].fillna(0, inplace=True)

# Calculando a coluna valor_face
df['valor_face'] = df['valor_principal'] + df['valor_juros']
print(df['valor_face'])

df['url_arquivo_oficio'] = df['numero_precatorio'] + '.pdf'
print(df['url_arquivo_oficio'])

# Formatando as colunas no formato brasileiro
df['data_liquidacao'] = pd.to_datetime(
    df['data_liquidacao']).dt.strftime('%d/%m/%Y')
df['data_autuacao'] = pd.to_datetime(
    df['data_autuacao']).dt.strftime('%d/%m/%Y')
df['data_transito_conhecimento'] = pd.to_datetime(
    df['data_transito_conhecimento']).dt.strftime('%d/%m/%Y')
df['data_transito_execucao'] = pd.to_datetime(
    df['data_transito_execucao']).dt.strftime('%d/%m/%Y')

df['advogado_nome'] = df['advogado_nome'].str.replace(
    '- ASSOCIADOS', 'ASSOCIADOS')

# Adicionar nova coluna temporária para armazenar nome e OAB combinados
df['temp'] = df['advogado_nome'].str.strip()

# Separar nome e OAB em colunas diferentes
df[['advogado_nome', 'advogado_oab']
   ] = df['temp'].str.split('-', n=1, expand=True)

# Remover coluna temporária
df.drop(columns=['temp'], inplace=True)

# Salvando o dataframe em um novo arquivo Excel
df.to_excel('output_padrao_tratado.xlsx', index=False)
