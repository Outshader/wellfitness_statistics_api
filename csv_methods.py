import csv

def check_headers(required):
    with open("logs.csv", mode="r+", newline="", encoding="utf-8") as file:
        file_content = file.readlines()
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
            required = ", ".join(required)
            file_content.insert(0,required+"\n")
            file_content = "".join(file_content)
            
            file.seek(0)
            file.truncate(0)
            file.write(file_content)
            
            

    