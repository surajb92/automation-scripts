import random


capitals = {
    "Andhra Pradesh": "Amaravati",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Dispur",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Goa": "Panaji",
    "Gujarat": "Gandhinagar",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jammu & Kashmir": "Srinagar",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Orissa": "Bhubaneshwar",
    "Punjab": "Chandigarh",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata",
    "Andaman & Nicobar Islands": "Port Blair",
    "Dadra & Nagar Haveli": "Silvassa",
    "Daman & Diu": "Daman",
    "Lakshadweep": "Kavaratti",
    "Puducherry": "Puducherry",
    "Delhi": "New Delhi",
    "Chandigarh": "Chandigarh",
}

for quiznum in range(35):
    qfile = open(f"capitals_quiz_{quiznum + 1}", "w")
    afile = open(f"capitals_quiz_answers_{quiznum + 1}", "w")
    qfile.write("Name: \n\nDate: \n\nClass: \n\n")
    qfile.write(" " * 20 + f" State Capitals Quiz Form {quiznum + 1}\n\n")
    states = list(capitals.keys())
    random.shuffle(states)  # states list is random now
    anslist = list(capitals.values())
    for qno in range(36):
        correct = capitals[states[qno]]
        wrong = random.sample(anslist, 4)
        if correct in wrong:
            del wrong[wrong.index(correct)]
        else:
            del wrong[3]
        options = [correct] + wrong
        random.shuffle(options)
        qfile.write(f"{qno + 1}. What is the capital of {states[qno]}?\n")
        for i in range(4):
            qfile.write(f"    {'ABCD'[i]}. {options[i]}\n")
        qfile.write("\n")
        afile.write(f"{qno + 1}. {'ABCD'[options.index(correct)]}")
    qfile.close()
    afile.close()
