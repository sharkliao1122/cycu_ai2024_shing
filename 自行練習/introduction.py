
def person(age, major, place):
    print("I am ", age, " years old")
    print('MY major is ', major)
    print("I am from", place)


import re

def get_valid_major():
    while True:
        major = input("What is your major? ").strip()
        if re.match(r'^[a-zA-Z\u4e00-\u9fff]+$', major):
            if re.match(r'^[a-zA-Z]+$', major):
                major = major.capitalize()
            return major
        else:
            print("Please enter a valid major (only English or Chinese characters).")

def get_valid_place():
    while True:
        place = input("Where are you from? ").strip()
        if re.match(r'^[a-zA-Z\u4e00-\u9fff]+$', place):
            if re.match(r'^[a-zA-Z]+$', place):
                place = place.capitalize()
            return place
        else:
            print("Please enter a valid place (only English or Chinese characters).")
# 獲取有效的年齡、專業和來自地點
age = get_valid_age()
major = get_valid_major()
place = get_valid_place()

# 呼叫 person 函數並傳遞獲取的參數
person(age, major, place)