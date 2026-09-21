# GoRest API Test Framework

![CI](https://github.com/olguinc/gorest-api-test-framework/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
[![Allure Report](https://img.shields.io/badge/report-Allure-orange)](https://olguinc.github.io/gorest-api-test-framework/)

A Pytest + Requests API test automation framework built against
[GoRest](https://gorest.co.in/), a public REST API with real CRUD operations
(users, posts, comments, todos) behind bearer-token auth. It exists to
demonstrate senior-level API test design and a working CI/CD pipeline —
the two things a UI/E2E portfolio (Playwright, Cypress, Selenium) doesn't cover.

## Why this project exists

Most QA portfolios only show browser automation. This one shows the other half
of the job: testing a system with no UI at all — request/response contracts,
auth, data lifecycle management against a shared external dataset, and a
pipeline that runs the suite on every change plus a nightly health check
against the live API.

## Architecture

```
tests/  ─────────────▶  resource clients (UsersClient, PostsClient, ...)
                                  │
                                  ▼
                          BaseAPIClient (auth, retries, logging)
                                  │
                                  ▼
                          GoRest public API
```

Supporting layers:
- **factories/** — Faker-based payload builders (unique emails per run)
- **schemas/** — JSON Schema per resource, used for contract validation
- **utils/** — status/schema/response-time assertion helpers, request logging
  with credential redaction, and a cleanup registry that deletes every
  resource a test creates

## Tech stack

| Layer            | Tool                              |
|-------------------|-----------------------------------|
| Language           | Python 3.12                       |
| HTTP client         | requests                          |
| Test runner        | pytest                            |
| Test data           | Faker                             |
| Contract validation | jsonschema                        |
| Reporting            | Allure (allure-pytest)            |
| Linting              | ruff                               |
| CI/CD                | GitHub Actions                    |

## What's covered

- **CRUD** — create/read/update/delete for users, posts, comments, todos
- **Negative paths** — missing/invalid fields, duplicate email, invalid token
  (401), unknown resource id (404), invalid enum values
- **Contract validation** — JSON schema checks on single-resource and list
  responses
- **Response-time guardrail** — a basic non-functional check (`< 3s`); this is
  not a substitute for real load testing, which is what K6/JMeter are for
- **Relational/e2e flow** — create a user → post → comment → todo, and verify
  the relationships through the nested read endpoints, with full teardown
- **Data-driven tests** — `pytest.mark.parametrize` across invalid-payload
  variations

## Getting started

```bash
git clone https://github.com/olguinc/gorest-api-test-framework.git
cd gorest-api-test-framework
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set GOREST_TOKEN to your own token from
# https://gorest.co.in/consumer/login

pytest -m smoke
```

## Running tests

```bash
pytest -m smoke          # fast subset, one CI run per push/PR
pytest                    # full suite
pytest -m negative        # only negative/edge-case tests
pytest -m e2e             # only the relational chained flow
```

### Generating the Allure report locally

```bash
pytest --alluredir=reports/allure-results
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

(Requires the [Allure commandline](https://allurereport.org/docs/gettingstarted/) — Java-based, installed separately from `pip`.)

## CI/CD

- **`ci.yml`** — runs on every push/PR: lint (ruff) → smoke tests → Allure
  report build → uploaded as a build artifact. On pushes to `main` only, the
  report is also published to
  [GitHub Pages](https://olguinc.github.io/gorest-api-test-framework/),
  **replacing** whatever was there before — so that URL always shows the
  report from the latest successful run on `main`, never a stale one. Pull
  request runs still generate a report, but only as a downloadable artifact
  (Actions → the run → *Artifacts* section) — they don't touch the public
  URL, so in-progress work never overwrites the published report.
- **`nightly.yml`** — scheduled daily (+ manual trigger) run of the full suite
  against live GoRest, acting as a lightweight external-API health monitor
  independent of any code change in this repo.

`GOREST_TOKEN` is stored as a GitHub Actions repository secret and injected as
an environment variable; it is never printed in logs (redacted by
`utils/logger.py`).

## Project structure

```
gorest-api-test-framework/
├── .github/workflows/       # ci.yml, nightly.yml
├── src/gorest_client/        # BaseAPIClient + resource clients
├── config/                    # env/settings loading
├── schemas/                    # JSON Schema per resource
├── factories/                   # Faker-based payload builders
├── utils/                        # assertions, logging, cleanup registry
└── tests/                         # smoke / users / posts / comments / todos / e2e
```

## Design decisions

- **Raw `Response` objects, not wrapped models** — client methods return the
  actual `requests.Response`, so tests can assert on status code, headers, and
  body independently instead of only on an unwrapped payload.
- **Cleanup registry, not a shared fixture teardown** — GoRest's dataset is
  public and shared across everyone running these tests, including nightly CI
  runs; every fixture that creates a resource registers it, and teardown
  deletes everything in reverse (child-first) order.
- **Response-time assertions are a guardrail, not a performance test** — real
  load/perf testing belongs in K6 or JMeter; this just catches gross
  regressions in a functional suite.

## Roadmap

- Contract testing with Pact
- A companion Locust/K6 performance suite against the same API
- Dockerized test execution

## License

MIT — see [LICENSE](LICENSE).


## 👩🏻‍💻 Author

**Carolina Olguin** — Senior QA Engineer · [GitHub](https://github.com/olguinc) · [LinkedIn](https://www.linkedin.com/in/carolina-olg/) · [Portfolio](https://olguinc.github.io/)

> *"The best tests don't just find bugs — they document the expected behavior of the system."*