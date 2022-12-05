# WORK IN PROGRESS
# How to build the db solution
To create the tables at a database, you can execute the scaffolding on file _PostgreSQL/build_scaffolding.psql_.

This scaffolding can be executed with the below command on your CLI:
```commandline
{path to psql executable} -h {server host} -U {user name} -d {database name} -p {port} -f {path to build_scaffolding.psql} -L {path to file where to write logs}
```

You will need to create a file on folder _PostgreSQL/sql_scripts/accounting/permissions_ granting permissions to user.
This permissions are based on the environment. Scaffolding will identify the environment by the name of the database, 
so:
    - database_name like '%dev%' -> dev environment -> file name: dev.sql
    - database_name like '%test%' -> test environment -> file name: test.sql
    - database_name like '%prod%' -> prod environment -> file name: prod.sql

test.sql file should be as follows:
```text
CREATE USER IF NOT EXISTS {test_user} WITH PASSWORD '{test_user_password}';

GRANT ALL ON SCHEMA accounting to {test_user};
GRANT ALL ON TABLE accounting.account_types TO {test_user};
GRANT ALL ON SEQUENCE accounting.account_types_account_type_id_seq TO {test_user};

GRANT ALL ON TABLE accounting.accounts TO {test_user};
GRANT ALL ON SEQUENCE accounting.accounts_account_id_seq TO {test_user};

GRANT ALL ON TABLE accounting.entry_types TO {test_user};
GRANT ALL ON SEQUENCE accounting.entry_types_entry_type_id_seq TO {test_user};

GRANT ALL ON TABLE accounting.transactions TO {test_user};
GRANT ALL ON SEQUENCE accounting.transactions_transaction_id_seq TO {test_user};

GRANT ALL ON TABLE accounting.ledger_entries TO {test_user};
```