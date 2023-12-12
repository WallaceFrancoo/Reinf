import pandas as pd
import Acumuladores
from tkinter import filedialog


def processar_arquivoNF(caminho_do_arquivo):
    try:
        dados = pd.read_csv(caminho_do_arquivo, delimiter=';', encoding='ISO-8859-1')

        # Acesse a coluna correspondente ao índice 73 (considerando que o índice começa em 0)
        notas = dados.iloc[:, 0]  # 0 é o índice da primeira coluna

        # Filtra o DataFrame para incluir apenas as linhas em que o valor na coluna 73 é igual a 2
        linhas_filtradas = dados.loc[notas == "2"].copy().astype('object')

        linhas_filtradas.fillna("", inplace=True)

        coluna_55 = 'PIS/PASEP'  # Substitua pelo nome real da coluna
        coluna_56 = 'COFINS'  # Substitua pelo nome real da coluna
        coluna_60 = 'CSLL'  # Substitua pelo nome real da coluna

        linhas_filtradas[coluna_55] = linhas_filtradas[coluna_55].apply(
            lambda x: str(x).replace(',', '.') if isinstance(x, str) else x).astype(float)
        linhas_filtradas[coluna_56] = linhas_filtradas[coluna_56].apply(
            lambda x: str(x).replace(',', '.') if isinstance(x, str) else x).astype(float)
        linhas_filtradas[coluna_60] = linhas_filtradas[coluna_60].apply(
            lambda x: str(x).replace(',', '.') if isinstance(x, str) else x).astype(float)


        # Defina uma função para formatar o texto
        def capturarCabecario(linha):
            CNPJEmpresa = str(linha.iloc[34]).replace('/', '').replace('.', '').replace('-', '')

            return f"|0000|{CNPJEmpresa}|" \
                   f"\n|0160|9|Servicos|"


        def formatar_texto(linha):
            ## Aqui começa a linha 0020
            CNPJ = str(linha.iloc[10]).replace('/', '').replace('.', '').replace('-', '')
            NomeContratual = str(linha.iloc[11])
            Nome10Char = str(linha.iloc[11])[:10]
            Endereco = str(linha.iloc[13])
            nEndereco_str = str(linha.iloc[14])
            # Verifica se o valor é 'S/N' antes de tentar converter para int
            if nEndereco_str.isdigit():
                nEndereco = int(nEndereco_str)
            else:
                # Atribui um valor padrão (por exemplo, 0) se for 'S/N'
                nEndereco = 0
            compEndereco = str(linha.iloc[15])
            bairro = str(linha.iloc[16])
            obterCodigo = str(linha.iloc[17])
            UF = str(linha.iloc[18])
            CEP = str(linha.iloc[19]).replace('-', '')
            IE = str(linha.iloc[36])
            IM = str(linha.iloc[8]).replace('.', '').replace('-', '')
            ## Aqui finaliza a linha 0020

            ## Aqui começa a linha 1000
            Acumulador = Acumuladores.fazerProcv(int(linha.iloc[28]))
            nNota = str(int(linha.iloc[1]))
            dataNota = str(linha.iloc[7])[:10]
            valordaNota = str(linha.iloc[26]).replace('.', '')
            CodigoServico = int(linha.iloc[28])


            ## Aqui finaliza a linha 1000

            CRF = str(linha[coluna_55] + linha[coluna_56] + linha[coluna_60]).replace('.', ',')
            IRRF = str(linha.iloc[58]).replace('.', ',')

            # Verifica se o valor na coluna 57 é uma string antes de chamar replace
            if isinstance(linha.iloc[57], str):
                INSS = str(linha.iloc[57]).replace('.', ',')
            else:
                INSS = str(linha.iloc[57])

            recolhimentoIR = str(Acumuladores.procvIR(int(linha.iloc[28])).replace('.', ','))
            text = ""

            if float(INSS.replace('.', '').replace(',', '')) != 0:
                compInss = f"\n|1020|26||{valordaNota}|11,00|{INSS}|||||{valordaNota}|2631||||"
            else:
                compInss = ''
            if Acumuladores.Procv1020(int(linha.iloc[28])) == "S":
                if int(linha.iloc[21]) == 0:
                    natRendimento = str(Acumuladores.procvNatRendimento(int(linha.iloc[28])))
                    text = f"\n|1020|25||{valordaNota}|4,65|{CRF}|||||{valordaNota}|595207||||{natRendimento}|" \
                           f"\n|1020|16||{valordaNota}|1,50|{IRRF}|||||{valordaNota}|{recolhimentoIR}||||{natRendimento}|" \
                           f"{compInss}"
                else:
                    text = f"{compInss}"
            elif Acumuladores.Procv1020(int(linha.iloc[28])) == "*":
                if int(linha.iloc[21]) == 0:
                    natRendimento = str(Acumuladores.procvNatRendimento(int(linha.iloc[28])))
                    text = f"\n|1020|16||{valordaNota}|1,50|{IRRF}|||||{valordaNota}|{recolhimentoIR}||||{natRendimento}|" \
                       f"{compInss}"
            else:
                text = f"{compInss}"

            return f"|0020|{CNPJ}|{NomeContratual}|{Nome10Char}|{Endereco}|{nEndereco}|{compEndereco}|{bairro}|3550308|{UF}||{CEP}||{IM}||||||||N|7|N|N|||||||||" \
                   f"\n|1000|39|{CNPJ}||{Acumulador}|1.933||{nNota}|||{dataNota}|{dataNota}|{valordaNota}||||T||||||||||||||||||||||{valordaNota}||||||||||||||||||||||||||||||||||||||||||||||||||||||0|||||" \
                   f"{text}" \
 \
                # Aplique a função à DataFrame
        texto_formatado = linhas_filtradas.apply(formatar_texto, axis=1)
        cabecario = capturarCabecario(linhas_filtradas.iloc[0])

        resultado_final = ''
        if len(linhas_filtradas) > 0:
            resultadoFinal = [cabecario]
            # Exiba os textos formatados
            for texto in texto_formatado:
                resultadoFinal.append(texto)

            resultado_final = '\n'.join(resultadoFinal)

        return resultado_final

    except UnicodeDecodeError:
        # Se houver um erro de decodificação, tente usar outra codificação
        print("Erro de decodificação. Tente outra codificação.")

