from pandas import Series
from datetime import datetime


EXCLUIR_PALAVRAS = ['ESPÓLIO DE', 'E OUTROS', 'E OUTRAS', 'E OUTROS(AS)', '- ASSOCIADOS']
def excluir_palavras(df, coluna, palavras):
    for palavra in palavras:
        df[coluna] = df[coluna].str.replace(palavra, '')
    return df

def formatar_cpf(cpf: str) -> str:
    cpf = str(cpf)
    if len(cpf) < 11:
        cpf = cpf.zfill(11)
    if len(cpf) == 11:
        cpf = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
    return cpf

def formatar_cnpj(cnpj: str) -> str:
    cnpj = str(cnpj)
    if len(cnpj) > 11 and len(cnpj) < 14:
        cnpj = cnpj.zfill(14)
    if len(cnpj) == 14:
        cnpj = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}'
    return cnpj

def formatar_numero_processo_judicial(numero_processo: str) -> str:
    numero_processo = str(numero_processo)
    if len(numero_processo) != 28:
        numero_processo = f'{numero_processo[:7]}-{numero_processo[7:9]}.{numero_processo[9:13]}.{numero_processo[13:14]}.{numero_processo[14:16]}.{numero_processo[16:]}'
    return numero_processo

def preencher_celulas_vazias (coluna_dataframe: Series, celulas_vazias: int = 0):
    return coluna_dataframe.fillna(celulas_vazias)

FORMATO_DATA_AMERICANO = '%Y-%m-%d'
FORMATO_DATA_BRASILEIRO = '%d/%m/%Y'
def formatar_data(data: str, formato_data_origem: str = FORMATO_DATA_AMERICANO, formato_saida: str = FORMATO_DATA_BRASILEIRO) -> str:
    if data is not None and str(data) != 'nan':
        datetime_origem = datetime.strptime(str(data), formato_data_origem)
        data_formatada = datetime_origem.strftime(formato_saida)
        return data_formatada

