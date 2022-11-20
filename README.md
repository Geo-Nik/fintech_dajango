# fintech_dajango
1. The app reads data about bank accounts from fintech/data/accounts.xlsx (fintech/db_app/management/commands/FAO.py)
2. The app uses API (fintech/db_app/management/commands/URL_.py) and readed data to get user accounts restrictions (fintech/db_app/management/commands/restrictions.py)
3. The app creates and updetes model according to the obtained data.
