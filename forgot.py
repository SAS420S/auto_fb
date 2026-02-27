import uiautomator2 as u2
import time
import threading, subprocess

devices = [
    "emulator-5554",
    "emulator-5556",
    "emulator-5558",
    "emulator-5560",
    "emulator-5562",
    "emulator-5564",
    "emulator-5566",
    "emulator-5568",
    "emulator-5570",
    "emulator-5572",
]

run_count = int(input(" How many Device: "))
devices = devices[:run_count]

filename =input("Enter file name: ")
try:
    with open(filename, "r", encoding="utf-8") as file:
        numbers = [line.strip() for line in file]
except FileNotFoundError:
    print("File not found. Exiting.")
    exit()

apk = "com.facebook.lite"

def clear_data(device):
    subprocess.run(f"adb -s {device} shell pm clear {apk}", shell=True)

def close_app(device):
    subprocess.run(f"adb -s {device} shell am force-stop {apk}", shell=True)

def device_work(device, as_num):
    try:
        d = u2.connect(device)
    except Exception as e:
        print(f"Cannot connect to {device}: {e}")
        return
    for num in as_num:
        try:
            clear_data(device)
            time.sleep(2)
            d.app_start(apk)
            d(text="Forgot password?").wait(timeout=10)
            d(text="Forgot password?").click()
            d(className="android.widget.EditText").wait(timeout=10)
            d(className="android.widget.EditText").set_text(num)
            time.sleep(1)
            d(text="Continue").click()
            time.sleep(5)
            close_app(device)
            time.sleep(2)
        
        except Exception as e:
            print(f"Error on {device} for number {num}: {e}")
            close_app(device)
            time.sleep(2)

def split_number(devices, numbers):
    result = [[] for _ in devices]
    for i, num in enumerate(numbers):
        result[i % len(devices)].append(num)
    return result

def safe_device_work(device_id, nums):
    try:
        device_work(device_id, nums)
    except Exception as e:
        print(f"Thread error on {device_id}: {e}")

dis_num = split_number(devices, numbers)
threads = []
for device_id, nums in zip(devices, dis_num):
    t = threading.Thread(target=safe_device_work, args=(device_id, nums))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print("Done")
