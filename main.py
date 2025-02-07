# main.py
import subprocess

def main():
    # 1. Create required folders
    subprocess.run(["python", "utils.py"]) 

    # 2. Run monsoon script
    subprocess.run(["python", "monsoon.py"])

    # 3. Run heatwave script
    subprocess.run(["python", "heatwave.py"])

    # 4. Run disasters script
    subprocess.run(["python", "disasters.py"])

if __name__ == "__main__":
    main()
