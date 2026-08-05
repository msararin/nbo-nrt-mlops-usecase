# Phase 5C — ADLS Landing and Read-Back Evidence

## Meaning

A governed 11-table composite NBO–NRT dataset package was landed in a dedicated ADLS Gen2 account as one composite package.

The package contains explicitly synthetic Telco decision-loop data and source-transformed methodology evidence. It does not contain production customer data. No model was executed, and Databricks Bronze ingestion has not started.

## Measurement

- Artifacts: 12
- CSV tables: 11
- Total CSV rows: 805
- Local-to-ADLS SHA-256 match: 12/12
- Authoritative manifest SHA-256: `2eb73e1f784c0540f07df88cda17c05c7aaf253e7d1db6ff49b1e9341a902f41`
- Manifest hash match: PASS
- ADLS read-back: PASS

## Trust Boundary

The proof includes:

- an Azure CLI object listing;
- downloads from ADLS;
- SHA-256 recomputation from downloaded ADLS bytes;
- local canonical byte comparison; and
- CSV row-count recomputation.

Publication copies were visually inspected for subscription IDs, tenant IDs, user emails, access keys, SAS tokens, credentials, private URLs, and unrelated personal information. None of those fields is present in the published captures, so no pixel-level redaction was required.

External Independent Checker status: `PASS_WITH_NON_BLOCKING_OBSERVATIONS`.

- Provider/model: OpenRouter / `openai/gpt-5.6-terra`
- Generation ID: `gen-1785865175-UVLHdP35R0sDQUXAtm09`
- Trust level: packet-only

The Checker reviewed the privacy-minimized diff and evidence packet. It did not directly observe the live repository, local files, Azure/ADLS execution, or rendered browser. This is not a claim of direct independent observation of those systems.

## Custody

Local canonical source:

`/Users/apple/Downloads/NBO_NRT_DATA_RESEARCH_2026-08-04/05_PHASE5B_LOCAL_COMPOSITE/generated`

ADLS destination:

`abfss://nbo-nrt-composite@rinnbonrt2026.dfs.core.windows.net/nbo-nrt-composite/`

Manifest:

`generation_manifest.json`

## Selected Evidence

- [ADLS Gen2 storage configuration](screenshots/01-adls-gen2-storage-created-redacted.png)
- [ADLS artifact inventory](screenshots/02-adls-cli-list-12-artifacts.png)
- [Hash and row-count read-back verification](screenshots/03-adls-hash-rowcount-final-pass.png)
