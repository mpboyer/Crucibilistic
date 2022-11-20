def date_generator() :
    dates = []
    for y in range(1994, 1995) :
        for m in range(1, 13):
            if m in [1,3,5,7,8,10,12] :
                for d in range(1,32):
                    date = str(m)+"/"+str(d)+"/"+str(y)
                    dates.append(date)
            elif m in [4,6,9,11] :
                for d in range(1,31):
                    date = str(m) + "/" + str(d) + "/" + str(y)
                    dates.append(date)
            else :
                if y%4 == 0 :
                    for d in range(1,30) :
                        date = str(m) + "/" + str(d) + "/" + str(y)
                        dates.append(date)
                else :
                    for d in range(1,29) :
                        date = str(m) + "/" + str(d) + "/" + str(y)
                        dates.append(date)

    return dates

def generator() :
    URLS = []
    dates = date_generator()
    for date in dates:
        url = "https://xwordinfo.com/Crossword?date=" + date
        URLS.append(url)

    return URLS




