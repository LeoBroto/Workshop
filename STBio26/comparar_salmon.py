#!/usr/bin/env python3
"""
comparar_salmon.py — Minicurso de Bioinformatica, bloco de transcriptomica.

Função: Lê dois arquivos quant.sf do salmon (controle e tratado/infectado),
agrega os transcritos por simbolo do gene, e gera uma tabela comparativa
ordenada por inducao.

Uso:
    python3 comparar_salmon.py quant_mock/quant.sf quant_cov2/quant.sf

Uso com nomes personalizados para as colunas:
    python3 comparar_salmon.py quant_mock/quant.sf quant_cov2/quant.sf \
        --nome-a Controle --nome-b SARS_CoV_2 --saida tabela_comparacao.tsv
"""


import argparse
import math
import statistics
import sys
from collections import defaultdict


# Pseudocontagem somada ao TPM antes do log2, para evitar divisao por zero.
PSEUDO = 1.0


# TPM minimo (na amostra mais expressa) para um gene entrar no ranking.
# Sem esse filtro o topo da lista vira ruido de genes com TPM ~0.3 -> 3.
TPM_MIN = 5.0




def ler_quant(caminho):
    """Le um quant.sf e devolve dois dicionarios agregados por gene: TPM e NumReads.


    O nome do transcrito foi construido por nos como ENST00000123.4_SIMBOLO
    (ver o passo de limpeza do FASTA do GENCODE). Aqui separamos no ultimo '_'
    para recuperar o simbolo. Transcritos sem '_' (como o SARS-CoV-2) mantem
    o nome inteiro.
    """
    tpm = defaultdict(float)
    reads = defaultdict(float)


    try:
        with open(caminho) as fh:
            cabecalho = fh.readline()
            if not cabecalho.startswith("Name"):
                sys.exit(f"ERRO: {caminho} nao parece um quant.sf "
                         f"(primeira linha: {cabecalho[:60]!r})")


            for linha in fh:
                campos = linha.rstrip("\n").split("\t")
                if len(campos) < 5:
                    continue
                nome, _len, _efflen, valor_tpm, valor_reads = campos[:5]


                # ENST00000641515.2_OR4F5 -> OR4F5 ; SARS-CoV-2 -> SARS-CoV-2
                gene = nome.rsplit("_", 1)[-1] if "_" in nome else nome


                tpm[gene] += float(valor_tpm)
                reads[gene] += float(valor_reads)
    except FileNotFoundError:
        sys.exit(f"ERRO: arquivo nao encontrado: {caminho}")


    if not tpm:
        sys.exit(f"ERRO: {caminho} nao tinha nenhuma linha de dados.")


    return tpm, reads




