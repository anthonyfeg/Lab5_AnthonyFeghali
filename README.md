# Lab 5 Postman and APIs

This project implements the Flask and SQLite user management API specified in the lab. It includes a Postman collection named **Flask user app**, a **Flask local** environment, saved live response examples, automated tests, local Git history, and a folder of proof screenshots.

## Verified results

- All five required API endpoints are implemented.
- The Postman collection has eight requests covering CRUD and verification, with one real response example per request.
- All eight requests use `{{base_url}}` from the environment. POST stores the generated `user_id` for subsequent requests.
- Newman 6.2.2 executed the collection: **8 requests, 27 assertions, 0 failures**.
- Python tests: **9 passed**, including persistence through an independent SQLite connection, validation, missing records, CORS, and repeatable schema initialization.
- A database commit was made on `main`; REST changes were committed on `feature/rest-api` and merged into `main` with a merge commit.

## Postman workspace and remaining steps

The collection and environment have now been imported into Anthony Feghali's Postman workspace, with Flask local selected. Actual workspace screenshots are in `proof-screenshots/postman-workspace`: collection overview, five CRUD examples, environment values, and a request using `{{base_url}}`.

[Open the Postman collection](https://a-r-feghali-486396.postman.co/workspace/5229428a-ad27-46da-89bc-4648eaf32e3e/collection/58733018-df64eaf9-04a0-4219-b865-699070c98254).

The example screenshots show the saved responses imported from the verified local execution. They do not represent a new live run in the Postman web client. The web client currently uses Cloud Agent; localhost requests need the desktop client or Desktop Agent. The original 13 screenshots in the parent proof folder show recorded execution reports; the eight new screenshots in the subfolder show the actual Postman application.

The project is published at [anthonyfeg/Lab5_AnthonyFeghali](https://github.com/anthonyfeg/Lab5_AnthonyFeghali). Both `main` and `feature/rest-api` are pushed. The direct browser GET check remains pending because the embedded browser blocked local API navigation; the API and collection were successfully verified through real HTTP requests and Newman.

## Start the API

Open this folder in VS Code. In the integrated terminal, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python database.py
python app.py
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.

The API runs at `http://127.0.0.1:5000`. Keep that terminal running. `database.db` is created automatically in this project directory. A demonstration John Doe record is included in the supplied database after testing, so the GET endpoints have something to display. The collection creates and deletes its own record and leaves other records intact.

`sqlite3` is part of Python's standard library; a separate `db-sqlite3` package is unnecessary. Flask-Cors is explicitly included because the lab imports it. If port 5000 is occupied, run `PORT=5001 python app.py` on macOS/Linux and change the Postman `base_url` to `http://127.0.0.1:5001`.

## Required endpoints

| Method | Path | Successful result |
| --- | --- | --- |
| GET | `/api/users` | 200 and a JSON array |
| GET | `/api/users/<user_id>` | 200 and one user |
| POST | `/api/users/add` | 201 and the inserted user |
| PUT | `/api/users/update` | 200 and the updated user |
| DELETE | `/api/users/delete/<user_id>` | 200 and a deletion message |

POST and PUT require non-empty string values for `name`, `email`, `phone`, `address`, and `country`. PUT also requires a positive integer `user_id`. Missing users return 404; invalid JSON fields return 400; a non-JSON request body returns 415. The endpoint paths and database columns match the lab. The application improves the sample's exception handling, connection cleanup, idempotent table creation, and response statuses.

Example POST body:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "067765434567",
  "address": "John Doe Street, Innsbruck",
  "country": "Austria"
}
```

## Use in Postman

1. Open the workspace linked above. The collection and environment are already imported there. To use a different workspace, sign in and select it.
2. Import `postman/Flask user app.postman_collection.json` and `postman/Flask local.postman_environment.json`.
3. Select **Flask local** as the active environment and confirm `base_url` is `http://127.0.0.1:5000`.
4. Keep Flask running. Use the desktop client, or a desktop agent with the web client, to reach localhost.
5. Run **Flask user app** in its numbered order. The create request saves `user_id` automatically; there is no need to enter an ID manually.
6. Expand each request to see its saved live response example. These examples were captured from the real API during execution and embedded in the collection file.
7. For direct browser checks, open `http://127.0.0.1:5000/api/users` and then `/api/users/1` for the included demonstration record. If using a different database, use an ID returned by the list.

The update request changes John Doe to John Doe Updated and changes the country to Lebanon. A follow-up GET verifies those values. DELETE is followed by a GET that must return 404 and a list check that confirms the deleted ID is absent. The environment export intentionally leaves `user_id` blank because each run creates a fresh record.

## Repeat automated verification

```bash
python -m pytest -v
```

With Node.js and npm installed, run the same Postman collection through Newman:

```bash
npx --yes newman@6.2.2 run "postman/Flask user app.postman_collection.json" \
  -e "postman/Flask local.postman_environment.json"
```

The captured run output is in `newman-results.txt`, with a full machine-readable report in `newman-results.json`. The API response examples are also recorded in `live-responses.json`. `pytest-results.txt` contains the Python test results.

## Git and GitHub

The repository is published at [anthonyfeg/Lab5_AnthonyFeghali](https://github.com/anthonyfeg/Lab5_AnthonyFeghali). Both `main` and `feature/rest-api` are available remotely. The local repository is also included as the hidden `.git` directory in the submission ZIP. Inspect the history and configured remote with:

```bash
git log --graph --all --oneline --decorate
git status
git remote -v
```

To fetch the published branches on another computer:

```bash
git clone https://github.com/anthonyfeg/Lab5_AnthonyFeghali.git
cd Lab5_AnthonyFeghali
git fetch --all
git branch -a
```

The Git history shows the database work, REST feature branch, merge into `main`, verified Postman artifacts, and actual workspace screenshots. Database contents and virtual environments are excluded from Git. The ZIP includes the demonstration database separately.

## Proof files

Open `evidence/index.html` locally to browse the supporting reports. The PNG screenshots are in `proof-screenshots`:

- `01` through `08`: actual recorded CRUD requests and responses, including update and deletion verification.
- `09` and `09b`: collection requests, saved examples and environment variables.
- `10`: Newman execution summary showing 27 passing assertions.
- `11`: nine passing Python tests.
- `12`: actual SQLite schema and local branch/merge history before the final evidence commit.

The raw results and screenshots were collected on October 5, 2026. Request examples use fictional sample data. The postman-workspace subfolder documents the completed workspace import and saved examples. GitHub publishing is complete.

## References

- Assigned handout: Lab5-Postman and APIs.docx.
- [Postman quick start](https://learning.postman.com/docs/getting-started/quick-start/).
- [Send requests in Postman](https://learning.postman.com/docs/use/send-requests/requests/).
- [Install and run Newman](https://learning.postman.com/docs/reference/newman-cli/installing-running-newman/).
