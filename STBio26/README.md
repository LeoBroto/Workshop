# Workshop de Bioinformática da Semana Temática de Biologia 2026
## Toolbox de Bioinformática: ferramentas para análises ômicas
Criado por Felipe S. Salles || [LinkedIn](https://br.linkedin.com/in/felipe-simionato-salles-b3640120b) || [Lattes](http://lattes.cnpq.br/3781167913621025)

Criado por Leandro de Brito Gonçalves Gonçalves || [LinkedIn](https://www.linkedin.com/in/leandro-gon45/) || [Lattes](http://lattes.cnpq.br/3096958278950054)

Monitores: [Sophia Pereira Saraiva](http://lattes.cnpq.br/5576461458658817) e [Bruno J. Teixeira de Melo](http://lattes.cnpq.br/0513855441372488)
***

&emsp; Na biologia pós-NGS, análises computacionais são indispensáveis ao profissional biólogo. Contudo, o primeiro contato com dados NGS é muitas vezes intimidador devido à barreira da linha de comando. Este minicurso propõe-se a desmistificar a bioinformática, focando na introdução ao tema e no uso de ferramentas de alto padrão na literatura científica. A proposta está em conferir ao aluno um contato inicial para metodologias de bioinformáticas, preparando-o para os desafios reais da pós-graduação e do mercado biotecnológico. O objetivo é fornecer uma introdução teórico-prática às ferramentas essenciais de bioinformática. Faremos um apanhado dos softwares mais importantes de bioinfo para análises evolutivas e de NGS, de forma que os alunos saibam: Compreender, revisar e saber manipular arquivos (.fasta, .fastq, .sam/bam, .newick, etc); 
1. Navegar no NCBI, executar alinhamentos de sequências e inferências filogenéticas (BLAST, MAFFT, IQTree)
2. Compreender conceitos básicos de Genômica (Qualidade e Anotação)
3. Compreender conceitos básicos de transcriptômica: alinhamento contra genoma de referência e quantificação de expressão
> [!NOTE]
> [Slides](https://canva.link/1uvpn017843xvc6) compartilhado 🔓
***

### Primeiros passos
&emsp; Veremos primeiro mencionar nos bancos de dados mais conhecidos e utilizados na bioinformática: [STEBio26/Banco de dados.md](https://github.com/211295/Workshop/blob/main/STBio26/Banco%20de%20dados.md).

### Inicialização na bioinformática:
#### A estrutura lógica da linha de comando será basicamente esta:
## `COMANDO` + `-OPÇÃO` + `OBJETO` 

#### Principais comandos para manuzeio e manipulação de dados biológicos com a linguagem BASH. 
> [Curso referência](https://cursosextensao.usp.br/enrol/index.php?id=2285) e Disciplina [IBI5765](https://uspdigital.usp.br/janus/componente/disciplinasOferecidasInicial.jsf?action=3&sgldis=IBI5765) (realizada no Instituto de Ciências Biomédias), ministrado pelo Professor Dr. [João Marcelo Pareira Alves](https://scholar.google.com/citations?hl=pt-BR&user=kUPJajcAAAAJ).

| COMANDO | DESCRIÇÃO | OPÇÕES | Utilidades |
|:----------:|:----------------|:-----------------------------------------------:|:-----------------------------------------------------|
| _[ls](https://man7.org/linux/man-pages/man1/ls.1.html)_ | **L**ist **S**how :page_facing_up: = Mostra os arquivos presentes no _Diretório_/_Pasta_ | `-e` `-a` `-l` `-h` `-s` | Jeito rápido de ver os arquivos presentes, bem como seu tamanho (opções `-l` e `-h` juntas). |
| _[cd](https://man7.org/linux/man-pages/man1/cd.1p.html)_ | **C**hange **D**irectory :open_file_folder: :arrows_clockwise: :file_folder: = muda o _Diretório_/_Pasta_ atual de trabalho |  | É utilizado para "transitar" entre os diretórios de trabalho. |
| _[mv](https://man7.org/linux/man-pages/man1/mv.1.html)_ | **M**o**V**e :left_right_arrow: = Move arquivo ou _Diretório_/_Pasta_, OU modifica o nome | `-t` `-v` `-f` | Utilizado para modificar nome (move um arquivo para um "novo arquivo"), subscreve arquivos que estão em outros diretórios (opção `-f`). Move arquivos entre _Diretórios_/_Pastas_. |
| _[mkdir](https://man7.org/linux/man-pages/man1/mkdir.1.html)_ | **M**a**K** a **DIR**ectory :file_folder: = cria um _Diretório_/_Pasta_ de trabalho |  | É utilizado para transitar entre os diretórios de trabalho. |
| _[pwd](https://man7.org/linux/man-pages/man1/pwd.1.html)_ | **P**rint **W**ork **D**irectory :computer: = Mostra qual o _Diretório_/_Pasta_ atual de trabalho |  | Garante o nome correto do _Diretório_/_Pasta_ e do o caminho atual de trabalho para se inserir nos scripts. |
| _[cp](https://man7.org/linux/man-pages/man1/mkdir.1.html)_ | **C**o**P**y :copyright: = copia arquivos ou _Diretório_/_Pasta_ | `-t` | Importante lembrar que a cópia deve haver um nome diferente em um mesmo _Diretório_/_Pasta_. |
| _[cat](https://man7.org/linux/man-pages/man1/cat.1.html)_ | **C**onc**AT**enate :memo: = printa o conteuto de todos os arquivos concatenando seus conteudos | `-A` `-n` | Geralmente utilizado para verificar o conteúdo de arquivos pequenos. O inverso dele é o comando `TAC`. |
| _[less](https://man7.org/linux/man-pages/man1/less.1.html)_ | Mostra o conteúdo na tela do terminal em uma "tela a parte" :desktop_computer: | `-S` | Como outros comandos, utiliza-se para visualizar o arquivo mas neste caso este não printa, mostra somente o conteudo que cabe na tela. Utilizado para verificar tabelas de maneira organizada (opção `-S`). |
| _[more](https://man7.org/linux/man-pages/man1/more.1.html)_ | Mostra o conteúdo do arquivo somente na tela :desktop_computer: |  | Um modo de visualizar um arquivo. Visualização de parte do arquivo na tela bem como a porcentagem do arquivo que está presente na tela (podendo ter uma ideia do quão grande é o arquivo). Arquivo permanece printado como se fosse o `cat`. Para continuar vendo o arquivo basta apertar o barra de espaço. |
| _[head](https://man7.org/linux/man-pages/man1/head.1.html)_ | Mostra as primeiras linhas de um arquivo :bear: | `-n` | Um modo de visualizar as primeiras linhas de um arquivo, quando junto do `-n` podendo visualizar quantas linhas necessárias. |
| _[tail](https://man7.org/linux/man-pages/man1/tail.1.html)_ | Mostra as últimas linhas de um arquivo :beaver: | `-n` | Um modo de visualizar as últimas linhas de um arquivo (em ordem), quando junto do `-n` podendo visualizar quantas linhas necessárias. |
| _[touch](https://man7.org/linux/man-pages/man1/touch.1.html)_ | Cria um arquivo em branco :new::book: |  | Pode-se criar um arquivo novo com intuito de garantir que o _output_ sejam indexados ao arquivo novo (utilizando o sinal `>`). |
| _[nano](https://linux.die.net/man/1/nano)_ | **N**ano's **ANO**ther editor :black_nib: = Edita um arquivo texto (e até mesmo cria caso não exista) |  | Após a edição, deve-se apertar `CRTL` + `X`, e depois `Y` para salvar as alterações. Usado para criar os arquivos de scripts `.sh`|
| _[grep](https://man7.org/linux/man-pages/man1/grep.1.html)_ | Adquire/pega/seleciona linhas no arquivo com um padrão especificado :mag_right: :pushpin: | `-c` `-v` `-e` | Este será um potente comando utilizado para trabalhar com os arquivos de bioinformática que seguem algum padrão. A estrutura do comando será `comando` + `opção` + `"padrão"` + `arquivos` |
| _[sed](https://man7.org/linux/man-pages/man1/sed.1.html)_ |  Seleciona e edita o arquivo :scissors: | `-n 'Np'` `-n 'Nd'` `'s/<substituir>/<substituto/'` | Editor de arquivos muito completo, mantendo o original e disponibilizando na tela somente a troca especificada. |
| _[awk](https://man7.org/linux/man-pages/man1/awk.1p.html)_ | **A** **W** **K** :date: =  | `-F` | É utilizado para transitar entre os diretórios de trabalho |
| _[wc](https://man7.org/linux/man-pages/man1/wc.1.html)_ | **W**orld **C**ount :calling: = Conta o número de elementos de um arquivo, ou | `-l` | Garante o nome correto do _Diretório_/_Pasta_ e do o caminho atual de trabalho |
| _[cut](https://man7.org/linux/man-pages/man1/cut.1.html)_ | Corta o número de elementos de todas as linhas de um arquivo como se fossem colunas :scissors: | `-b` `-c` `-f` `-s` `-w` | Geralmente utilizado junto a outros comandos como o `cat`|
| _[colrm](https://man7.org/linux/man-pages/man1/colrm.1.html)_ | **COL**umn **R**e**M**ove = Remove a coluna de strings selecioanda |  | Utiliza-se junto de outros arquivos. Necessita-se dos números especificados |
| _[column](https://man7.org/linux/man-pages/man1/column.1.html)_ | Disponibiliza o arquivo em formato de "tabela" | `-d` `-S` `-t` `-J` | Facilita a visualização por tabular um _output_, já que geralmente as tabelas `.tsv` e `.csv` não organiza-se de maneira simétrica cada coluna |
| _[sort](https://man7.org/linux/man-pages/man1/sort.1.html)_ | Organiza o arquivo, ordenando de diversas formas :abc: :1234: | `-n` `-r` `-k` `-d` `-h` | Utiliza-se junto a outros comandos para organizar o _output_ gerado, podendo ser organizado em ordem alfabética ou numérica, ou em notação científica |
 
>[!WARNING]
> Outro comando básico porem fatal, é o _[rm](https://man7.org/linux/man-pages/man1/rm.1.html)_ (**R**e**M**ove), uma vez usado, não há mais volta
***

# Softwares de bioinformática
#### Esses programas/ferramentas utilizadas no tutorial são alternativas 

| PROGRAMA / FERRAMENTA | DESCRIÇÃO |
|:----------:|:--------------------------------------------------------------------------------------------------------------------|
| **[BLAST](https://www.ncbi.nlm.nih.gov/books/NBK279690/)** | _**B**asic **L**ocal **A**lignment **S**earch **T**ool_ é o programa de alinhamento local mais famoso e mais utilizado. Há diversas [funcionalidades](https://blast.ncbi.nlm.nih.gov/Blast.cgi) do uso do alinhador entre as moléculas de Amino Ácidos e Nucleotídeos (DNA e RNA). |
| **[MAFFT](https://mafft.cbrc.jp/alignment/software/linux.html)** | Programa de múltiplos alinhamentos **globais** das sequências necessárias. Homo logous regions are rapidly identified by the fast Fourier transform (FFT), in which an amino acid sequence is converted to a sequence composed of volume and polarity values of each amino acid residue. (ii) We propose a simplified scoring system that performs well for reducing CPU time and increasing the accuracy of alignments even for sequences having large insertions or extensions as well as distantly related sequences of similar length |
| **[IQTree](https://iqtree.github.io/)** | Large phylogenomics data sets require fast tree inference methods, especially for maximum-likelihood (ML) phylogenies. Fast programs exist, but due to inherent heuristics to find optimal trees, it is not clear whether the best tree is found. Thus, there is need for additional approaches that employ different search strategies to find ML trees and that are at the same time as fast as currently available ML programs. Utiliza o [Model Finder](https://www.nature.com/articles/nmeth.4285) como método de estimativa filogenética através do modelo de heterogeneidade de sitios. |
| **[fastp](https://github.com/opengene/fastp)** | A tool designed to provide ultrafast all-in-one preprocessing and quality control for FastQ data. This tool is designed for processing short reads (i.e. Illumina NovaSeq, MGI). Há diversas funções possiveis para o programa ex: filtragem, limpeza de bases, remove adaptadores, "cortagem" de alinhamento... |
| **[seqtk](https://github.com/lh3/seqtk)**| Seqtk is a fast and lightweight tool for processing sequences in the FASTA or FASTQ format. It seamlessly parses both FASTA and FASTQ files which can also be optionally compressed by gzip. |
| **[BWA](https://github.com/lh3/BWA)** | _**B**urrows-**W**heeler **A**ligner_ programa para alinhar sequências de DNA ou RNA (reads) contra um genoma de referência longo (ex: genoma Humano) |
| **[SAMTools](https://www.htslib.org/)** | A suite of programs for interacting with high-throughput sequencing data, used to read, write, edit, index, and view SAM, BAM, and CRAM format files |
| **[SRATools](https://github.com/ncbi/sra-tools)** | A tools set of NCBI to acesses, download and convert genomic sequencing data of SRA (Sequence Read Archive) database  |
| **[Salmon](https://combine-lab.github.io/salmon/)**  | Is a ultra-fast program for highly-accurate, transcript-level quantification from RNA-seq data. |


## websites para mexer com bioinformática
Site de alinhadores e [toolkit.tuebingen.mpg.de](https://toolkit.tuebingen.mpg.de/). Para outras ferramentas utiliza-se [Galaxy](https://galaxy-main.usegalaxy.org/)

## Lição de casa
Tutorial disponibilizado no [Canva.com](canva.com) para recriar as análises feitas durante a aula em uma plataforma online

https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#alt-h1
