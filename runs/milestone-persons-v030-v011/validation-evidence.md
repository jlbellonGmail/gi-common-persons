# Validation evidence

- PyPI index lookup for both packages returns no matching distribution.
- GitHub Release wheels are reproducible: Core `v0.3.0`, SHA256
  `41830d62b1b3e40b12c657cc5cc3147ca598411a495265cf52aa962503753b47`; Tenants
  `v0.1.1`, SHA256 `0d43d24d376b6cf56ef7214da2fa848b0543bc6a9c92d5dbb794f61918c0bda7`.
- A clean venv installed the three wheels: Core `0.3.0`, Tenants `0.1.1`,
  Persons `0.1.0`; Core public contracts imported successfully.
- Published Tenants wheel reports distribution `0.1.1` but module `0.1.0`;
  Tenants PR #11 corrects the source without changing the existing tag.
- Persons tests: `24 passed, 1 skipped`; Core integration: `4 passed`.
- No real Supabase migration executed: `PERSONS_TEST_DATABASE_URL` absent.
