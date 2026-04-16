# New-News
AI NLP project analyzing sentiments towards designated topics from major news companies, using these results to determine the correlation between different topics to determine how the news companies will report on current events.



### To set up the virtual environment

In the project folder, run the following commands in order:

```
python -m venv venv
\venv\Scripts\activate
pip install -r requirements.txt
```

This ensures the environment stores all the necessary packages.



### To run

In the project folder, run

```
python .\run.py [-d | --data] path/to/csv [-m | --mode] [train | test]
```


Resources:
https://www.baeldung.com/cs/absa
https://beautiful-soup-4.readthedocs.io/en/latest/
https://huggingface.co/yangheng/deberta-v3-base-absa-v1.1
https://numpy.org/doc/stable/user/index.html#user
https://www.sciencedirect.com/science/article/pii/S1319157823002057?__cf_chl_tk=OshSBkDNFberTgR.nEG33heTiauRxb94y1l0lXNRKuM-1776296301-1.0.1.1-PsYYn_oH.qYsKRjAkcQk5L6OIIe69b5k2ucMWGgfWPI