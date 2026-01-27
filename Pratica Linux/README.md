# Workshop de Bioinformática do IV Curso de Genética no Verão (USP)
Criado por Felipe S. Salles | Linkedin | Lattes

Assitentes: Sophia Pereira Saraiva e Bruno J. Teixeira de Melo
***
#### Bem vindo ao mini tutorial do Workshop
###### Após a breve explicação sobre tipo de arquivos e abordagens de tipos de estudos, vamos iniciar o aprendizado do "terminal"


Para começar iremos introduzir o terminal e a linguagem Bash/Linux. O terminal de um computador é a área onde conversamos com o computador sem a interface gráfica (portanto não utilizamos mouse para mover os arquivos ou clicar neles), permitindo usar scripts e comandos básicos para realizar as tarefas computacionais.

Para quem possiu o sistema Linux basta apertar `Ctrl` + `Alt` + `T` . E para outros sistemas operacionais há aplicativos ou outras interfaces:

**Windows:** WSL, Ubunto e Xmobe

**Android:** Andronix ou Termux

**IOS:** iSH ou a-Shell

Iniciaremos com a visalização da tela e os primeiros comandos mais simples. Agora chamaremos todos os arquivos seguintes dependendo do conteundo dele. E cada um terá uma `terminação` especifica. E tambem toda pasta agora será chamada de `diretório`. 

Procure o aplicativo chamado `Ubunto`

**Ubunto2.09.1** :o:

Depois vamos iniciar com o comando que lista os arquivos e diretórios de um determinado local
```
$ ls
programas tutorial_workshop
```

Veja a diferença utilizando as opções `-l`, `-a`, `-h`, `-s`. Pode fazer combinação entre todas elas.
```
$ ls -l
$ ls -lh
$ ls -lash
```

Interessante notar que as opções dos comandos não tem ordem correta, somente em alguns poucos casos onde uma opção tem que obrigatóriamente vir antes de outra.

Encontrou o diretório chamado `tutorial_workshop`? Vamos utilizar então agora um PADRÃO de comando que irá se repetir
```
[comando] -[opção] [objeto]
``` 

Portanto iremos usar o comando `ls` no diretório `tutorial_workshop`
```
$ ls tutorial_workshop
catch_genes.sh eukaria_protein.fasta transform_single_line_fasta.sh 
```

> Se quiser pode usar o mesmo comando no outro diretório para ver qual o conteudo, pode se usar.

Agora entramemos no `diretório` chamado `tutorial_workshop`. Se fosse um computador com interface gráfica você clicaria duas vezes na pasta para entrar nela mas no nosso caso será em linha de comando, ao mesmo tempo que já mostraremos o conteudo dela. So é possivel por conta do `;`, que entende que isso seria uma linha nova:
``` 
$ cd tutorial_workshop ; ls -lh
```

Percebe-se que há dois script (verde) de final ".sh" e um fasta. Utilizaremos um `catch_genes.sh` para recuperarmos as sequências do arquivo fasta das proteinas de Eukariotos.
***
#### Inspecionar os arquivos
Agora vamos inspecionar os arquivos. O tamanho já nos foi dado ( ), precisamos ver o conteudo. Para inspecionar os arquivos temos diversos comandos: `head`, `tail`, `more`, `less`, `cat`, `tac` ... Cada um com suas especificidades. :warning: Procure não usar o `cat` ou `tac` para arquivos muito grandes :warning:

``` 
$ head eukaria_protein.fasta
```

OU

``` 
$ more eukaria_protein.fasta
```

Caso queira entender o que cada comando faz, você pode:
1. Testar com "tentativa e erro", utilizando o padrão `[comando]` `-[opção]` `[objeto]`
2. Utilizar o comando manual `man`, information`info` ou a opção `--help` para os comandos.
> Para sair do manual basta clicar na tecla 'Q' de quit

``` 
$ man [comando]
$ info [comando]
$ [comando] --help
```

Agora inspecionaremos o arquivo fasta com um pouco mais de detalhes. Contaremos quantas sequencias há no arquivo `fasta`. Cada início de sequência tem seu cabeçalho iniciado por `>___` e na linha de baixo o conteudo da sequência. Iremos tambem calcular quantas linhas INICIAM com o aminoacido `Metionina` e a quantidade de linhas totais no arquivo. E ai qual o resultado? Discuta o por quê disso.

```
$ grep -c ">" eukaria_protein.fasta
1257723
$ grep -c "^M" eukaria_protein.fasta
1257723
$ wc -l eukaria_protein.fasta
1257723
```

OU

```
$ grep ">" eukaria_protein.fasta | wc -l
1257723
$ grep "^M" eukaria_protein.fasta | wc -l
1257723
$ wc -l eukaria_protein.fasta
1257723
```

O primeiro comando conta automaticamente o numero de linhas que apresentam o sinal '>' e o segundo comando seleciona as linhas que apresentam '>' - ou seja, ele seleciona os 'headers', e DEPOIS conta o número de linhas total do comando anterior. Só é possivel isso pois utilizamos o 'pipe' `|` - significa 'tubo'  ou 'cano' - portanto o resultado (output) do `grep` entra em um cano e segue automaticametne para o proximo comando.

Agora inspecione com `cat` os arquivos `*.sh` (**Shell**). Pode observar que ambos tem um cabeçalho único: `#!/bin/bash`.
Esta linha exige que o arquivo seja lido pelo computador de um jeito especial. E isso trasnforma os arquivos textos em "scripts".
***
#### Baixar os arquivos
Vamos iniciar e baixar nossa proteina de interesse no site do NCBI.

⚠️ Agora importante se certificar que a proteina a ser baixada está no diretório que será trabalhado e com algum nome que seja útil e informativo para você. Portanto vamos renomear, caso necessário, e mover o arquivo até o diretório `tutorial-workshop`

Vai até o site do [NCBI](https://www.ncbi.nlm.nih.gov/protein/), e procura na aba de pesquisa pela proteina X e clique na aba Y e com o botão esquerdo clique e copie o link do arquivo.
Cole junto ao comando `wget`
```
$ wget [link]
```

Mudando o nome  ou mova o arquivo para o diretório que você quer trabalhar
```
$ mv [nome_antigo] [nome_novo]
$ mv [arquivo] -t [diretório]
```
***
#### Alinhamento local
Agora iremos rodar o primeiro programa, o BLAST, para alinhar as proteínas que queremos adquirir com a proteína alvo. Nesta etapa vale a pena e pesquisar e [ler um pouco sobre](https://pmc.ncbi.nlm.nih.gov/articles/PMC441573/). Utilizaremos o comando `blastp` para alinhar proteína com todas as outras proteínas.

```
$ ../programas/blast2.09+n/bin/blastp
```

Pode obsverar que o `[comando]` é `blastp`, as `-[opções]` são  `-o`, `-core` e o `[objeto]` esta definido na `-[opção]` `-i`.  

***
#### Alinhamento global
