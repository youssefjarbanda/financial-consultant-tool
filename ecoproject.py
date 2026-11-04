
import logging
import json

logging.basicConfig(level=logging.INFO, filename="log.log", filemode= "w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

logging.info('-'*70)


try:
    with open("input_sample.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    logging.error(f"Could not find \"input_sample.json\"")
    data = []
  

    with open("families_data", "w") as file:
        json.dump(data, file, indent=4)


accepted = []
rejected = []

for clients in data:
    try:
        family = clients.get("family", "unknown family")
        if not isinstance(family, (str)) or family == "":
            logging.info(f'family\'s name missing')
            rejected.append(clients)
            continue

        income = clients.get("income")
        if not isinstance(income, (int, float)):
            logging.info(f'revise the income section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if income < 0:
            logging.info(f'there is a mistake in the income section of: {clients["family"]}, rent is negative')
            rejected.append(clients)
            continue

        detailed_expenses = clients.get("expenses")
        if not isinstance(detailed_expenses, (dict)):
             logging.info(f'the expenses section is empty in: {clients["family"]}' ", ")
             rejected.append(clients)
             continue
        
        food = detailed_expenses.get("Food", 0) or detailed_expenses.get("Food", 0)
        rent = detailed_expenses.get("Rent", 0)
        entertainment = detailed_expenses.get("Entertainment", 0)
        transport = detailed_expenses.get("Transport", 0)
        other = detailed_expenses.get("Other", 0)


        if not isinstance(food, (int, float)):
            logging.info(f'revise the food\'s section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if food < 0:
            logging.info(f'there is a mistake in the food section of: {clients["family"]}, food is negative')
            rejected.append(clients)
            continue

        if not isinstance(rent, (int, float)):
            logging.info(f'revise the rent section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if rent < 0:
            logging.info(f'there is a mistake in the rent section of: {clients["family"]}, rent is negative')
            rejected.append(clients)
            continue

        if not isinstance(entertainment, (int, float)):
            logging.info(f'revise the entertainment section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if entertainment < 0:
            logging.info(f'there is a mistake in the entertainment section of: {clients["family"]}, entertainment is negative')
            rejected.append(clients)
            continue

        if not isinstance(transport, (int, float)):
            logging.info(f'revise the transport section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if transport < 0:
            logging.info(f'there is a mistake in the transport section of: {clients["family"]}, transport is negative')
            rejected.append(clients)
            continue

        if not isinstance(other, (int, float)):
            logging.info(f'revise the other section of: {clients["family"]}')
            rejected.append(clients)
            continue
        if other < 0:
             logging.info(f'there is a mistake in the other section of: {clients["family"]}, other is negative')
             rejected.append(clients)
             continue            
        
        accepted.append(clients)

    except (ValueError,TypeError,KeyError):
        rejected.append(clients)
        logging.info(f'there is a problem in the data of: {clients["family"]}')
        continue

logging.info("-"*70)
logging.info(f"accepted len {len(accepted)}")
logging.info(f"rejected len {len(rejected)}")
logging.info("-"*70)

report_results = []

for acceptedfamilies in accepted:
    family_name = acceptedfamilies.get('family')
    total_income = acceptedfamilies.get('income')
    valid_expenses = acceptedfamilies.get('expenses', 0) #expenses as a nested dict
    total_expenses = sum(valid_expenses.values())
    valid_rent = valid_expenses.get('Rent', 0)
    valid_entertainment = valid_expenses.get('Entertainment', 0)
    valid_food = valid_expenses.get('Food', 0) or valid_expenses.get('food', 0)
    valid_transport = valid_expenses.get('Transport', 0)
    valid_other = total_expenses - (valid_transport + valid_food + valid_entertainment + valid_rent)
    

    if valid_rent > total_income*35/100:
        logging.info(f'{acceptedfamilies["family"]} are spending too much on rent')

    if valid_entertainment > total_income*35/100:
        logging.info(f'{acceptedfamilies["family"]} are spending too much on entertainment')

    if valid_food > total_income*35/100:
        logging.info(f'{acceptedfamilies["family"]} are FAT')

    if valid_transport > total_income*35/100:
        logging.info(f'{acceptedfamilies["family"]} are spending too much on transportation')

    if valid_other > total_income*35/100:
        logging.info(f'{acceptedfamilies["family"]} are spending too much on other stuff')

    try:
        saving_rate = (total_income - total_expenses) / total_income * 100
        logging.info(f'{acceptedfamilies["family"]} saving rate is {saving_rate}%')
    except ZeroDivisionError:
        logging.info(f'{acceptedfamilies["family"]} saving rate is Null')

    

    family_report = {
        "family": family_name,
        "month": acceptedfamilies.get("month", "Unknown"),
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings_rate": round(saving_rate, 2) if saving_rate is not None else None,
        "saving_rate_status": "deficit" if saving_rate is not None and saving_rate < 0 else "healthy",
        "categories": {
            "Rent": valid_rent,
            "Food": valid_food,
            "Entertainment": valid_entertainment,
            "Transport": valid_transport,
            "Other": valid_other
        }
    }
    
    # 3. Add each family report into our list
    report_results.append(family_report)

with open("report.json", "w") as report_file:
    json.dump(report_results, report_file,indent=4)