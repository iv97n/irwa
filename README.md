# IRWA


## TL;DR
This repository contains the implementation of a search engine for the Information Retrieval and Web Analytics course, 
part of the Mathematical Engineering in Data Science degree at Pompeu Fabra University. The corpus of documents used is a collection of tweets related to the Farmers
Protests in 2021.

## Usage
The code is executed from the python notebooks located in the ``notebooks/`` folder. To run the code you will need to install the dependencies specified in the ``requirements.txt``file.  

The data folder is empty by default. To use the code you will need to populate it with the corresponding files.

Here is a step by step example of how to run the code using _Jupyter Notebook_ and _venv_. Other editors such as Visual Studio are also suitable options for running the code.

### Step 1: Git clone the repository to your local system
```bash
git clone git@github.com:iv97n/irwa.git
```
### Step 2: Create a venv in the root of your project and install dependencies

**Create the virtual environment**  
Windows
```bash
python -m venv venv
```
Ubuntu
```bash
python3 -m venv venv
```
**Activate the virtual environment**  
Windows
```bash
.\venv\bin\activate
```
Ubuntu
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