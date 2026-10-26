# A1: inject one false claim into a local QĐ1416 copy

This controlled fixture targets Q-VKU07. The reviewed clean chunk says the
rounding precision is one decimal place. The fixture adds a false claim of two
decimal places to a separate in-memory corpus. Its metadata marks it as
poison/test data; the false claim is only supplied to this local experiment.
It does not modify the clean JSONL corpus or source PDF.

Run the clean and poisoned retrieval-only conditions first with the same
question and top-k. If the poison enters top-k, the generation condition can
then be run separately. Results are appended to
`experiments/data/real_vku/results/a1_results.csv` and remain separate from
the clean QA baseline.

The runner also has a prototype D2 option. It compares claims against the
curated trusted claim in `claim_registry.json`, flags conflicting untrusted
records, and measures false positives per clean chunk. This pilot rule only
covers the registered rounding fact; it is not a general-purpose detector.

The fixture must only be used for local research and must not be published as
an official VKU rule.
