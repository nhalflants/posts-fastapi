# Fast API

## Setup 

**Setup Project Virtual Env**

`> python3 -m venv venv`

`> source venv/bin/activate`

Select Python Interpreter > `./venv/bin/python`

**Install FastAPI**

`pip install fastapi`

**Install ASGI server**

`pip install "uvicorn[standard]"`

**Create main.py file**

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

**Run python file**

`uvicorn main:app --reload`

- `main`: the file `main.py` (the Python "module").
- `app`: the object created inside of `main.py` with the line `app = FastAPI()`.
- `--reload`: make the server restart after code changes. Only do this for development.

Open your browser at http://127.0.0.1:8000

**Alembic Setup**

Database change management tool

Add the alembic command to the virtual environment. 
`pip install alembic`

Init alembic in the following directory "alembic"
`alembic init alembic`

In the created `alembic` directory `env.py` file change 
`target_metadata = Base.metadata` (`Base` class should be imported from the `models` file describing the table structure) and overide the sqlalchemy URL config by adding :

`config.set_main_option("sqlalchemy.url", f"postgresql+psycopg2://...`

Make sure that there are no existing table in the database. 

Create new revision file 
`alembic revision -m "create posts table"`

Upgrade to revision file by specifying revision number
`alembic upgrade fbd8ee385be5`. Further upgrade can be done via `alembic upgrade head` (head is fetching the latest revision)

Downgrade to revision file by specifying earlier revision number to which we would like to roll back.
`alembic downgrade fbd8ee385be5` or `-1` instead of of revision number to go to previous version.

Autogenerate revision based on sqlachelmy table models structure 
`alembic revision --autogenerate -m "generate votes tables"`

**Git Setup**

Create `.gitignore` file

Run `pip freeze > requirements.txt` to list all packages/dependencies and versions installed 