def processar_arquivoNFTS(caminho_do_arquivo):
    try:
        dados = pd.read_csv(caminho_do_arquivo, delimiter=';', encoding='ISO-8859-1')

        # Acesse a coluna correspondente ao índice 73 (considerando que o índice começa em 0)
        notas = dados.iloc[:, 0]  # 0 é o índice da primeira coluna

        # Filtra o DataFrame para incluir apenas as linhas em que o valor na coluna 73 é igual a 2
        linhas_filtradas = dados.loc[notas == "4"].copy().astype('object')

        linhas_filtradas.fillna("", inplace=True)
        # Defina uma função para formatar o texto
        def capturarCabecario(linha):
            CNPJEmpresa = str(linha.iloc[9]).replace('/', '').replace('.', '').replace('-', '')
            return f"|0000|{CNPJEmpresa}|" \
                   f"\n|0160|9|Servicos|"
        def formatar_texto(linha):
            ## Aqui começa a linha 0020
            CNPJ = str(linha.iloc[33]).replace('/', '').replace('.', '').replace('-', '')
            ## Aqui começa a linha 1000
            Acumulador = Acumuladores.fazerProcv(int(linha.iloc[27]))
            nNota = str(int(linha.iloc[5]))
            dataNota = str(linha.iloc[6])[:10]
            valordaNota = str(linha.iloc[25]).replace('.', '')
            CodigoServico = int(linha.iloc[27])
            if str(linha.iloc[42]) == "SP":
                codEstado = "1"
            else:
                codEstado = "2"


            recolhimentoIR = str(Acumuladores.procvIR(int(linha.iloc[27])).replace('.', ','))
            text = ""

            if Acumuladores.Procv1020(int(linha.iloc[27])) == "S":
                if int(linha.iloc[20]) == 0:
                    natRendimento = str(Acumuladores.procvNatRendimento(int(linha.iloc[27])))
                    text = f"\n|1020|25||{valordaNota}|4,65||||||{valordaNota}|595207||||{natRendimento}|" \
                           f"\n|1020|16||{valordaNota}|1,50||||||{valordaNota}|{recolhimentoIR}||||{natRendimento}|"
            elif Acumuladores.Procv1020(int(linha.iloc[27])) == "*":
                if int(linha.iloc[20]) == 0:
                    natRendimento = str(Acumuladores.procvNatRendimento(int(linha.iloc[27])))
                    text = f"\n|1020|16||{valordaNota}|1,50||||||{valordaNota}|{recolhimentoIR}||||{natRendimento}|"

            return f"|1000|39|{CNPJ}||{Acumulador}|{codEstado}.933||{nNota}|||{dataNota}|{dataNota}|{valordaNota}||||T||||||||||||||||||||||{valordaNota}||||||||||||||||||||||||||||||||||||||||||||||||||||||0|||||" \
                   f"{text}"
                # Aplique a função à DataFrame
        texto_formatado = linhas_filtradas.apply(formatar_texto, axis=1)
        cabecario = capturarCabecario(linhas_filtradas.iloc[0])

        resultado_final = ''
        if len(linhas_filtradas) > 0:
            resultadoFinal = [cabecario]
            # Exiba os textos formatados
            for texto in texto_formatado:
                resultadoFinal.append(texto)

            resultado_final = '\n'.join(resultadoFinal)

        return resultado_final

    except UnicodeDecodeError:
        # Se houver um erro de decodificação, tente usar outra codificação
        print("Erro de decodificação. Tente outra codificação.")
def selecionar_arquivo():
    caminho_do_arquivo = filedialog.askopenfilename()
    if caminho_do_arquivo:
        resultado = processar_arquivoNF(caminho_do_arquivo)
        print(resultado)

