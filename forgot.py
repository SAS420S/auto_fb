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
]

filename =input("Enter file name: ")
with open(filename, "r", encoding="utf-8") as file:
    numbers = [line.strip() for line in file]

apk = "com.facebook.lite"

def clear_data(device):
    subprocess.run(f"adb -s {device} shell pm clear {apk}", shell=True)

def close_app(device):
    subprocess.run(f"adb -s {device} shell am force-stop {apk}", shell=True)

def device_work(device, as_num):
    d = u2.connect(device)
    for num in as_num:
        try:
            clear_data(device)
            time.sleep(2)
            d.app_start(apk)
            time.sleep(8)
            d(text="Forgot Password?").click()
            time.sleep(3)
            d(className="android.widget.EditText").set_text(num)
            time.sleep(1)
            d(text="Continue").click()
            time.sleep(5)
            close_app(device)
            time.sleep(2)
        
        except Exception as e:
            print(f"Error on {device}: {e}")
            close_app(device)
            time.sleep(2)

def split_number(devices, numbers):
    result = [[] for _ in devices]
    for i, num in enumerate(numbers):
        result[i % len(devices)].append(num)
    return result

dis_num = split_number(devices, numbers)
threads = []
for device_id, nums in zip(devices, dis_num):
    t = threading.Thread(target=device_work, args=(device_id, nums))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print("Done")
