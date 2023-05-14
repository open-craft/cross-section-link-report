# cross-section-link-report
Script to generate report about the cross sectional links used in course

1. Create a new file called `config.yml` based on `confiy.yml.example`. Populate all the variables there.
2. Install requirements
```
pip install -r requirement.txt
```
3. Execute script 
```
python ./generate_report.py
```
4. If script runs succesfully, a report file called `report.html` should be generated in the report path configured in the configs.

> **Note**
> To speed up the process of fetching xblock data, we batch the requests and fire them simultaneously. You can optimize the batch size using the REQUEST_BATCH_SIZE config to speed up the process or to prevent rate-limiting