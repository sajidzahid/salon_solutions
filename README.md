# salon_solutions
Final Project

## Run locally

```bash
streamlit run app.py
```

## Deploy on Railway

1. Push this repo to GitHub.
2. Create a new Railway project from the GitHub repo.
3. Railway will detect the `Dockerfile` automatically.
4. Add the database variable:

   ```bash
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.sgzvzplsmmeevctvpnpu.supabase.co:5432/postgres
   ```

5. The app adds `sslmode=require` automatically if it is missing.
6. Make sure the Supabase PostgreSQL database is reachable from Railway.

## Supabase setup

1. Create a Supabase project.
2. Open the SQL editor and run `supabase_schema.sql`.
3. Copy the Supabase PostgreSQL connection string into `DATABASE_URL`.
4. Use SSL mode `require`.

Supabase is PostgreSQL, so the app now uses `psycopg2` instead of the MySQL connector.
