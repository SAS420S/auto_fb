# ================== IMPORTS ==================
import time, random
import os
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

init(autoreset=True)

# ================== GLOBALS ==================
stats = {
    "total": 0,
    "success": 0,
    "no_id": 0,
    "no_sms": 0,
    "error": 0
}
lock = Lock()
HEADLESS = False  # True = background, False = visible browser

log_count = 0  # global log counter

# ================== HELPERS ==================
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]

def log_event(msg, color=Fore.WHITE):
    """Thread-safe numbered log"""
    global log_count
    with lock:
        log_count += 1
        print(f"{color}[{log_count}] {msg}{Style.RESET_ALL}")

def show_stats():
    """Print current stats"""
    print(Fore.CYAN + "=" * 50)
    print(
        f"Total: {stats['total']} | "
        f"Success: {stats['success']} | "
        f"No ID: {stats['no_id']} | "
        f"No SMS: {stats['no_sms']} | "
        f"Error: {stats['error']}"
    )
    print(Fore.CYAN + "=" * 50 + "\n")

# ================== SELENIUM SETUP ==================
def setup_chrome():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    return driver

# ================== CORE PROCESS ==================
def process_number(any_number):
    driver = None
    try:
        driver = setup_chrome()
        driver.get("https://www.facebook.com/recover/initiate/")

        # Input number
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@placeholder='Email address or mobile number']")
            )
        )
        input_field.clear()
        input_field.send_keys(any_number)

        # Click search
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Search')]"))
        )
        search_button.click()
        time.sleep(3)
        log_event(f"{any_number} : Processing", Fore.YELLOW)

        page_text = driver.page_source

        # No account found
        if "No search results" in page_text:
            log_event(f"{any_number} : Invalid Account", Fore.RED)
            with lock:
                stats["no_id"] += 1

        # SMS / OTP available
        elif any(x in page_text for x in ["Send code via SMS", "We can send a login code to:", "Try another way"]):
            try:
                # Try another way if exists
                try:
                    try_another_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Try another way')]")
                    driver.execute_script("arguments[0].click();", try_another_btn)
                    time.sleep(1)
                    page_text = driver.page_source
                except:
                    pass

                # Select SMS option
                sms_option = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, "//label[contains(.,'Send code via SMS')]//input"
                    ))
                )
                if not sms_option.is_selected():
                    driver.execute_script("arguments[0].click();", sms_option)

                # Click Continue
                continue_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Continue')]"))
                )
                driver.execute_script("arguments[0].click();", continue_btn)
                time.sleep(3)
                page_text = driver.page_source

                if "Please check your phone for a text message" in page_text or "Your code is" in page_text:
                    with lock:
                        stats["success"] += 1
                    with open("success_sent.txt", "a", encoding="utf-8") as f:
                        f.write(any_number + "\n")
                    log_event(f"{any_number} : Success", Fore.GREEN)

            except Exception as e:
                log_event(f"{any_number} : SMS / Continue failed -> {e}", Fore.RED)
                with lock:
                    stats["error"] += 1

        # Already in OTP step
        elif "Enter security code" in page_text:
            with lock:
                stats["success"] += 1
            with open("success_sent.txt", "a", encoding="utf-8") as f:
                f.write(any_number + "\n")
            log_event(f"{any_number} : Already in OTP step", Fore.GREEN)

        # Unknown page
        else:
            log_event(f"{any_number} : Unknown page layout", Fore.RED)
            with lock:
                stats["error"] += 1

    except Exception as e:
        log_event(f"{any_number} : Exception -> {e}", Fore.RED)
        with lock:
            stats["error"] += 1

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

# ================== MAIN ==================
def main():
    numbers = load_data("numbers.txt")
    if not numbers:
        print(Fore.RED + "numbers.txt ফাঁকা বা নেই!")
        return

    stats["total"] = len(numbers)

    try:
        threads = int(input(Fore.WHITE + "Enter Threads (5-10): "))
        threads = max(1, min(threads, 10))
    except:
        threads = 3

    global HEADLESS
    choice = input("Run in background (headless)? (y/n): ").lower()
    HEADLESS = True if choice == "y" else False

    print(Fore.CYAN + "\nStarting...\n")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for num in numbers:
            executor.submit(process_number, num)

    time.sleep(2)
    show_stats()

    # Summary
    end_time = time.time()
    elapsed = end_time - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)

    print(Fore.CYAN + "=" * 50)
    print(Fore.GREEN + f"ALL DONE | Time Taken: {hours}h {minutes}m {seconds}s")
    print(Fore.CYAN + "=" * 50)
    input("Press Enter to exit...")

# ================== ENTRY ==================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal Error: {e}")
    input("\nPress Enter to exit...")
