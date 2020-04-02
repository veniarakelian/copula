[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

# Copula
This is the official implementation in Python for: **Sovereign Risk Zones in Europe During and After the Debt Crisis.** 
<br /> [Veni Arakelian](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=492068), [Petros Dellaportas](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=383211), [Roberto Savona](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=365367), [Marika Vezzoli](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=1165311).
<br /> **Quantitative Finance 2019**
<br /> [[Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3217047&fbclid=IwAR0NVD4OpZEmGw0IaWVBtd4riLHyKzBrmBG2lhfD5qSWEvJuPlBR0OrrO80)]

## BibTex

If you find this code useful, please consider citing:

```
@article{doi:10.1080/14697688.2018.1562197,
author = {Veni Arakelian and Petros Dellaportas and Roberto Savona and Marika Vezzoli},
title = {Sovereign risk zones in Europe during and after the debt crisis},
journal = {Quantitative Finance},
volume = {19},
number = {6},
pages = {961-980},
year  = {2019},
publisher = {Routledge},
doi = {10.1080/14697688.2018.1562197},
URL = {https://doi.org/10.1080/14697688.2018.1562197},
eprint = {https://doi.org/10.1080/14697688.2018.1562197}
```

## Installation

Dependencies
~~~~~~~~~~~~

copula requires:

- numpy>=1.16
- copulae>=0.5.2
- scipy>=1.4.1
- pandas>=1.0.3


```
git clone https://github.com/PetropoulakisPanagiotis/copula.git
cd copula
pip install .
```

## Run an artificial example 
```
cd copula/copula
change the path in laplacetest_volatility.py line 10: 
df = read_excel("/home/petropoulakis/Desktop/copula-master/data/artificial_data_iosif.xlsx", sheet_name='Sheet1')  
python laplacetest_volatility.py
```
### Contributors 
* Petropoulakis Panagiotis petropoulakispanagiotis@gmail.com
