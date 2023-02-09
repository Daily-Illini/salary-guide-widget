import csv
import json

# Python file containing the functions used to process salary guide data

# Not using EMPL_CLASSES since this it is incomplete
EMPL_CLASSES = {
    "AA":"Academic 9/12 month Benefit Eligible (9 months service paid over 12 month period)",
    "AB":"Academic 9/12 month Non-Benefit Eligible (9 months service paid over 12 month period)",
    "AG":"Academic 10/12 month Benefit Eligible (10 months service paid over 12 month period)",
    "AH":"Academic 10/12 month Non-Benefit Eligible (10 months service paid over 12 month period)",
    "AL":"Academic 12 month Benefit Eligible (12 months service paid over 12 month period)",
    "AM":"Academic 12 month Non-Benefit Eligible (12 months service paid over 12 month period)",
    "BA":"Academic Professional 12 month Benefit Eligible (12 months service paid over 12 month period)",
    "BB":"Academic Professional 12 month Non-Benefit Eligible (12 months service paid over 12 month period)",
    "BC":"Academic Professional 9/12 month Benefit Eligible (9 months service paid over 12 month period)",
    "BD":"Academic Professional 9/12 month Non-Benefit Eligible (9 months service paid over 12 month period)",
    "BG":"Academic Professional 10/12 month Benefit Eligible (10 months service paid over 12 month period)",
    "BH":"Academic Professional 10/12 month Non-Benefit Eligible (10 months service paid over 12 month period)",
    "PA":"Postdoctoral Research Associate Benefit Eligible (Service paid over 12 month period)",
    "PB":"Postdoctoral Research Associate Non-Benefit Eligible (Service paid over 12 month period)"
}

# Dict for tenure codes
TENURE_CODES = {
    "A":"Indefinite Tenure",
    "M":"Multi-Year Contract Agreement",
    "N":"Initial/Partial Term",
    "P":"Probationary Term",
    "Q":"Specified Term Appointment",
    "T":"Terminal Contract",
    "W":"Special Agreement to Accept Academic Appointment and Reappointment for Definite Term"
}


# We use a tuple of (employee_name_string, employee_total_salary_float) as a makeshift primary key
""" 
all_empls_dict has structure: 
{
    (employee1_name, employee1_total_salary_as_float_2f) : {
        "name": employee1_name,
        "salary": employee1_total_salary_as_float_2f,
        "positions": [
            {
                "title": position_title,
                "department": position_dept,
                "college": position_college,
                "positionSalary": position_salary_as_float_2f,
                "tenure": tenure_status (see 'TENURE_CODES'),
                "payType": paycode
            }, ... ]
        ]
    },
    (employee2_name, employee2_salary_as_float_2f) : { See above }...
}
"""
all_empls_dict = {}


# processing graybook salaries
def parse_gb_(gb_csv_path: str):
    row_idx = 1 # setting start index at 1 for easier debugging since Excel row labels start at 1
    with open(gb_csv_path, encoding="utf-8") as data_raw:
        data_reader = csv.DictReader(data_raw)
        print("\nCSV opened successfully...")
        for row in data_reader:
            # Checks if tuple key exists in all_empls_dict
            # If so, we add a dict containing info on the new position to the "positions" list for the corresponding employee in all_empls_dict
            if (row["Employee Name"], "${:,.2f}".format(float(row["Empl Total\nProposed\nSalary"]))) in list(all_empls_dict.keys()):
                
                # Creating the dict with new position info
                curr_pos_dict = {
                    "title":row["Job Title"],
                    "department":row["Dept Name"],
                    "college":row["College Name"],
                    "positionSalary":float(row["Proposed\nSalary"]),
                    "tenure":TENURE_CODES.get(row["Tenure"], ""),
                    "payType":row["Empl\nClass"]
                }
                # Adding the new position dict to all_empls_dict
                curr_empl_dict = all_empls_dict[(row["Employee Name"], "${:,.2f}".format(float(row["Empl Total\nProposed\nSalary"])))]
                curr_empl_dict["positions"].append(curr_pos_dict)
            
            # If the tuple key does not exist, we create a new entry in all_empls_dict using the tuple key
            else:
                curr_empl_dict = {
                    "name":row["Employee Name"],
                    "salary":float(row["Empl Total\nProposed\nSalary"]),
                    "positions":[{
                        # Adding position dict in "positions" for the position info
                        "title":row["Job Title"],
                        "department":row["Dept Name"],
                        "college":row["College Name"],
                        "positionSalary":float(row["Proposed\nSalary"]),
                        "tenure":TENURE_CODES.get(row["Tenure"], ""),
                        "payType":row["Empl\nClass"]
                }]
                }
                # Adding the new employee dict to all_empls_dict
                all_empls_dict.update({(row["Employee Name"], "${:,.2f}".format(float(row["Empl Total\nProposed\nSalary"]))):curr_empl_dict})
            row_idx += 1
        data_raw.close()
        print("\n" + str(row_idx - 2) + " rows in CSV")


