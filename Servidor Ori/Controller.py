import time
import os

def main():
    data = os.system("python MainServer.py")
    if data == 1:
        print("[ERROR] An error occured. Restarting in 3s")
        time.sleep(3)
        os.system("cls")
        main()
    elif data in [5,1280]:
        print("[INFO] Server has been shut down.")
        raw_input("")
    elif data in [11,2816]:
        for x in range(1, 11):
            print(f"[ERROR] An error occurred. Restarting in {10 - x}s")
            time.sleep(1)
        os.system("cls")
        main()
    else:
        print("[ERROR] Server down. Restarting in 5s")
        time.sleep(5)
        os.system("cls")
        main()

if __name__=="__main__":
    main()
