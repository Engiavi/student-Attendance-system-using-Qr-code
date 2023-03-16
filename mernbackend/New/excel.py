
# import os
# import pandas as pd
# import sys

# a = sys.argv[1]

# # print("The value of a is: ", a)



# dir_path = r"./excel"


# person_name = a


# all_person_info = []


# for filename in os.listdir(dir_path):
   
#     if filename.endswith(".xlsx"):
       
#         df = pd.read_excel(os.path.join(dir_path, filename))

        
#         if person_name in df["firstname"].tolist():
           
#             person_info = df[df["firstname"] == person_name].to_dict()

           
           
#             def simplify_dict(d):
#                 result = {}
#                 for key, value in d.items():
#                     result[key] = value[0]
#                 return result
           
#             all_person_info.append(simplify_dict(person_info))


# person_info_df = pd.DataFrame(all_person_info, columns=['firstname', 'lastname', 'emailid', 'time'])

# writer = pd.ExcelWriter("person_info.xlsx")
# person_info_df.to_excel(writer, index=False)
# writer.save()
import os
import pandas as pd
import sys

a = sys.argv[1]
person_name = a

print("The value of a is: ", person_name)

dir_path = r"./excel"

all_person_info = []

for filename in os.listdir(dir_path):
    if filename.endswith(".xlsx"):
        df = pd.read_excel(os.path.join(dir_path, filename))
        if person_name in df["firstname"].tolist():
            person_info = df[df["firstname"] == person_name].to_dict()
            def simplify_dict(d):
                result = {}
                for key, value in d.items():
                    result[key] = value[0]
                return result
            all_person_info.append(simplify_dict(person_info))

person_info_df = pd.DataFrame(all_person_info, columns=['firstname', 'lastname', 'emailid', 'time'])
writer = pd.ExcelWriter(person_name+".xlsx")
person_info_df.to_excel(writer, index=False)
writer.save()

