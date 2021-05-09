# Auditor
Auditor is a command line tool for auditing
correctness of CODE VOTING elections.

## Feautres
Auditor implements set of checks to validate all files generated
for finished election:
* pre-election ↔ data_tally - validates if the 
  commitment data is the same for pre-election 
  (commitments for codes and answers) and for data_tally (basically the same as pre-election but with marked votes)
  
* data_tally ↔ data_opened - validate if commitments for opened columns were correct. data_opened has one column
for each table opened, and the commitment should match the column data

* data_opened ↔ bb - validate if all votes from bb (bulletin board) are correctly recorded (
  correspond to correct question, cast code and vote code) in data_opened
  
* data_opened ↔ tally_all - validate if tally_all (both dummy and real votes) is counted correctly by counting votes in data_opened

* data_opened ↔ tally_dummy - validate if tally_dummy (only dummy votes) is counted correctly

* data_opened ↔ tally_final - validate if tally_final (only real votes) is counted correctly


## Install
To manage packages we use tool Poetry. See how to install it [here](https://github.com/python-poetry/poetry#installation).

### Install dependencies
Install dependencies needed to run Auditor:
```bash
> poetry install
```

## Usage
There are four commands provided:
* `audit-elections` - run all checks apart from data_opened ↔ tally_dummy and data_opened ↔ tally_final
* `audit-tally-all` - run check data_opened ↔ tally_all
* `audit-tally-dummies` - run check data_opened ↔ tally_dummy 
* `audit-tally-final` - run check data_opened ↔ tally_final 

To run the command open poetry shell, go to directory `auditor/` and run CLI.

Example:
```bash
> poetry shell
> cd auditor
> python -m auditor --help

> python -m auditor audit-elections ../data/demo444/public/audit_data-opened.json \
${DATA_DIR}/demo444/public/audit_data-pre-election-0.json \
${DATA_DIR}/demo444/public/audit_data-tally.json \
${DATA_DIR}/demo444/public/bb.json \
${DATA_DIR}/demo444/public/tally_all.json
```