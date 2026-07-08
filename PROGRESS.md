# MagnumOpus — Progress & Roadmap

Cadence: **1 hour/day, 1 commit/day.** Weekly milestone. No exceptions.

---

## PHASE 0 — HARDENING (do this first, ~3 sessions)

Live defects. Each is one commit. You write the fix; the "why" is here so you understand it.

- [x] **Day 1 — Kill module-level side effects in `data/storage.py`.** ✅ verified 2026-07-08
      Removed `connect = get_connection()` and `print(get_dashboard_data(connect))` at module scope.
      Why: importing storage anywhere currently opens a DB connection and runs a query. Imports must be side-effect free. The connection is owned by `app.py`, not the module.

- [x] **Day 1 — Fix table name in `get_data` (`storage.py`).** ✅ verified 2026-07-08
      `JOIN sales_item` → `sale_item`. Every other query uses `sale_item`. This one throws the instant the ML pipeline calls it.

- [ ] **Day 2 — Fix `buy_product` in `app.py`.**
      `purchase_processing` returns a dict `{"status","s_id"}`. Use `sale["status"] == "success"` and `s_id=sale["s_id"]` (match `checkout`). Fix the trailing `redirect(url_for('show_receipt'))` that passes no `s_id`.

- [ ] **Day 2 — Fix `Product(...)` positional args.**
      In `sales_processing` and `db_get_receipt`, the `product_id` is landing in the `image_path` slot. Signature: `(name, price, quantity, category, image_path, p_id)`. Pass by keyword or fix order.

- [ ] **Day 3 — Fix worst-sellers comprehension in `get_dashboard_data`.**
      `[... for row in row]` shadows the outer variable. Rename the loop var. Verify best/worst/unsold all return correct shapes.

- [ ] **Day 3 — Smoke test.** Run the app, place a sale via storefront AND via cart checkout, load receipt, load dashboard. Confirm no crashes. Commit.

**Milestone P0:** platform runs clean end-to-end with the bot simulator feeding it.

---

## PHASE 1 — PREDICTIVE INVENTORY MODEL (from scratch)

Fix and finish `analysis/processor.py`. No sklearn. Pure NumPy/pandas math.

- [ ] Fix `train_linear_models`: store per product → `self.models[p_id] = {"m":..., "b":...}` (currently overwrites every loop).
- [ ] Implement `predict_stockout(product_id, future_hours)`: use the fitted line to project demand, compare against current stock, return hours-to-stockout.
- [ ] Add a loss function (MSE) and, later, gradient descent as an alternative to the closed-form OLS — this is the "optimization loops from first principles" the blueprint demands.
- [ ] Expose a `/predict` route or dashboard widget showing predicted stockouts.

**Milestone P1:** dashboard shows "Product X predicted to stock out in ~N hours."

---

## PHASE 2 — CUSTOM NLP CHATBOT BRAIN (from scratch)

No LLM APIs. Raw Python + NumPy. New module (proposed `nlp/`).

- [ ] `nlp/tokenizer.py` — normalize + split raw text into tokens.
- [ ] `nlp/vocab.py` — token↔index mapping (vocabulary).
- [ ] `nlp/vectorizer.py` — turn token indices into numeric vectors (BoW → later embeddings).
- [ ] `nlp/intent.py` — classify a vector into an intent (stock query, demand trend, price, etc.).
- [ ] `nlp/brain.py` — map intent → PostgreSQL query → natural-language answer.
- [ ] Flask `/chat` route + minimal UI in a template.

**Milestone P2:** ask "how much stock of X do we have?" in the UI and get a live DB-backed answer.

---

## PHASE 3 — AWS CLOUD DEPLOYMENT

- [ ] `Dockerfile` for the Flask app + gunicorn.
- [ ] Externalize DB creds (env vars, not hardcoded in `storage.py`).
- [ ] RDS Postgres, containerize, deploy (ECS/Fargate or EB).
- [ ] Modular so frontend / DB / AI engine scale independently.

**Milestone P3:** platform live on AWS.

---

## Bug log (found 2026-07-08)
1. storage.py module-level `connect` + `print(get_dashboard_data)` — side effects on import.
2. storage.py `get_data` — `sales_item` should be `sale_item`.
3. app.py `buy_product` — dict/ID contract mismatch + `show_receipt` missing `s_id`.
4. sales_processing / db_get_receipt — `Product` positional-arg mismatch (id → image_path).
5. get_dashboard_data — worst-sellers loop-variable shadowing.
