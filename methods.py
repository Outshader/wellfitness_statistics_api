import csv
from pathlib import Path

def check_headers(required):
    data_path = Path("data/logs.csv")

    with open(data_path, mode="r+", newline="", encoding="utf-8") as file:
        file_content = file.readlines()
        missing = True
        entry = True
        if file_content: 
            first_row = file_content[0]        
            entry = False
            for i in first_row:
                if not isinstance(i, str):
                    entry = True
                    break
                    
            missing = True if not set(required) == set(first_row) else False
        
        
        writer = csv.DictWriter(file, fieldnames=required)
        if missing and entry:
            writer.writeheader()
        elif missing and not entry:
            file_content.pop(0)
            required = ",".join(required)
            file_content.insert(0,required+"\n")
            file_content = "".join(file_content)
            
            file.seek(0)
            file.truncate(0)
            file.write(file_content)
            
def validate_env_vars(var_name: str) -> str:
    fixed_var = ""
    with open("data/vars.env", "r") as f:
        data = f.readlines()
        for i in data:
            if var_name in i :
                fixed_var = i.strip().split("=", 1)[-1]
                if len(fixed_var) > 1:
                    first_char, last_char = fixed_var[0], fixed_var[-1]
                    if first_char == last_char:
                        fixed_var = fixed_var.strip(f"{first_char}")
            
    return fixed_var