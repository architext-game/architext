# Run locally for development

```bash
# local database
# from project root
docker-compose -f docker-compose-dev.yml up -d

# backend
# from /server
source venv/bin/activate
pip install -r requirements.txt
python -m architext.entrypoints.socketio.server

# web
# from /web
npm install
npm run dev
```

# Test

```bash
source venv/bin/activate

# run all tests using memory repositories
pytest

# run using in memory sql database
pytest --db

# run tests in folder
pytest tests/core/

# run specific test
pytest -k <test_name>
```


# Other info
- Tested and compatible with Python 3.12.8

