import calendar
import datetime

import PySimpleGUI as sg


sg.theme('LightBlue6')
today = datetime.date.today()

def create_layout(cal_date):
    weekday = ['SUN','MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']  
    cal = calendar.Calendar(firstweekday=6)
    days = cal.monthdatescalendar(cal_date.year, cal_date.month)
    layout = [[sg.Text(cal_date.year, font=(None, 13, 'bold'))],
              [sg.Push(), sg.Button('<<'), sg.Button('<'), sg.Text(cal_date.month, font=(None, 30)), sg.Button('>'), sg.Button('>>'), sg.Push()]]
    inner = []
    
    for week in weekday:
        inner.append(sg.Text(week, size=(12,3), text_color='white', background_color='pink', justification='center'))
    layout.append(inner.copy())

    def date_judgement(i, day):
        if day == today:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='white', background_color='gray')
        elif i == 0 and day.month == cal_date.month:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='red')
        elif i == 6 and day.month == cal_date.month:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='blue')
        elif day.month == cal_date.month:
            return sg.Text(day.day, size=(12,3), justification='right')
        elif i == 0:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='#ff9999')
        elif i == 6:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='#9999ff')
        else:
            return sg.Text(day.day, size=(12,3), justification='right', text_color='#cccccc')

    for row in days:
        inner = []
        for i, day in enumerate(row):
            sg_text = date_judgement(i, day)
            inner.append(sg_text)
        layout.append(inner.copy())
    return layout

def main():
    cal_date = today
    layout = create_layout(cal_date)
    window = sg.Window('Simple Calendar', layout)

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == '<':
            cal_date = datetime.date(cal_date.year, cal_date.month, 1) - datetime.timedelta(days=1)
        elif event == '>':
            cal_date = datetime.date(cal_date.year, cal_date.month, 28) + datetime.timedelta(days=4)
        elif event == '<<':
            cal_date = datetime.date(cal_date.year - 1, cal_date.month, 1)
        elif event == '>>':
            cal_date = datetime.date(cal_date.year + 1, cal_date.month, 1)
        window.close()
        window = sg.Window('Simple Calendar', create_layout(cal_date))
    window.close()

if __name__ == '__main__':
    main()

    


