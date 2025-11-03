# BidInAction (Vitrine de Joias - Caixa) 
[![English Version]( https://img.shields.io/badge/Translate-English_Version-green)](https://github.com/dtdias/BidInAction/blob/main/ReadmeEnglishVersion.md)
## 🎯 Sobre o Projeto

O **BidInAction** é uma ferramenta windows desenvolvida em Python para automatizar e otimizar a busca por leilões de joias no site oficial de Leilões de Bens da Caixa Econômica Federal.

Se o seu interesse é filtrar rapidamente o vasto catálogo de leilões e focar apenas nas oportunidades de **Joias e Artigos Preciosos**, esta ferramenta economiza tempo valioso, facilitando a identificação de itens relevantes.

### ✨ Funcionalidades Principais

* **Conexão Direta:** Realiza requisições HTTP e Navegação Intuitiva (via Requests/PySide6) para acessar os dados atualizados do portal de leilões da Caixa.
* **Filtro Inteligente:** Aplica filtros automáticos para exibir apenas leilões classificados como Joias.
* **Extração de Dados:** Extrai informações cruciais de cada leilão (data, local, número, etc.).

## ⬇️ Download do Setup de instalação no Windows:

[![Baixar Instalador](https://img.shields.io/badge/Download-Instalador_v1.0.0-blue?style=for-the-badge&logo=windows)](https://drive.usercontent.google.com/u/0/uc?id=1VMk0bx-3N0VeGbsYxZcyR15vjY-vn-eS&export=download)
---

## 🚀 Executar o projeto no Editor (Preferencialmente VSCODE)

Siga estas instruções para configurar e rodar o projeto localmente.

### Pré-requisitos

Você precisará ter o **Python 3.x** e o **`pip`** (gerenciador de pacotes) instalados no seu sistema.
Você precisará instalar as bibliotecas do [requirements.txt](requirements.txt) utilizando o comando abaixo
```bash 
pip install -r requirements.txt
```

#### 1. Clonagem do Repositório

```bash
git clone https://github.com/dtdias/BidInAction
```
#### 2. Entrar na pasta do projeto
```bash
cd BidInAction
```
#### 3. Executar 
```bash
python main.py

#### Ou apertar F5 pelo VSCODE
```
---
### Compilação

* **Compilação do .exe:**
O executavel foi criado utilizando o Nuitka, segue abaixo o comando utilizado no console para compilar:
```bash
python -m nuitka ^    --onefile ^    --windows-console-mode=disable ^    --msvc=latest ^    --enable-plugin=pyside6 ^    --output-filename="Vitrine de Joias - Caixa.exe" ^    --windows-icon-from-ico=icon/caixa-logo.ico ^    --windows-product-name="Vitrine de Joias - Caixa" ^    --windows-company-name="Sua Empresa" ^    --windows-file-version="1.0.0.0" ^    --windows-product-version="1.0.0.0" ^    --windows-file-description="Vitrine de Joias - Caixa" ^    --include-data-file=icon/caixa-logo.ico=icon/caixa-logo.ico ^    --include-data-file=assets/logo_vitrine_de_joias.png=assets/logo_vitrine_de_joias.png ^    main.py
```
* **Criação do Setup**
O setup foi criado utilizando o Inno Setup utilizando [script](script-inno-setup/script-vitrine-caixa.iss)
