# Deploy

Aqui estão os dados de referência para deploy de uma aplicação Django, de acordo
com as aulas do meu curso de Django na Udemy.

## Criando um servidor

Como vamos usar um servidor na nuvem (cloud server), é interessante que você
utilize algum serviço gratuito para isso. Recomendo a Google Cloud Platform.

Caso não tenha como usar a Google Cloud Platform, um servidor em máquina virtual
também funciona perfeitamente. Porém, não será possível disponibilizar a
aplicação online na Internet. VirtualBox (Windows, Linux e macOS intel),
Parallels (macOS M1), UTM (macOS M1), são alguns dos softwares mencionados
indicados para isso.

Siga as instruções da aula para criar um servidor na Google Cloud Platform.

### Chaves SSH

Para criar chaves ssh no seu computador, utilize o comando ssh-keygen. Se você
já tem chaves SSH no computador e por algum motivo queira usar outra, use o
comando:

```
ssh-keygen -t rsa -b 4096 -f CAMINHO+NOME_DA_CHAVE
```

Lembre-se que a pasta .ssh deve existir dentro da pasta do seu usuário para que
seja possível criar a chave SSH. Muito comum ocorrer erros no Windows por falta
dessa pasta.

Para conectar-se ao servidor usando uma chave SSH com caminho personalizado,
utilize:

```
ssh IP_OU_HOST -i CAMINHO+NOME_DA_CHAVE
```

### Ao entrar no servidor

A primeira coisa será atualizar tudo:

```
sudo apt update -y
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install build-essential -y
sudo apt install python3.9 python3.9-venv python3.9-dev -y
sudo apt install nginx -y
sudo apt install certbot python3-certbot-nginx -y
sudo apt install postgresql postgresql-contrib -y
sudo apt install libpq-dev -y
sudo apt install git
```

# Configurando Postegres

sudo -u postgres psql

 - Criando usuário
CREATE ROLE thiagoesantos WITH LOGIN SUPERUSER CREATEDB CREATEROLE PASSWORD '123456';

 - Criando base de dados
CREATE DATABASE basededados WITH OWNER thiagoesantos;

 - Dando permissões
GRANT ALL PRIVILEGES ON DATABASE basededados TO thiagoesantos;

 - Saindo
\q

sudo systemctl restart postegresql

# Configurando git

git config --global user.name "Thiago Santos"
git config --global user.email "playsd395@gmail.com"
git config --global init.defaultBranch main

# Criando um repositório no servidor

mkdir -p ~/app_bare
cd ~/app_bare
git init --bare
cd ~


mkdir -p ~/app_repo
git init
git remote add origin ~/app_bare

# Configurando remote na máquina local

git remote add app_bare cursodjango:~/app_bare
git push app_bare main

# No app_repo

git pull origin <branch>
Ativar ambiente virtual
pip install -r requirementes.txt
pip install psycopg2
pip install gunicorn