# processing non-graybook salaries
def parse_non_gb_(non_gb_csv_path: str):
    row_idx = 1
    with open(non_gb_csv_path, encoding="utf-8") as data_raw:
        data_reader = csv.DictReader(data_raw)
        print("\nCSV opened successfully...")
        for row in data_reader:
            # The non-graybook data has different formatting for the salary numbers, which this code handles
            tot_sal = row["Empl Total\nSalary"]
            tot_sal = tot_sal.replace("$","")
            tot_sal = tot_sal.replace(",", "")
            pos_sal = row["Salary"]
            pos_sal = pos_sal.replace("$", "")
            pos_sal = pos_sal.replace(",","")
            
            # Also, there's slightly different column labels for non-graybook data, so there are minor differences when it comes to the keys used for salaries and position
            
            # Checks if tuple key exists in all_empls_dict
            # If so, we add a dict containing info on the new position to the "positions" list for the corresponding employee in all_empls_dict
            if (row["Employee Name"], row["Empl Total\nSalary"]) in list(all_empls_dict.keys()):
                # Basically does the same thing as we did for the graybook salaries
                curr_pos_dict = {
                    "title":row["Job Title"],
                    "department":row["Dept Name"],
                    "college":row["College Name"],
                    "positionSalary":float(pos_sal),
                    "tenure":"",
                    "payType":row["Empl\nClass"]
                }
                curr_empl_dict = all_empls_dict[(row["Employee Name"], row["Empl Total\nSalary"])]
                curr_empl_dict["positions"].append(curr_pos_dict)
            
            # If the tuple key does not exist, we create a new entry in all_empls_dict using the tuple key
            else:
                # Basically does the same thing as we did for the graybook salaries
                curr_empl_dict = {
                    "name":row["Employee Name"],
                    "salary":float(tot_sal),
                    "positions":[
                        {
                            "title":row["Job Title"],
                            "department":row["Dept Name"],
                            "college":row["College Name"],
                            "positionSalary":float(pos_sal),
                            "tenure":"",
                            "payType":row["Empl\nClass"]
                        }
                    ]
                }
                all_empls_dict.update({(row["Employee Name"], row["Empl Total\nSalary"]):curr_empl_dict})
            row_idx += 1
        data_raw.close()
        print("\n" + str(row_idx - 2) + " rows in CSV")

# Method that basically puts it all together and dumps the result into a JSON file at the provided output path
def process_salary_data(campus_gb_path: str, campus_ngb_path: str, output_path: str):
    parse_gb_(campus_gb_path)
    parse_non_gb_(campus_ngb_path)
    with open(output_path, "w+", encoding='utf-8') as out:
        # Takes the values of all_empls_dict as a list, and dumps it into JSON
        json.dump(list(all_empls_dict.values()), out, indent='\t')