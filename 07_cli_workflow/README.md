# Exercise 7: Shell + Python QA

## Goal
Teach Hermes to inspect raw CSV datalogs before running analysis, using the shell terminal tool.

## Engineering Focus
Well separator CSV: NaN, out-of-range temperature, negative pressure, duplicate dates.

## Activity
1. Run the QA script: `python3 07_cli_workflow/shell_production_QA.py sample_separator.csv`
2. Deliberately corrupt the CSV (add negative pressure, duplicate row, missing date).
3. Re-run QA and verify it catches the issue.
4. Use Hermes `terminal()` to invoke the QA script and inspect output.

## Before Prompt (vague)
```
Check the CSV file.
```

## After Prompt (precise)
```
Run 07_cli_workflow/shell_production_QA.py on 01_explore_plan_code/sample_separator.csv using terminal().
If any FAIL lines appear, report:
- which row and column
- expected range
- suggested fix
Do not trust CSV data until QA passes.
```

## Checklist
- [ ] QA script invoked via terminal
- [ ] Corrupted CSV caught
- [ ] Clean CSV marked PASSED
