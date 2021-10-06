import calendar
import datetime

days=["MON","TUE","WED","THU","FRI","SAT","SUN"]
days_month=[31,28,31,30,31,30,31,31,30,31,30,31]

def date_properties(date):
    properties=['EVERYDAY']
    
    in_date=datetime.datetime.strptime(date, "%Y-%m-%d")
    property="DAY" + str(in_date.day)
    properties.append(property)
    
    property="MONTH" + str(in_date.month)
    properties.append(property)
    
    property=days[in_date.weekday()]
    properties.append(property)

    if in_date.weekday() < 5:
        property="WEEKDAY"
    else:
        property="WEEKEND"
    properties.append(property)

    if in_date.day == 1:
        properties.append("FIRST")

    if in_date.day < 8:
        property="FIRST" + days[in_date.weekday()]
        properties.append(property)
        
    no_days=days_month[in_date.month-1]
    
    if calendar.isleap(in_date.year) and in_date.month==2:
        no_days=29
    if in_date.day == no_days:
        properties.append("LAST")
        
    if  in_date.day > no_days - 7 :
        property="LAST" + days[in_date.weekday()]
        properties.append(property)
        
    return properties