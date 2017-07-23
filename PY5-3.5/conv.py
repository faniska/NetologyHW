import osa


def convert_length(value, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    result = client.service.ChangeLengthUnit(
        LengthValue=value,
        fromLengthUnit=from_unit,
        toLengthUnit=to_unit
    )

    return result


def convert_temp(value, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    result = client.service.ConvertTemp(
        Temperature=value,
        FromUnit=from_unit,
        ToUnit=to_unit
    )

    return result


def convert_currency(value, from_unit, to_unit):
    client = osa.client.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    result = client.service.ConvertToNum(
        amount=value,
        fromCurrency=from_unit,
        toCurrency=to_unit,
        rounding=True
    )
    return result


def get_avg_temp(filename):
    count = 0
    total = 0
    with open(filename) as f:
        for line in f:
            temp_in_f, temp_unit = line.strip().split()
            if temp_unit == 'F':
                count += 1
                temp_in_c = convert_temp(temp_in_f, 'degreeFahrenheit', 'degreeCelsius')
                total += temp_in_c
    return total / count if count > 0 else False


def get_flying_cost_in_rub(filename):
    total_cost = 0
    with open(filename) as f:
        for line in f:
            direction, cost, currency = line.strip().split()
            total_cost += float(cost) if currency == 'RUB' else convert_currency(cost, currency, 'RUB')
    return total_cost


def get_total_distance_in_km(filename):
    total_distance = 0
    with open(filename) as f:
        for line in f:
            direction, value, unit = line.strip().split()
            if unit == 'mi':
                distance_in_km = convert_length(float(value.replace(',', '')), 'Miles', 'Kilometers')
                total_distance += distance_in_km
    return total_distance


print("Средняя температура в Цельсиях")
print(get_avg_temp('input/temps.txt'))

print("Стоимость перелета в рублях")
print(round(get_flying_cost_in_rub('input/currencies.txt')))

print("Суммарная дистанция перелетов в км")
print(round(get_total_distance_in_km('input/travel.txt'), 2))
