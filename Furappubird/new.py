employeeName = input('Enter employee name: ')
yrsService = input('Enter year-in service: ')
enterOffice = input('Enter office (choose here: IT,ACCT and HR): ')

# check what office

if enterOffice == 'IT' or enterOffice == 'it':
    pass
    #check what yr service
    if int(yrsService) >= 10:
        bonus = 10000
    else:
        bounce = 5000

if enterOffice == 'acct' or enterOffice == 'ACCT':
    pass
    if int(yrsService) >= 10:
        bonus = 12000
    else:
        bonus = 6000


if enterOffice == 'hr' or enterOffice == 'HR':
    pass
    if yrsService >= 10:
        bonus = 15000
    else:
        bonus = 7500


output = f'''
Name: {employeeName}
Years of Service: {yrsService}
Office: {enterOffice} 

Hi {employeeName}, your bonus is {bonus}.

'''

print(output)

 