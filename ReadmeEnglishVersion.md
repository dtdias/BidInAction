BidInAction (Jewelry Showcase - Caixa)
🎯 About the Project
BidInAction is a Windows tool developed in Python to automate and optimize the search for jewelry auctions on the official Auctions of Goods website of the Brazilian Federal Savings Bank (Caixa Econômica Federal).

If your interest is to quickly filter the vast auction catalog and focus only on Jewelry and Precious Articles opportunities, this tool saves valuable time, facilitating the identification of relevant items.

✨ Key Features
Direct Connection: Performs HTTP requests and Intuitive Navigation (via Requests/PySide6) to access updated data from Caixa's auction portal.

Smart Filter: Automatically applies filters to display only auctions classified as Jewelry.

Data Extraction: Extracts crucial information from each auction (date, location, number, etc.).

⬇️ Download the Installation Setup for Windows:
🚀 Run the Project in the Editor (Preferably VSCODE)
Follow these instructions to set up and run the project locally.

Prerequisites
You will need to have Python 3.x and pip (package manager) installed on your system. You will need to install the libraries from requirements.txt using the command below:

Bash

pip install -r requirements.txt
1. Clone the Repository
Bash

git clone https://github.com/dtdias/BidInAction
2. Enter the project folder
Bash

cd BidInAction
3. Execute
Bash

python main.py
Or press F5 in VSCODE
---
### Compilation

* **Compiling the .exe:**
The executable was created using Nuitka. Below is the command used in the console for compilation:
```bash
python -m nuitka ^
    --onefile ^
    --windows-console-mode=disable ^
    --msvc=latest ^
    --enable-plugin=pyside6 ^
    --output-filename="Jewelry Showcase - Caixa.exe" ^
    --windows-icon-from-ico=icon/caixa-logo.ico ^
    --windows-product-name="Jewelry Showcase - Caixa" ^
    --windows-company-name="Your Company" ^
    --windows-file-version="1.0.0.0" ^
    --windows-product-version="1.0.0.0" ^
    --windows-file-description="Jewelry Showcase - Caixa" ^
    --include-data-file=icon/caixa-logo.ico=icon/caixa-logo.ico ^
    --include-data-file=assets/logo_vitrine_de_joias.png=assets/logo_vitrine_de_joias.png ^
    main.py