def main():
    ap = argparse.ArgumentParser(
        description="Compara dois quant.sf do salmon, agregando por gene.")
    ap.add_argument("quant_a", help="quant.sf da amostra CONTROLE")
    ap.add_argument("quant_b", help="quant.sf da amostra TRATADA/INFECTADA")
    ap.add_argument("--nome-a", default="controle", help="rotulo da amostra A")
    ap.add_argument("--nome-b", default="tratado", help="rotulo da amostra B")
    ap.add_argument("--saida", default="tabela_comparacao.tsv",
                    help="arquivo TSV de saida")
    ap.add_argument("--tpm-min", type=float, default=TPM_MIN,
                    help=f"TPM minimo para entrar no ranking (padrao {TPM_MIN})")
    ap.add_argument("--top", type=int, default=10,
                    help="quantos genes mostrar em cada direcao")
    args = ap.parse_args()


    tpm_a, reads_a = ler_quant(args.quant_a)
    tpm_b, reads_b = ler_quant(args.quant_b)


    genes = sorted(set(tpm_a) | set(tpm_b))


    linhas = []
    for g in genes:
        ta, tb = tpm_a.get(g, 0.0), tpm_b.get(g, 0.0)
        ra, rb = reads_a.get(g, 0.0), reads_b.get(g, 0.0)
        log2fc = math.log2((tb + PSEUDO) / (ta + PSEUDO))
        expresso = max(ta, tb) >= args.tpm_min
        linhas.append((g, ta, tb, ra, rb, log2fc, expresso))


    # --- arquivo de saida: todos os genes, ordenados por log2FC decrescente ---
    linhas.sort(key=lambda x: x[5], reverse=True)
    with open(args.saida, "w") as out:
        out.write("\t".join([
            "gene",
            f"TPM_{args.nome_a}", f"TPM_{args.nome_b}",
            f"reads_{args.nome_a}", f"reads_{args.nome_b}",
            "log2FC", "expresso",
        ]) + "\n")
        for g, ta, tb, ra, rb, fc, exp in linhas:
            out.write(f"{g}\t{ta:.3f}\t{tb:.3f}\t{ra:.1f}\t{rb:.1f}\t"
                      f"{fc:+.3f}\t{'sim' if exp else 'nao'}\n")


    # --- relatorio no terminal ---
    filtradas = [l for l in linhas if l[6]]


    print(f"\nGenes na referencia .......... {len(genes)}")
    print(f"Genes com TPM >= {args.tpm_min} .......... {len(filtradas)}")
    print(f"Tabela completa gravada em ... {args.saida}")


    # Os blocos 2 e 3 tem a mesma largura, para caberem lado a lado
    # num terminal de 80 colunas: 38 + 4 de espaco + 38 = 80.
    LARGURA = 38


    # O bloco 1 tem colunas mais largas e fica sozinho no topo: 46 colunas.
    LARGURA_B1 = 46


    def bloco_tpm(titulo, dados):
        """Bloco 1: gene + TPM nas duas amostras + log2FC, colunas largas."""
        rot_a, rot_b = args.nome_a[:11], args.nome_b[:11]
        linhas_b = [titulo[:LARGURA_B1],
                    f"{'gene':<14}{rot_a:>12}{rot_b:>12}{'log2FC':>8}",
                    "-" * LARGURA_B1]
        for g, ta, tb, _ra, _rb, fc, _e in dados:
            linhas_b.append(f"{g[:14]:<14}{ta:>12.1f}{tb:>12.1f}{fc:>+8.2f}")
        return linhas_b


    def bloco_fc(titulo, dados):
        """Blocos 2 e 3: mesmas colunas, compactadas para caber lado a lado."""
        # 8 e nao 9: garante ao menos um espaco entre os cabecalhos.
        rot_a, rot_b = args.nome_a[:8], args.nome_b[:8]
        linhas_b = [titulo[:LARGURA],
                    f"{'gene':<12}{rot_a:>9}{rot_b:>9}{'log2FC':>8}",
                    "-" * LARGURA]
        for g, ta, tb, _ra, _rb, fc, _e in dados:
            linhas_b.append(f"{g[:12]:<12}{ta:>9.1f}{tb:>9.1f}{fc:>+8.2f}")
        return linhas_b


    def lado_a_lado(esq, dir_, espaco=4):
        """Imprime dois blocos de texto lado a lado, alinhados pelo topo."""
        for i in range(max(len(esq), len(dir_))):
            e = esq[i] if i < len(esq) else ""
            d = dir_[i] if i < len(dir_) else ""
            print(f"{e:<{LARGURA}}{' ' * espaco}{d}".rstrip())


    # Bloco 1, sozinho no topo: os mais expressos no controle.
    mais_expressos = sorted(linhas, key=lambda x: x[1], reverse=True)[:args.top]
    print()
    for linha in bloco_tpm(f"TOP {args.top} MAIS EXPRESSOS", mais_expressos):
        print(linha)


    # Genes de manutencao nao deveriam mudar. Se todos caem juntos por um valor
    # parecido, essa mediana estima o VIES DE COMPOSICAO da biblioteca (escala),
    # nao regulacao. E o mesmo raciocinio da normalizacao do DESeq2/edgeR.
    mediana_fc = statistics.median(l[5] for l in mais_expressos)
    print("-" * LARGURA_B1)
    print(f"{'mediana':<14}{'':>12}{'':>12}{mediana_fc:>+8.2f}"
          f"   <- vies de composicao")


    # Blocos 2 e 3, lado a lado: induzidos e reprimidos.
    print()
    lado_a_lado(
        bloco_fc(f"TOP {args.top} INDUZIDOS EM {args.nome_b[:11].upper()}",
                 filtradas[:args.top]),
        bloco_fc(f"TOP {args.top} REPRIMIDOS EM {args.nome_b[:11].upper()}",
                 filtradas[-args.top:][::-1]),
    )


    # --- carga viral, se o SARS-CoV-2 estiver na referencia ---
    for chave in ("SARS-CoV-2", "NC_045512.2"):
        if chave in tpm_a or chave in tpm_b:
            print(f"\nCARGA VIRAL ({chave})")
            print(f"  {args.nome_a:<14} TPM={tpm_a.get(chave, 0.0):>12.1f}  "
                  f"reads={reads_a.get(chave, 0.0):>12.1f}")
            print(f"  {args.nome_b:<14} TPM={tpm_b.get(chave, 0.0):>12.1f}  "
                  f"reads={reads_b.get(chave, 0.0):>12.1f}")
            break
    print()




if __name__ == "__main__":
    main()
