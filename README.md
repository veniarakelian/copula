# Copula
This is the official implementation in Python for
**[[Paper](https://arxiv.org)]

If you find this code useful, please consider citing:

```
@inproceedings{wang2019fast,
    title={Fast online object tracking and segmentation: A unifying approach},
    author={Wang, Qiang and Zhang, Li and Bertinetto, Luca and Hu, Weiming and Torr, Philip HS},
    booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
    year={2019}
}
```

## Installation
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

###### Acknowledgements
* [ambhas](https://github.com/neel9102/ambhas/blob/master/ambhas/copula.py) repository for the parameter estimation of copula
