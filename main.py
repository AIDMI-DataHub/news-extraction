import subprocess

def main():
    subprocess.run(["python", "utils.py"])  # This only needs to be run once initially
    subprocess.run(["python", "monsoon.py"])

if __name__ == "__main__":
    main()