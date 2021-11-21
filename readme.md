# Data Pipelines com Apache Airflow e Spark

Construção de um _data pipeline_ para um processo de ELT seguindo o modelo _batch_. O processo roda uma vez ao dia e armazena os dados em um _data lake_ no formato JSON.

O objetivo da aplicação é extrair dados do Twitter e tranformar esses dados de forma que possam ser analisados da forma mais simples possível.

As principais ferramentas utilizadas são: Apache Airflow, para orquestrar os processos (agendar o horário de cada processo e monitorar sua execução); e Apache Spark para processamento distribuído.

0. [Rodando a aplicação](#0-rodando-a-aplicação)  
1. [Preparando o ambiente virtual](#1-preparando-o-ambiente-virtual)  
2. [Iniciado o Airflow](#2-iniciado-o-airflow)  

## 0 Rodando a aplicação

Após clonar o projeto, execute os comandos abaixo na raiz do diretório clonado:

1. Instalar o pacote responsável por gerenciar os ambientes virtuais: `apt-get install python3-venv`
2. Criar ambiente virtual: `python3 -m venv .env`
3. Carregar ambiente virtual: `source .env/bin/activate`
4. Ativar a variável de ambiente: `export AIRFLOW_HOME=$(pwd)/airflow`
5. Iniciar o _web service_: `airflow webserver`
6. Acessando o _web service_: `http://localhost:8080`
7. Iniciar o agendador: `airflow scheduler`
8. : ``

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

- Antes de instalar o Airflow é necessário criar uma variável de ambiente que aponte para pasta onde ele vai vai ficar. É necessário manter essa variável ativa para que o Airflow não seja instalado na _home_ do usuário, e depois de instalado, para que o terminal não vá la procurar pela aplicação.
  
```terminal
export AIRFLOW_HOME=$(pwd)/airflow
```

- Instalando o Apache Airflow:
  
```terminal
pip install apache-airflow==1.10.14 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.14/constraints-3.7.txt"
```

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)

## 2 Iniciado o Airflow

O primeiro passo é iniciar (criar?) o banco de dados do Airflow com o comando:

```terminal
airflow db init
```

Esse comando vai criar uma pasta chamada `airflow` com alguns arquivos como: o de configurações (`airflow.cfg`), o banco de dados SQLite (`airflow.db`), pasta de logs e testes unitários (`unittests.cfg`).

Após isso devemos rodar o _web service_, que é a interface gráfica do Airflow:

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

## Apêndice

### _Data pipelines_

Um _data pipeline_ é uma cadeia de processos (_workflows_) que manipula dados seguindo os formatos ETL ou ELT - E de _extration_ (extração), T para _transformation_ (tranfosrmação) e L de _loading_ (armazenamento). Ou seja, servem para movimentar dados de uma ou mais fontes, para um ou mais destinos, (e se necessário) transformando-os durante o processo.

_Data pipelines_ podem seguir dois modelos de funcionamento: _batch_ e _streaming_. _Batch_ significa lote, neste formato os dados são primeiro agrupados e então processados. O tamanho dos lotes e a frequência (a cada segundos ou até mesmo meses) com que seram extraídos vai depender da infraestrutura e da finalidade.

Por sua vez, _streaming_ significa fluxo. Neste formato os dados são extraídos seguindo um fluxo constante e o processamento ocorre em tempo real conforme os dados vão chegando.

### Apache Airflow

- projeto open source
- google e aws
- dag (como limpar os dags default da instalação?)
- serviços
  - webservice: ui, monitoramento
  - scheduler: agendador, heartbeat (fica observando quando os dags devem executar), executores (sequencial, local, cluster)

### Apache Spark

[↑ voltar ao topo](#data-pipelines-com-apache-airflow-e-spark)
