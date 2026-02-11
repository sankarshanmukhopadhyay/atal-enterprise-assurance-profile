# Sample Forensic Bundle — Verification Walkthrough (Example)

## Steps
1. Confirm manifest enumerates all artifacts.
2. Compute SHA-256 of each artifact and compare to the manifest.
3. Confirm the chain head matches the expected chain head recorded elsewhere.
4. Validate signature on the manifest if used.
5. Modify one file and confirm verification fails.

## Output
A short verification report (pass/fail, mismatches, environment).
