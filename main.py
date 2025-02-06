import subprocess

def main():
    subprocess.run(["python", "utils.py"]) 
    subprocess.run(["python", "monsoon.py"])
    subprocess.run(["python", "heatwave.py"])
    subprocess.run(["python", "disasters.py"])

if __name__ == "__main__":
    main()
