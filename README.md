# Repositório para jogar minhas paradas de web sraping

Para referencia futura

Após configurar o seu `pyenv` e o `pyenv-virtualenv` (veja abaixo), certifique que esteja instalado os requisitos. 

```
pip install requisitos.txt
```

## Configurando o Pyenv Virtualnv e ativação automática

Configurar a ativação automática com `pyenv` e `pyenv-virtualenv` envolve alguns passos para garantir que, ao navegar até um diretório que contém um projeto Python, a versão de Python correspondente e o ambiente virtual sejam ativados automaticamente. Aqui está um guia mais detalhado sobre como configurá-lo:

### 1. Instalar `pyenv`

Primeiro, você precisa instalar `pyenv`. O método de instalação pode variar dependendo do seu sistema operacional. No macOS, você pode usar o Homebrew:

```bash
brew update
brew install pyenv
```

Para sistemas Ubuntu/Debian, você pode instalar clonando o repositório `pyenv` e adicionando comandos de inicialização ao arquivo de configuração do seu shell (por exemplo, `.bashrc` ou `.zshrc`):

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```

### 2. Instalar `pyenv-virtualenv`

Após instalar `pyenv`, instale `pyenv-virtualenv`. Se você estiver usando Homebrew no macOS, pode instalá-lo diretamente:

```bash
brew install pyenv-virtualenv
```

Para Ubuntu/Debian, após clonar o repositório `pyenv`, clone o repositório `pyenv-virtualenv` no diretório de plugins do `pyenv`:

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
```

Em seguida, adicione o comando de inicialização ao arquivo de configuração do seu shell:

```bash
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
exec "$SHELL"
```

### 3. Configurar o Shell para Ativação Automática

O recurso de ativação automática é habilitado adicionando o comando `pyenv virtualenv-init` ao arquivo de configuração do seu shell, como mostrado no passo anterior. Este comando configura hooks no shell que detectam automaticamente quando você entra em um diretório com um arquivo `.python-version` (criado pelo comando `pyenv local <version>`) e ativa o ambiente virtual correspondente.

Certifique-se de que as linhas que você adicionou ao seu `.bashrc` ou `.zshrc` estão corretamente colocadas e que você reiniciou seu terminal (ou usou `exec "$SHELL"`) para que as alterações tenham efeito.

### 4. Uso

Com `pyenv` e `pyenv-virtualenv` instalados e a ativação automática configurada, você pode começar a usá-los:

- **Instale uma versão do Python** (se necessário): `pyenv install 3.8.5`
- **Crie um ambiente virtual** para um projeto: `pyenv virtualenv 3.8.5 myproject-3.8.5`
- **Defina a versão local do Python** e ative o ambiente virtual automaticamente: Navegue até o diretório do seu projeto e use `pyenv local myproject-3.8.5`.

Agora, sempre que você entrar neste diretório, `pyenv` e `pyenv-virtualenv` ativarão automaticamente o ambiente virtual `myproject-3.8.5` para você. Quando você sair do diretório, o ambiente será desativado.

Lembre-se, se você abrir uma nova janela ou aba do terminal, você deve estar no diretório do projeto para que a ativação automática ocorra. Se não ativar automaticamente, certifique-se de que as alterações no arquivo de configuração do seu shell foram aplicadas corretamente e que você reiniciou seu terminal ou carregou o arquivo de configuração.
