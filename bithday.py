from datetime import datetime, date, timedelta

def string_to_date(date_string):
    return datetime.strptime(date_string, "%d.%m.%Y").date()

def date_to_string(date):
    return date.strftime("%d.%m.%Y")

def prepare_user_list(user_data):
    prepared_list = []
    for user in user_data:
        prepared_list.append({"name": user["name"], "birthday": string_to_date(user["birthday"])})
    return prepared_list
def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


def get_upcoming_birthdays(users, days=7):
    upcoming_birthdays = []
    today = date.today()
    _users = prepare_user_list(users)
    for user in _users:
        birthday_this_year = user["birthday"].replace(year=today.year)

        if (birthday_this_year < today):
            birthday_next_year = user["birthday"].replace(year=today.year + 1)
            if 0 <= (birthday_next_year - today).days <= days:
                birthday_this_year = birthday_next_year
            
        birthday_this_year = adjust_for_weekend(birthday_this_year)
        if 0 <= (birthday_this_year - today).days <= days:
            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": user["name"], "congratulation_date": congratulation_date_str})
    return upcoming_birthdays