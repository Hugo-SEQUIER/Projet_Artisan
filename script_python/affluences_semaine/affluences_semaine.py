# %% IMPORT
import datetime

# %% Données / Constantes
donneeStruct = {
    "idRdv",
    "idClient",
    "idArtisan",
    "typePrestation",
    "prestation",
    "prix",
    "date",
}

_date = "2023-02-14 15:30:00"

FrenchDay = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
EngDay = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

frequenceSemaine = {
    'Lundi' : 0,
    'Mardi' : 0,
    'Mercredi' : 0,
    'Jeudi' : 0,
    'Vendredi' : 0,
    'Samedi' : 0,
    'Dimanche' : 0
}

frequenceHeure = {}
# %% Fonctions

def convertStringtoDateTime(data):
    getYearMonthDay = data.split('-')
    year = getYearMonthDay[0]
    month = getYearMonthDay[1]
    dayHourMinutes = getYearMonthDay[2].split(' ')
    day = dayHourMinutes[0]
    hourMinutes = dayHourMinutes[1].split(':')
    hour = hourMinutes[0]
    minutes = hourMinutes[1]
    return datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes))

def getDayOfWeekFromDateTime(date):
    return date.strftime("%A")

def getHourFromDatetime(date):
    return date.strftime("%H")

def convertEngDaytoFrDay(day):
    return [FrenchDay[idx] for idx in range(len(FrenchDay)) if EngDay[idx] == day][0]

def countAffluence(jour):
    frequenceSemaine[jour] += 1

def countAffluenceHour(hour):
    if hour in frequenceHeure :
        frequenceHeure[hour] += 1
    else : frequenceHeure[hour] = 1
    
def traitement(data) :
    dateF = convertStringtoDateTime(data)
    dayWeek = getDayOfWeekFromDateTime(dateF)
    hourDay = getHourFromDatetime(dateF)
    jourSemaine = convertEngDaytoFrDay(dayWeek)
    
    countAffluence(jourSemaine)
    countAffluenceHour(hourDay)

# %% Main

date0 = "2023-02-14 15:30:00"
date1 = "2023-02-15 15:10:00"
date2 = "2023-02-16 16:30:00"
date3 = "2023-02-17 17:30:00"
date4 = "2023-02-18 18:30:00"
date5 = "2023-02-19 14:30:00"
date6 = "2023-02-20 08:30:00"
date7 = "2023-02-21 11:30:00"
date8 = "2023-02-22 17:00:00"
date9 = "2023-02-08 18:00:00"
date10 = "2023-02-04 19:50:00"
date11 = "2023-02-24 20:30:00"

listeDate = [date0,date1,date2,date3,date4,date5,date6,date7,date8,date9,date10,date11]

for date in listeDate :
    traitement(date)

print(frequenceSemaine)
print(frequenceHeure)
