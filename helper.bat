@echo on
cd /d "C:\Users\Artur\Desktop\MediaThings\adb\my-gym-people-counter"
".\gym_venv\Scripts\python.exe" script.py 
rclone sync --progress  "logs.csv" "GDUpload:GDUpload\gym_rat_counter" --config rclone.conf
timeout /t 10