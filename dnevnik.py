import requests
from bs4 import BeautifulSoup
import bot

def get_html(log, passw):       #Функция получения hmtl кода из url сайта
    s = requests.Session()      #Начало сессии, для сохранения cookies
    r = s.post('https://login.dnevnik.ru/login', data = {'login':log, 'password':passw})        #Отправляем POST запрос для авторизации
    #r = s.get('https://schools.dnevnik.ru/marks.aspx?school=14477&index=8&tab=week&year=2017&month=1&day=11')
    try:
        r = s.get('https://dnevnik.ru/user')
        soup = BeautifulSoup(r.text, 'html.parser')
        grade = soup.find('a', {'title':'Мой дневник'})     #Ищем <a> который содержит тайтл == Мой дневник, для перехода к оценкам
        grade_page = grade['href']
        r = s.get(grade_page)
    except:
        return False
    return(r.text)      #Возвращаем html код дневника
'''
Парсим html код дневника    
'''
def parse(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except:
        return False
    table = soup.find('div', {'id':'diarydays'})        #Таблица которая содержит все дни недели
    try:
        row = table.find_all('div', {'class':'cc'})       #Отдельно каждый день
    except AttributeError:
        return False
    lessons = []
    for x in row:       #Обрабатываем каждый день
        i = 0
        list = x.find_all('a', {'class':'strong'})      #Находим все <a> с классом стронг. В нем хранятся наши уроки
        list1 = []
        while i < 20:
            try:
                list1.append(list[i].text)      #Добавляем в другой список только названия предметов
                i += 1
            except IndexError:
                break
        lessons.append(list1)  
    return lessons

def main(dict, id):
    lp = dict[id]
    l = lp[0]
    p = lp[-1]
    list = parse(get_html(l, p))
    if list == False:
        return False
    i = 0
    while i <= 5:
        if i == 0:
            monday = list[i]
        elif i == 1:
            tuesday = list[i]
        elif i == 2:
            wednesday = list[i]
        elif i == 3:
            thursday = list[i]
        elif i == 4:
            friday = list[i]
        elif i == 5:
            saturday = list[i]
        i += 1
    bist = [monday, tuesday, wednesday, thursday, friday, saturday]
    return bist


if __name__ == "__main__":
    main()

