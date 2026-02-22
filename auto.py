import uiautomator2 as u2
import time
 
device = u2.connect("192.168.0.103:5555")

print("ডিভাইস কানেক্ট করা হয়েছে!")


package_name = "com.facebook.katana"
device.app_start(package_name)
print("অ্যাপ ওপেন করা হচ্ছে...")
time.sleep(5)


try:
    create_account_btn = device(text="Create new account")
    create_account_btn.click()
    print("Create new account বাটনে ক্লিক করা হয়েছে")
    time.sleep(2)
except:
    print("Create new account বাটন খুঁজে পাওয়া যায়নি")

try:
    get_started_btn = device(text="Get started")
    if get_started_btn.exists:
        get_started_btn.click()
        print("Get started বাটনে ক্লিক করা হয়েছে")
        time.sleep(2)
except:
    print("Get started বাটন খুঁজে পাওয়া যায়নি")

try:
    first_name_field = device(resourceId="com.facebook.katana:id/first_name")
    if first_name_field.exists:
        first_name_field.click()
        first_name_field.clear_text()
        first_name_field.set_text("John")
        print("First name ইনপুট করা হয়েছে")
    else:
        first_name_field = device(className="android.widget.EditText", instance=0)
        first_name_field.set_text("John")
    
    last_name_field = device(resourceId="com.facebook.katana:id/last_name")
    if last_name_field.exists:
        last_name_field.click()
        last_name_field.clear_text()
        last_name_field.set_text("Doe")
        print("Last name ইনপুট করা হয়েছে")
    else:
        last_name_field = device(className="android.widget.EditText", instance=1)
        last_name_field.set_text("Doe")
    
    time.sleep(1)
    
    next_btn = device(text="Next")
    if next_btn.exists:
        next_btn.click()
        print("Next বাটনে ক্লিক করা হয়েছে (Name section)")
        time.sleep(2)
except:
    print("নাম ইনপুট ফিল্ড খুঁজে পাওয়া যায়নি")

try:
    dob_field = device(text="Date of birth")
    if dob_field.exists:
        dob_field.click()
    else:
        dob_field = device(resourceId="com.facebook.katana:id/dob")
        if dob_field.exists:
            dob_field.click()
        else:
            device(className="android.widget.EditText", instance=0).click()
    
    time.sleep(2)
    
    device(resourceId="android:id/month").set_text("Jan")
    device(resourceId="android:id/day").set_text("15")
    device(resourceId="android:id/year").set_text("1995")
    
    time.sleep(1)
    set_btn = device(text="SET")
    if not set_btn.exists:
        set_btn = device(text="OK")
    if not set_btn.exists:
        set_btn = device(text="Done")
    
    if set_btn.exists:
        set_btn.click()
        print("Set/OK বাটনে ক্লিক করা হয়েছে")
        time.sleep(1)
    
    next_btn = device(text="Next")
    if next_btn.exists:
        next_btn.click()
        print("Next বাটনে ক্লিক করা হয়েছে (DOB section)")
        time.sleep(2)
except Exception as e:
    print(f"Date of birth সিলেক্ট করতে সমস্যা: {e}")


try:
    male_option = device(text="Male")
    if male_option.exists:
        male_option.click()
        print("Male সিলেক্ট করা হয়েছে")
    else:
        male_option = device(resourceId="com.facebook.katana:id/radio_male")
        if male_option.exists:
            male_option.click()
            print("Male সিলেক্ট করা হয়েছে (resourceId দিয়ে)")
        else:
            female_option = device(text="Female")
            if female_option.exists:
                female_option.click()
                print("Female সিলেক্ট করা হয়েছে")
    
    time.sleep(1)
    
    next_btn = device(text="Next")
    if next_btn.exists:
        next_btn.click()
        print("Next বাটনে ক্লিক করা হয়েছে (Gender section)")
        time.sleep(2)
except:
    print("Gender সিলেক্ট করতে সমস্যা")

try:
    email_field = device(resourceId="com.facebook.katana:id/email")
    if email_field.exists:
        email_field.click()
        email_field.clear_text()
        email_field.set_text("johndoe@example.com")
        print("Email ইনপুট করা হয়েছে")
    else:
        email_field = device(className="android.widget.EditText")
        email_field.set_text("johndoe@example.com")
    
    time.sleep(1)
    
    
    next_btn = device(text="Next")
    if next_btn.exists:
        next_btn.click()
        print("Next বাটনে ক্লিক করা হয়েছে (Email section)")
        time.sleep(2)
except:
    print("Email ইনপুট ফিল্ড খুঁজে পাওয়া যায়নি")

try:
    password_field = device(resourceId="com.facebook.katana:id/password")
    if password_field.exists:
        password_field.click()
        password_field.clear_text()
        password_field.set_text("StrongPass123!")
        print("Password ইনপুট করা হয়েছে")
    else:
        password_field = device(className="android.widget.EditText")
        password_field.set_text("StrongPass123!")
    
    time.sleep(1)
    
    next_btn = device(text="Next")
    if next_btn.exists:
        next_btn.click()
        print("Next বাটনে ক্লিক করা হয়েছে (Password section)")
        time.sleep(2)
except:
    print("Password ইনপুট ফিল্ড খুঁজে পাওয়া যায়নি")


try:
    agree_checkbox = device(text="I agree")
    if agree_checkbox.exists:
        agree_checkbox.click()
        print("I agree তে ক্লিক করা হয়েছে")
    else:
        agree_checkbox = device(resourceId="com.facebook.katana:id/agree_checkbox")
        if agree_checkbox.exists:
            agree_checkbox.click()
            print("I agree তে ক্লিক করা হয়েছে (resourceId দিয়ে)")
    
    time.sleep(1)
    
    finish_btn = device(text="Create account")
    if not finish_btn.exists:
        finish_btn = device(text="Finish")
    if not finish_btn.exists:
        finish_btn = device(text="Sign up")
    
    if finish_btn.exists:
        finish_btn.click()
        print("Create account/Finish বাটনে ক্লিক করা হয়েছে")
    else:
        print("Create account বাটন খুঁজে পাওয়া যায়নি, শুধু I agree চেকবক্সে ক্লিক করা হয়েছে")
    
except Exception as e:
    print(f"I agree ক্লিক করতে সমস্যা: {e}")

print("অ্যাকাউন্ট তৈরি প্রক্রিয়া সম্পন্ন হয়েছে!")
