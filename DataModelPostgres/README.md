### Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals.
The purpose of this excercise it to create a star schema database in postgres, in order to allow the retrieve data insights upon any query defined by the business.

Sparkify is a music startup and their data so far comes from two sources in json format.
The analytical goal of this exercise if to model this given data and orchestrate it in a way that is useful to the business. For this, we will create a star schema, meaning one fact table in the center that takes the information from the surrounding dimension tables.

More in details, we will define the tables to be created with CREATE statements, defining dependancies and data types. INSERT statements will also be defines to allow insertion of data in the newly created tables and robust enough to handle conflicts as well. After having defined the dimension tables we will, through a join query be able to retrieve and in turn populate the central dimension table - which will be the main focus for business queries.

### How to run the Python scripts
I have run the python scripts by executing i.e. **%run sql_queries.py** in a jupyter notebook. Please advice on how to get it to run through the terminal. 

### An explanation of the files in the repository
sql_queries.py = where the various CREATE and INSERT statements are built
create_tables.py = contains lines of code to create and connect to the Sparkify database and is responsible of executing sql_queries.py within its functions
etl.ipynb = extract, transform, load data work done at the jupyter notebook level
etl.py = neat and clean code make into functions in order to create and populate the database more seemlessly
data = where json files containing song data and log data are found
test.ipynb = used in order to check that tables are being correctly populated and run sanity tests at the end

### State and justify your database schema design and ETL pipeline.
For the amount and complexity of data provided I believe it makes sense to go with a simple star schema, and create a central fact table to run various queries onto. As opposed to a snowflake schema where dependancies multiply and there may be more fact models and more dimension nodes.

The ETL pipeline built is quite intuitive, it extracts the data provided in the json and only in one occation (time table) we perform a little feature engineering to create non existing fields. 

