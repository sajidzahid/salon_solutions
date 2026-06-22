# salon_solutions
Final Project

## Run locally

```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set the main file path to `app.py`.
4. Add database secrets or environment variables for:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
   - `DB_PORT`
   - `DB_SSLMODE`
5. Make sure the Supabase PostgreSQL database is reachable from Streamlit Cloud.

## Supabase setup

1. Create a Supabase project.
2. Open the SQL editor and run `supabase_schema.sql`.
3. Copy the Supabase PostgreSQL connection details into the environment variables above.
4. Use SSL mode `require`.

Supabase is PostgreSQL, so the app now uses `psycopg2` instead of the MySQL connector.
