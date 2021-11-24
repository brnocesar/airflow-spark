# Data Pipelines com Apache Airflow e Spark

Construção de um _data pipeline_ para um processo de ELT seguindo o modelo _batch_. O processo roda uma vez ao dia e armazena os dados em um _data lake_ no formato JSON. Esse repositório foi feito acompanhando o curso ["Engenharia de dados: Conhecendo Apache Airflow"](https://cursos.alura.com.br/course/engenharia-dados-apache-airflow) da Alura.

O objetivo da aplicação é extrair dados do Twitter e tranformar esses dados de forma que possam ser analisados da forma mais simples possível.

As principais ferramentas utilizadas são: Apache Airflow, para orquestrar os processos (agendar o horário de cada processo e monitorar sua execução); e Apache Spark para processamento distribuído.

0. [Rodando a aplicação](#0-rodando-a-aplicação)  
1. [Preparando o ambiente virtual](#1-preparando-o-ambiente-virtual)  
2. [Iniciado o Airflow](#2-iniciado-o-airflow)  
3. [Consumindo a API do Twitter](#3-consumindo-a-api-do-twitter)  
4. [Airflow](#4-airflow)  

## 0 Rodando a aplicação

Após clonar o projeto, execute os comandos abaixo na raiz do diretório clonado:

1. Instalar o pacote responsável por gerenciar os ambientes virtuais: `apt-get install python3-venv`
2. Criar ambiente virtual: `python3 -m venv .env`
3. Carregar ambiente virtual: `source .env/bin/activate`
4. Ativar a variável de ambiente: `export AIRFLOW_HOME=$(pwd)/airflow`
5. Iniciar o _web service_: `airflow webserver`
6. Acessando o _web service_: `http://localhost:8080`
7. Iniciar o agendador: `airflow scheduler`

## 1 Preparando o ambiente (virtual)

- Instalação do pacote no sistema:

```terminal
apt-get install python3-venv
```

- Criação do ambiente dentro da pasta que vai ficar a aplicação:

```terminal
mkdir airflow-spark
cd airflow-spark
python3 -m venv .env
```

- Carregando o ambiente:

```terminal
source .env/bin/activate
```

- Antes de instalar o Airflow é necessário criar uma variável de ambiente que aponte para pasta onde ele vai ficar. É necessário manter essa variável ativa para que o Airflow não seja instalado na _home_ do usuário, e depois de instalado, para que o terminal não vá la procurar pela aplicação.
  
```terminal
export AIRFLOW_HOME=$(pwd)/airflow
```

- Instalando o Apache Airflow:
  
```terminal
pip install apache-airflow==1.10.14 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.14/constraints-3.7.txt"
```

- Criando o banco de dados do Airflow:

```terminal
airflow db init
```

Esse comando cria uma pasta chamada `airflow` com arquivos de configurações (`airflow.cfg`), um banco SQLite (`airflow.db`), pasta de logs e testes unitários (`unittests.cfg`).

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)

## 2 Iniciado o Airflow

Para começar a trabalhar com o Airflow devemos rodar o _web service_, que é a interface gráfica do Airflow:

```terminal
airflow webserver
```

Após rodar o comando podemos observar algumas saídas no terminal como: o executor utilizado (sequencial, vem configurado por padrão), o local onde ficam armazenados os _dags_ e a porta em que ele está rodando (_Listening at_).

Agora podemos acessar o _web service_ no navegador através do endereço `http://localhost:8080`. Ao carregar podemos ver uma tabel com _DAGs_, suas informações de controle e alguns links. No topo da página existe um aviso informado que o _scheduler_ (agendador) não está rodando, então executamos o comando abaixo para iniciar esse segundo serviço:

```terminal
airflow scheduler
```

O agendador é o serviço que executa o _heart beat_, que fica observando quando um processo deve ser executado.

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)

## 3 Consumindo a API do Twitter

Vamos extrair os dados do Twitter consumindo sua API. Para isso é necessário primeiro criar um projeto no "portal do desenvolvedor" do Twitter. Em seguida começamos escrever o código Python a partir de um [exemplo](https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/2bd47d1ecfa31a1d71ed7902e5ac9c222d575331/Recent-Search/recent_search.py) da própria API.

Criamos um arquivo chamado `recent_search.py` e colamos o código de exemplo (_commit_ [8bba23a](https://github.com/brnocesar/alura/commit/8bba23af383beea399b157ec3c143d9ceffec8fc)). Logo no começo vemos que o _Bearer Token_ é obtido através de uma variável de ambiente do sistema operacional:

```python
def auth():
    return os.environ.get("BEARER_TOKEN")
```

Podemos criar uma variável de ambiente para o _token_ou alterar o código para que essa informação seja recuperada de outro lugar (_commit_ [eee61a7](https://github.com/brnocesar/alura/commit/eee61a7256f69d4a9b2cbde7e0ca28c4f6cd6f3a)). Só não é uma boa idéia deixar isso em _plain text_ dentro do código.

Em seguida partimos para o método `create_url()` onde começamos alterando a variável `query` para que a busca seja feita em relação a `"AluraOnline"` e depois passamos para a variável `tweet_fields`, alterando os campos que devem ser retornados (a lista dos parâmetros disponíveis pode ser encontrada na [documentação](https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent) da API).

Também criamos outras duas variáveis, uma com campos referentes aos usuários e outra com as datas de início e fim da consulta. Lembrando que a API retorna apenas dados dos últimos sete dias para uma conta gratuita (_commit_ [5ab8e41](https://github.com/brnocesar/alura/commit/5ab8e4179f7a18e5f5cff5633d039e89924bc747)).

Neste ponto podemos testar esse código. Então se tudo funcionou corretamente, após executar o código Python, devemos ter como retorno um JSON com três itens: `data`, `includes` e `meta`. Em `data` é um vetor com os _tweets_ e suas informações, `includes` possui a chave `users` com um vetor com as informações dos usuários. E por fim temos o item `meta`, que possui um campo chamado `next_token` indicando que existem mais dados para retornar e para retornar esses dados devemos implementar a paginação no código (_commit_ [150ba91](https://github.com/brnocesar/alura/commit/150ba914eedd766ee338a9b7c61f4bc8cb9069b8)).

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)

## 4 Airflow

- projeto open source
- google (clound composer) e aws
- dag (gráficos aciclicos direcionados)
  - conjunto de passos conectados, com inicio e fim
    - podem ser executados de forma sequencial ou paralela
    - são executados através de operadores
      - são _nodes_ de um DAG
      - caracteristicas de um operador: indepotência, isosalmento e atomicidade
      - 3 tipos de operadores
  - como limpar os dags default da instalação?
- serviços
  - webservice: ui, monitoramento
  - scheduler: agendador, heartbeat (fica observando quando os dags devem executar), executores (sequencial, local, cluster)

### 4.1 Criando uma conexão

O Airflow permite acessar diversas fontes de dados externas e geralmente é necessário alguma credencial para esses acessos, usuário e senha para um banco de dados ou um _token_ para uma API.

O Airflow possui um "repositório" que centraliza todas as conexões para que qualquer DAG possa utiliza-lás. O _web service_ nos fornece um CRUD para as conexões, no menu **Admin -> Connections**.

Ao acessar a página de _create_ podemos preencher os seguintes campos do formulário para criar a conexão com a API do Twitter:

- Conn Id: twitter_default
- Conn Type: HTTP
- Host: https://api.twitter.com
- Extra: {"Authorization": "Bearer `<coloque o token aqui>`"}

### 4.2 Criando um _hook_

A forma mais adequada de se conectar a alguma ferramenta externa é através de uma interface comum que seja desacoplada do _pipeline_. No Airflow, essas interfaces são chamadas de _hooks_. Nos _hooks_ são colocados todo código necessário para interagir com a ferramenta bem como a definição da conexão que deve ser usada.

Na seção 1 (ou 2) após criarmos o Banco do Airflow, foi criada uma estrutura de pastas e arquivos de configuração, sendo a raiz uma pasta chamada `airflow`. Dentro dessa pasta vamos criar o arquivo `plugins/hooks/twitter_hook.py` e dentro desse arquivo escrevemos nossa classe de _hook_ (_commit_ [b790f86](https://github.com/brnocesar/alura/commit/b790f86acd9c5764853fa0200ede81fcd4e7e416)).

Como o _hook_ vai interagir com uma API, faz mais sentido herdarmos uma classe mais adequada para essa finalidade. Partimos do código de exemplo escrito na seção 3 e o modificamos de acordo com a classe base (_commit_ [5e513a2](https://github.com/brnocesar/alura/commit/5e513a2aced7066c26c66b5cd4a86f062edc391f)).

### 4.3 Criando um operador

Dentro da pasta `plugins` vamos criar uma nova pasta chamada `operator` e dentro dela o arquivo `twitter_operator.py`. Da mesma forma como os _hooks_, operadores são classes que seguem uma estrutura já definida e herdam uma classe base. 

Obrigatóriamente devemos implementar o método `execute` recebendo um parâmetro chamado `context`, que traz alguns parâmetros do Airflow. Este é o método chamado para executar o DAG.

No método `__init__` aplicamos o _decorator_ `apply_defaults`, que facilita o envio/captura de parâmetros padrâo das DAGs(?), definimos os mesmo parâmetros recebidos pelo _hook_ e chamamos o método `super` (_commit_ [70f9b98](https://github.com/brnocesar/alura/commit/70f9b98f1c9ddedfc078161648fe4f1b523e58a3)).

No passo anterior escrevemos um _hook_ responsável por interagir com a API do Twitter, então agora vamos conectá-lo ao operador. Dessa forma teremos uma tarefa responsável por buscar os dados no Twitter e tendo as características de um operador. Por hora vamos apenas retornar os dados na saída padrão, então apenas importamos a classe de _hook_ que escrevemos, a instânciamos no método `execute` e iteramos sobre o retorno do método `run()`. Para testar o operador devemos criar uma tarefa (DAG) de testes (_commit_ [34b6548](https://github.com/brnocesar/alura/commit/34b65483276517d5e0f14cfee2367f4e6473b62a)), e ao executar o código devemos esperar o mesmo comportamento da seçao 3.

Agora vamos alterar a classe para que os dados coletados sejam armazenados em arquivos. Começamos adicionando um novo parâmetro ao construtor da classe do operador, que receberá o caminho em que o arquivo deve ser salvo. Em seguida alteramos a parte "printava" os dados para que eles sejam enviado para um arquivo. De modo a garantir que o caminho do arquivo sempre exista, implementamos o método `create_parent_folder`.

Sempre que instânciamos uma tarefa no Airflow podemos ter acesso a dados específicos da execução através das **macros** e eu posso receber essas informações para cada um dos meus parâmetros usando _jinja template_. Devemos indicar em quais parâmetros isso será permitido e fazemos isso através do `template_fields`. O `template_fields` é uma lista com os parâmtros que queremos permitir esse acesso e é definido como um parâmetro para a classe. Para que o _jinja template_ seja tranformado, ao invés de executar o operador vou executar a tarefa fictícia, pois ela irá fazer isso(?). Agora quando executamos o código deve ser criado um arquivo JSON com os dados coletados (_commit_ [faa2f3e](https://github.com/brnocesar/alura/commit/faa2f3eaebd6cb94d57abc253ab2b1d6dfa96744)).

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)

## Apêndice

### _Data pipelines_

Um _data pipeline_ é uma cadeia de processos (_workflows_) que manipula dados seguindo os formatos ETL ou ELT - E de _extration_ (extração), T para _transformation_ (tranfosrmação) e L de _loading_ (armazenamento). Ou seja, servem para movimentar dados de uma ou mais fontes, para um ou mais destinos, (e se necessário) transformando-os durante o processo.

_Data pipelines_ podem seguir dois modelos de funcionamento: _batch_ e _streaming_. _Batch_ significa lote, neste formato os dados são primeiro agrupados e então processados. O tamanho dos lotes e a frequência (a cada segundos ou até mesmo meses) com que seram extraídos vai depender da infraestrutura e da finalidade.

Por sua vez, _streaming_ significa fluxo. Neste formato os dados são extraídos seguindo um fluxo constante e o processamento ocorre em tempo real conforme os dados vão chegando.

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)
