# TRANSCRIPTÔMICA COMPARATIVA
### Desenvolvido por 
### Revisado por 
***
&emsp; Nesta parte do curso, pretendemos comparar duas amostras de RNA-seq, uma controle e uma condição, quantificando a abundância relativa de transcritos, medida em TPM (transcripts per million), e identificar genes que são mais transcritos em cada situação.

&emsp; O aluno deve sair capaz de fazer o processamento básico de arquivos FASTQ até a obtenção de uma tabela de abundância (.tsv) e, adicionalmente, uma interpretação funcional. 

&emsp; Pela questão de tempo e complexidade da aula, minha intenção é a apresentar o seguinte

&emsp; Este trabalho foi feito no esforço contra a pandemia de COVID-19 e fez um screening de transcrição em diversos tipos celulares infectados por diversos vírus respiratórios. Usaremos duas corridas específicas. **SRR11517744** (controle, células CALU-3, tipo de adenocarcinoma de pulmão) e **SRR11517748** (doença, para SARS-CoV2). 
> Para a prática foram escolhidos os dados [Blanco-Melo et al., Cell 2020](http://www.cell.com/pb-assets/products/coronavirus/CELL_CELL-D-20-00985.pdf) :page_facing_up:. 

&emsp; Os autores relatam que os genes induzidos por SARS-CoV são
- ISGs efetores: IFIT1, IFIT2, IFIT3, ISG15, IFI6, IFI27, MX1, MX2, OAS1, OAS2, OAS3, OASL, RSAD2, IFITM1, IFITM3, HERC5, USP18, BST2, XAF1
- Sensores e fatores de transcrição: DDX58 (RIG-I), IFIH1 (MDA5), STAT1, STAT2, IRF7, IRF9
- Quimiocinas: CXCL10, CXCL11, CCL5, IL6
- Interferons: IFNB1, IFNL1, IFNL2, IFNL3

2. Dados utilizados
Estudo		GSE147507 — Blanco-Melo et al., Cell 2020
Fontes		GEO GSE147507 · ENA PRJNA615032 
BioProject		PRJNA615032
Modelo		Células Calu-3 (epitélio pulmonar humano)
Controle		SRR11517744 — Calu-3 controle
Condição		SRR11517748 — Calu-3 SARS-CoV-2
Layout		Single-end, Illumina NextSeq 500
Referência		GENCODE v50 (GRCh38) e genoma SARS-CoV-2 (NC_045512.2)
Quantificador	salmon

** AULA PRÁTICA **

1. **Baixando e preparando os arquivos**
Para o RNA-seq vamos usar os arquivos SRR11517744.subsample.fastq

Vamos baixar a referência para o transcriptoma humano GENCODEv50 (Jul 2026)
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/latest_release/gencode.v50.transcripts.fa.gz

Vamos baixar também o genoma de SARS-CoV2
wget -O NC_045512.2.fa "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi 

Como os programas que vamos usar só aceitam uma entrada, vamos concatenar (unir em um único arquivo) a referência GENCODE com o genoma viral NC_045512.2
cat NC_045512.2.fa gencode.v50.transcripts.fa > ref.fa

2 **Controle de qualidade**
Como boa prática, é necessário fazer o controle de qualidade e remoção de adaptadores. O melhor e mais rápido hoje é o fastp

fastp -i SRR11517744.subsample.fastq -o SRR11517744.quality.fastq -j report.json -h report.html
    O que significa o comando: 
    fastp é o programa que apara os adaptadores e avalia a qualidade ao mesmo tempo
    -i é o arquivo de entrada
    -o é o arquivo de saída
    -j e -h são os relatórios de qualidade no formato JSON e HTML, respectivamente. 

O output “quality” não importa muito para ser sincero. Interessante mostrar o report.html onde tem estatísticas de qualidade.

3. **Construindo o ìndex**
O que é um índice? Uma estrutura de busca pré-processada. Sem ela, para cada _read_ o software precisaria que varrer 110 mil transcritos. É o mesmo princípio do índice remissivo no fim de um livro. Isso reduz o tempo de processamento!

Existem diversos programas que estimam a transcrição em RNA-seq como o RSEM, Kallisto e FeatureCounts. Vamos usar o [Salmon]([url](https://github.com/COMBINE-lab/salmon)). Seu índex se faz com o comando:

salmon index -t ref.fa -i index_dir -k 31 -p 4

4. **Quantificando**
Vamos comparar o perfil de transcrição das duas amostras baixadas, por isso, vamos rodar duas vezes. Quando acabar uma, rode a segunda
salmon quant -i index_dir -l A -r SRR11517744.fastq -p 4 -o quantificação_controle
salmon quant -i index_dir -l A -r SRR11517748.fastq -p 4 -o quantificação_doença
    O que significa o comando: 
    Salmon é o pacote, quant é o programa do Salmon que faz a estimativa
     -i é a entrada
     -r é o arquivos com as _reads_
     -p é o número de processadores
     -o é a pasta de saída
5. **Visualização**
O Salmon tem os seguintes arquivos de saída que nos importam:
aux_info/meta_info.json, que é o arquivo de metadados e quant.sf, um tsv (arquivo tabulado) com os dados de quantificação; 
quant.sf tem as seguintes colunas:

Name    			    Header do transcrito ou nome do gene/transcrito/proteína
Length  			    Tamanho, em nucleotídeos
EffectiveLength		Número de posições que um fragmento médio pode se alinhar ao transcrito 
TPM				        Métrica normalizada de expressão (_reads per million_)
NumReads			    Valor absoluto de leituras que mapearam em cima do transcrito

Para observar as 30 primeiras linhas
head -30 quant.sf | column -t

ordena coluna 4a (número) de maneira decrescente
sort -nrk4 quant.sf | head -30 | column -t 
O esperado é uma lista ordenada por TPM:
(IMAGEM)

6.**Tabela comparativa usando script python**
Temos um script escrito em python chamado comparar_salmon.py
Vamos usar ele para comparar os dois arquivos quant.sf
Para usar, use o comando
python compara_salmon.py quant_1 quant_2 --nome-a --nome-b --saida
    exemplo: python comparar_salmon.py quantificação_controle/quant.sf  quantificação_doença/quant.sf --nome-a Controle --nome-b SARS_CoV_2 --saida comparacao_salmon.tsv
No output temos:
-No cabeçalho > o quento da referência foi mapeada (referência é transcriptoma geral humano e a célula é pulmonar)
-Bloco 1 “TOP 10 MAIS EXPRESSOS” > mostra o fold change entre as amostras
-Bloco 2 “TOP 10 INDUZIDOS EM SARS_COV_2” > mostra aqueles genes que mais aumentaram a expressão em SARS-CoV
-Bloco 2 “TOP 10 REPRIMIDOS EM SARS_COV_2” > mostra aqueles genes que mais diminuiram a expressão em SARS-CoV
-Bloco 4 “CARGA VIRAL (SARS-CoV-2)” > é uma informação didática, não é carga viral real, mas, mostra o “Boom” de TPM de transcritos do vírus. 

(IMAGEM)

7.**Anotação funcional**
Boa. Agora sabemos quais os transcritos mais expressos em cada uma das amostras e conseguimos comparar elas, mas, qual o significado biológico disso?
Para isso, vamos descobrir quais os Processos Biológicos estão anotados para cada gene. 
Vamos fazer isso para os 150 transcritos mais expressos:
awk '$7=="sim" && $6>1 {print $1}' tabela_comparacao.tsv | head -n150
    O que significa esse comando?
    awk é o programa que manipula textos. A lógica é "se estiver marcado como 'Sim' na coluna 7 e a coluna 6 for maior que 1, imprime a coluna 1 e me mostre os 150 primeiros"
    	$6>1 para os genes induzidos
    	$6>1 para os genes reprimidos





