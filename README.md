# IRWA

## TL;DR
This repository contains the implementation of a search engine for the Information Retrieval and Web Analytics course, 
part of the Mathematical Engineering in Data Science degree at Pompeu Fabra University.

## Usage
### Step 1: Git clone the repository to your local system
```bash
git clone git@github.com:iv97n/irwa.git
```
### Step 2: Create a venv in the root of your project and install dependencies

**Create the virtual environment**
```bash
python -m venv venv
```
If the ``python`` command is not recognized, try using ``python3``.  

**Activate the virtual environment**
```bash
source venv/bin/activate
```
**Install the requirements.txt dependencies**
```bash
pip install -r requirements.txt
```

### Step 3: Create a ipykernel
```bash
ipython kernel install --user --name=venv
```
### Step 4: Select the ipykernel and run the code
The code is executed from the python notebooks located in the ``notebooks/`` folder. To select the suitable kernel for 
executing them, once you have opened Jupyter Notebook go to Kernel>>Change Kernel and select the ``venv`` kernel.