# FitTude Repo

Esse repositório contém todas as funções para manipulação de dados da aplicação principal [FitTude](https://github.com/lcsouza2/fittude)

## Setup
**Sequência de passos:**

Considerando que o poetry não está instalado:
1. Clonar com `git clone https://github.com/lcsouza2/fittude_repo`
2. Instalar o poetry com `pip install poetry`
3. Navegue até o repositório e execute `poetry install --no-root`

Provavelmente a IDE reconhecerá automaticamente o novo ambiente virtual, porém, se não reconhecer basta executar `poetry env info` 

A saída deve ser algo como:
```
Virtualenv
Python:         3.12.3
Implementation: CPython
Path:           ~/.cache/pypoetry/virtualenvs/repo-fittude-0x3FuZFt-py3.12
Executable:     ~/.cache/pypoetry/virtualenvs/repo-fittude-0x3FuZFt-py3.12/bin/python
Valid:          True

Base
Platform:   linux
OS:         posix
Python:     3.12.3
Path:       /usr
Executable: /usr/bin/python3.12
```

Basta copiar o caminho fornecido em Executable na seção Virtualenv e usar como caminho do ambiente virtual na IDE