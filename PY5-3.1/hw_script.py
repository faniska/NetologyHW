# Тест прошел в 09.07.2017 12.02 по московскому времени

# Ответ на 10 вопрос

mass = range(1, 15)
res_list = [x**2 for x in mass if (x**2 % 3 == 0 and x**2 % 4 == 0)]
print(res_list)