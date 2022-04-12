# osm-scout-subs

Script to take CAF bank CSV statement export and split any new account names found from transaction references (with user input).

Input file - in the format downloaded from CAF bank `CSV_Export.csv`.

The list of know account names are saved to a CSV file `account-names.csv`.

The split (account name / payment reference) output is saved to a an Excel file `CSV_Export-output.xlsx`.
