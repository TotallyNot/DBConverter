# Usage

Clone the repository and run

```
> python3 -m venv .
> . ./bin/activate
> pip install -r requirements.txt
```

You can then use the script to extract the tables from `OK.xml` and `Accounts.xml`.

```
> python3 xmlparser.py
```

Additionally you can provide the `--engine` argument, which will be passed to the [sqlalchemy.create_engine](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls). Provided the necessary adapters are installed, you can use this to extract the tables to any sqlalchemy compatible database.
For mysql/mariadb the syntax would be

```
> python xmparser.py -- engine 'mysql+mysqladapter://{user}:{password}@{host}/{database}'
``` 

for instance.