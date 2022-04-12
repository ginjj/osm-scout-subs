import pandas as pd
import re
import sys

def main():
    # Import CAF export data from CSV
    # Name the CSV 'CSV_Export.csv'
    caf_df = pd.read_csv('CSV_Export.csv', skiprows=9, skipfooter=5, engine='python')

    caf_df['Description'] = caf_df['Description'].str.upper()

    # Create series where the description starts 'FP ' and then slice after the three 'FP ' characters 
    description_series = caf_df.loc[caf_df['Description'].str.contains('^FP\s')]['Description'].str.slice(start=3)


    # Import Account Names
    # Name the CSV 'account-names.csv'
    acc_df = pd.read_csv('account-names.csv', index_col=0)
    acc_df.to_csv('account-names-backup.csv')
    print(acc_df)
    acc_df.drop_duplicates(keep='first', inplace=True)
    print(acc_df)
    acc_df['Account Name'] = acc_df['Account Name'].str.upper()



    acc_regex = '$|'.join(map(re.escape, acc_df['Account Name']))
    added_flag = False
    for description in description_series:
        if not re.search(acc_regex, description):
            account_name = get_account_name_from_user(description)
            if account_name:
                acc_df2 = pd.DataFrame([[account_name]], columns=['Account Name'])
                acc_df = pd.concat([acc_df, acc_df2], ignore_index=True)
                print('Added: ' + account_name)
                acc_regex = '$|'.join(map(re.escape, acc_df['Account Name']))
                added_flag = True
            elif added_flag:
                acc_df.drop(acc_df.tail(1).index,inplace=True) # drop last 1 row
                acc_df.to_csv('account-names-new.csv')
                sys.exit('removed last and aborted')
            else:
                sys.exit('aborted')


    acc_df.to_csv('account-names.csv')
    regex = r'^(.*?)\s*({})$'.format('|'.join(map(re.escape, acc_df['Account Name'])))
    # acc_regex = '$|'.join(map(re.escape, acc_df['Account Name'])) +'$'
    print(acc_regex)
    # caf_df[['Reference','Not Used']] = caf_df['Description'].str.split(acc_regex, expand=True)
    caf_df[['Reference',    'Name']] = caf_df['Description'].str.extract(regex, expand=True) # was: caf_df[['Reference',    'Name']] = caf_df['Description'].str.extract(regex, expand=True)
    caf_df.to_excel('CSV_Export-output.xlsx', sheet_name='CAF Data Split')
    # caf_df.to_csv('CSV_Export-output.csv')
    
    print(caf_df)

def get_account_name_from_user(description):
    print('Account unknown:')
    words = description.split()
    start = 0
    break_positions = []
    for word in words:
        position = description.find(word, start)
        if position + 1 > (len(description) - 18) and position <= 19:  # Account reference is max 18 characters long
            break_positions.append(position)
        start = position + len(word)
    print(description)
    previous_position = 0
    for i, break_position in enumerate(break_positions, start=1):
        print(' ' * (break_position - previous_position - 1) + str(i), end="")
        previous_position = break_position
    print()    
    selection = inputNumber('Please enter the number corresponding to the account name start. (Type 0 to undo the previous entry and abort).\n', len(break_positions))
    if selection == 0:
        return False
    else:
        index = selection-1
        account_name = description[break_positions[index]:] # slice string at break position selected
        return account_name


def inputNumber(message, max):
  while True:
    try:
       userInput = int(input(message))       
    except ValueError:
       print("Not an integer! Please try again.")
       continue
    except userInput > max or userInput < 0:
        print('That number is not available. Please try again')
    else:
       return userInput 
       break 


if __name__ == "__main__":
    main()