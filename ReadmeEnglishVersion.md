
# BidInAction (Jewelry Showcase - Caixa)
## 🎯 About the Project

**BidInAction** is a Windows tool built in Python to automate and optimize the search for jewelry auctions on the official auction portal of Caixa Econômica Federal (Brazilian federal savings bank).

If your goal is to quickly filter the vast auction catalog and focus only on opportunities for **Jewelry and Precious Articles**, this tool saves valuable time by making it easier to spot relevant items.

### ✨ Key Features

- **Direct Connection:** Performs HTTP requests and intuitive navigation (via Requests/PySide6) to access up-to-date data from Caixa's auction portal.
- **Smart Filter:** Automatically applies filters to display only auctions categorized as Jewelry.
- **Data Extraction:** Extracts crucial information from each auction (date, location, number, etc.).

## ⬇️ Windows Installer Download

[![Download Installer](https://img.shields.io/badge/Download-Installer_v1.0.0-blue?style=for-the-badge&logo=windows)](https://drive.usercontent.google.com/u/0/uc?id=1VMk0bx-3N0VeGbsYxZcyR15vjY-vn-eS&export=download)

---

## 🚀 Run the Project in an Editor (Preferably VS Code)

Follow these instructions to set up and run the project locally.

### Prerequisites

You need **Python 3.x** and **`pip`** installed on your system.
Install the libraries from [requirements.txt](requirements.txt) using the command below:

```bash
pip install -r requirements.txt
```

#### 1. Clone the Repository

```bash
git clone https://github.com/dtdias/BidInAction
```

#### 2. Enter the project folder

```bash
cd BidInAction
```

#### 3. Run

```bash
python main.py

# Or press F5 in VS Code
```

---

### Build

- **Build the .exe:**
The executable was created using Nuitka. Below is the command used to compile it in the console:

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
```

- **Create the Setup:**
The setup was created using Inno Setup with the following [script](script-inno-setup/script-vitrine-caixa.iss).
