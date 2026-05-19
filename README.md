# AuraNapló

Modern, local-first migrén / migrénaura napló Flask stackkel. Alapból SQLite-tal fut egyetlen gépen, de `DATABASE_URL` megadásával PostgreSQL-re is kapcsolható. A cél a gyors, mobilbarát rögzítés és a hosszabb távú mintázatok áttekintése, diagnózis vagy túlzsúfolt dashboard nélkül.

## Funkciók

- Local auth felhasználónévvel és jelszóval
- Gyors "Új aura" rögzítés 15-20 másodperces használatra
- Részletes migrén / aura esemény szerkesztés
- 24 órás trigger kontextus: alvás, folyadék, koffein, étkezés, stressz, betegség, képernyőterhelés
- Regenerációs adatok
- Timeline, havi bontás, napszak szerinti bontás, trigger gyakoriságok
- Aura intenzitás grafikon és egyszerű naptár strip
- Red flag jellegű események finom kiemelése, alarmista megfogalmazás nélkül
- Mobil-first UI, floating action button, dark mode

## Stack

- Python Flask
- SQLite alapértelmezésként, opcionális PostgreSQL
- SQLAlchemy ORM
- Flask-Migrate
- Flask-Login
- Jinja2
- Bootstrap 5 + minimal custom CSS
- python-dotenv

## Telepítés

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
flask db upgrade
flask seed
flask run
```

Alap demo fiók seed után:

```text
demo / demo12345
```

Az app alapértelmezetten itt indul: `http://127.0.0.1:5000`.

Alhálózaton elérhető futtatás:

```powershell
flask run --host 0.0.0.0 --port 5000
```

Ezután másik eszközről a gép LAN IP címével éred el, például: `http://192.168.1.50:5000`.

## Környezeti változók

`.env`:

```text
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=change-me-locally
DATABASE_URL=postgresql+psycopg://migraine:migraine@localhost:5432/migraineaura
```

Ha a `DATABASE_URL` nincs beállítva, az app automatikusan az `instance/migraineaura.sqlite3` fájlt használja.

## Migrációk

A repo tartalmaz egy kezdeti Alembic migrációt:

```powershell
flask db upgrade
```

Új modellváltozás után:

```powershell
flask db migrate -m "describe change"
flask db upgrade
```

## PostgreSQL séma

A kézzel olvasható séma itt van: `db/schema.sql`.

## Projektstruktúra

```text
app/
  models/
  routes/
  services/
  static/
  templates/
config.py
migrations/
db/schema.sql
docker-compose.yml
run.py
```

## Megjegyzés

Az alkalmazás személyes napló és mintázatfelismerő segédlet. Nem állít fel diagnózist, nem ad orvosi döntést, és a szövegezése szándékosan nyugodt.
