---
description: Run pytest and report results for geothermal-engineering exercises.
tags: [testing, pytest, geotherm
 requires_tools: [terminal]
---

# Run Tests Skill

Load this skill when asked to verify exercise code.

## Steps

1. Identify the test file from exercise context.
2. Run: `python3 -m pytest <file> -v`
3. Report: pass count, fail count, fail reasons.
4. If asked to run all tests: `python3 -m pytest -v`
5. If asked to run one exercise folder: `python3 -m pytest <folder> -v`

## Quality Gate

- All tests must pass before code review.
- Failing tests must show expected vs actual values.
- Warn if any test lacks known-value checks or physical-bounds checks.

## Sinopsis Perintah

```text
python3 -m pytest -v
python3 -m pytest 01_explore_plan_code/ -v
python3 -m pytest 02_specific_context/ -v
python3 -m pytest 03_verify_your_work/ -v
```
