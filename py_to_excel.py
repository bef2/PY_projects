import pandas


def toExcel():
    myDataFrame = pandas.DataFrame({'Name': ['Manchester City', 'Real Madrid', 'Liverpool',
                                'FC Bayern München', 'FC Barcelona', 'Juventus'],
                    'League': ['English Premier League (1)', 'Spain Primera Division (1)',
                                'English Premier League (1)', 'German 1. Bundesliga (1)',
                                'Spain Primera Division (1)', 'Italian Serie A (1)'],
                    'TransferBudget': [176000000, 188500000, 90000000,
                                        100000000, 180500000, 105000000]})

    myDataFrame.to_excel('teams.xlsx')


def writerExcel():
    salaries1 = pandas.DataFrame({'Name': ['L. Messi', 'Cristiano Ronaldo', 'J. Oblak'],
                                        'Salary': [560000, 220000, 125000]})
    salaries2 = pandas.DataFrame({'Name': ['K. De Bruyne', 'Neymar Jr', 'R. Lewandowski'],
                                        'Salary': [370000, 270000, 240000]})
    salaries3 = pandas.DataFrame({'Name': ['Alisson', 'M. ter Stegen', 'M. Salah'],
                                        'Salary': [160000, 260000, 250000]})
    salary_sheets = {'Group1': salaries1, 'Group2': salaries2, 'Group3': salaries3}
    writer = pandas.ExcelWriter('salaries.xlsx', engine='xlsxwriter')

    salaries1.to_excel(writer)
    salaries1.to_excel(writer)
    salaries1.to_excel(writer)
    for sheet_name in salary_sheets.keys():
        salary_sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


if __name__ == "__main__":
    toExcel()