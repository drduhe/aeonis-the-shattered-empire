# Current sim baselines (M3)

**Updated:** 2026-07-03 · Regenerate tournament reports to `/tmp` or a dated file — stored snapshots are optional.

**Default stack:** M3 engine + Lever C expander brakes + S1 `seat_of_empire_vp: 1`.

---

## Configs (keep in repo)

| Config | Use |
| --- | --- |
| `bracket-m2-smoke.json` | Mixed 4p smoke (100 games) — primary balance bracket |
| `bracket-m2-4p.json` | Solo 4p ladder (200 games) |
| `bracket-6p-mixed.json` / `bracket-8p-mixed.json` | High-count mixed |
| `bracket-m2-ci.json` / `bracket-m3-ci.json` | CI gates (20 games) |
| `regression-plan{1,2}-*.json` | Plan 1/2 metric gates (CI) |

---

## Headlines (last run 2026-07-03)

### Mixed 4p (`bracket-m2-smoke.json`, 100 games)

Mean **6.2** rounds · economist **10.7%** · expander **23.3%** · max persona balanced **33.8%**

### Mixed 6p (`bracket-6p-mixed.json`, 200 games)

Mean **6.4** rounds · economist **3.6%** (H8 fail) · warmonger **27.2%**

### Mixed 8p (`bracket-8p-mixed.json`, 200 games)

Mean **6.2** rounds · economist **2.0%** (H8 fail) · max persona **22.6%**

### Solo 4p (`bracket-m2-4p.json`, 200 games)

~**25%** each persona (parity sanity)

---

## Hypothesis scoreboard (mixed 4p)

| ID | Status | Read |
| --- | --- | --- |
| H1 | killed | Seat+streak 6.5% of VP |
| H2 | killed | Avg margin 3.1 VP |
| H3 | killed | Winner objective share 79.5% |
| H7 | 4p inconclusive | Expander 23.3%; max 33.8% |
| H8 | 4p met, 6–8p not | 10.7% / 3.6% / 2.0% |
| H12 | killed | Economist 10.7% at 4p |

Full H1–H12 table lives in tournament `--report` output when you regenerate.

---

## Regenerate

```bash
cd sim
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-m2-smoke.json --report /tmp/baseline-4p.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-6p-mixed.json --report /tmp/baseline-6p.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-8p-mixed.json --report /tmp/baseline-8p.md --workers 4
py -3.11 -m aeonis_sim.runner.tournament --config configs/bracket-m2-4p.json --report /tmp/baseline-solo-4p.md --workers 4
```

After engine changes, update headlines in this file or `docs/reports/INDEX.md`.
