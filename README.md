# Como rodar o projeto (Linux)
- Requisitos
    - Python 3.10.2
    - Pip
    - Virtualenv


- Criação do ambiente virtual
```python -m venv venv```

- Ativação do ambiente virtual
```source venv/bin/activate```

- Instalação das dependências
```pip install -r requirements.txt```

- Fazer o download da biblioteca Clang [Clique aqui](https://download.qt.io/development_releases/prebuilt/libclang/libclang-release_70-based-linux-Rhel7.2-gcc5.3-x86_64.7z)

- Desempacotar a biblioteca
```7z x libclang-release_70-based-linux-Rhel7.2-gcc5.3-x86_64.7z```

- Definir a variável de ambiente LLVM_INSTALL_DIR
```export LLVM_INSTALL_DIR=$PWD/libclang```

- Para rodar o projeto
```python main.py```