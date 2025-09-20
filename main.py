import os
import time
import tkinter as tk
import threading
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from pushbullet import API
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinter.ttk import Button as ttk_but
from dotenv import load_dotenv
from PIL import ImageTk

load_dotenv("depends\conf.env")
API_KEY = os.getenv("API_KEY")
PASSW = os.getenv("PASSWORD")
USER = os.getenv("USER")

class Kaeto(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        icon = ImageTk.PhotoImage(file="depends/CHEBBY ENERGY.png")
        self.title("Kaeto's App")
        self.iconphoto(False, icon)
        self.wm_state('zoomed')

        #temporarily remove parameters from displaying
        def clear_set_children(where):
            for widget in self.winfo_children():
                if widget in where:
                    widget.grid_remove()

        # delete all current subset widgets of self not in parameters
        def destroy_set_children(where):
            for widget in self.winfo_children():
                if  widget not in where:
                    widget.destroy()

        #bring back widgets in parameters
        # def bring_set_children(self, where):
        #     for widget in self.winfo_children():
        #         if widget in where:
        #             widget.grid()

        #handling mouse events
        def on_left_key_press(event, canv_pro):
            if canv_pro.winfo_exists() and canv_pro.focus_displayof():
                canv_pro.xview_scroll(-1, "units")

        def on_right_key_press(event, canv_pro):
            if canv_pro.winfo_exists() and canv_pro.focus_displayof():
                canv_pro.xview_scroll(1, "units")

        def on_up_key_press(event, canv_pro):
            if canv_pro.winfo_exists():                    
                canv_pro.yview_scroll(-1, "units")

        def on_down_key_press(event, canv_pro):
            if canv_pro.winfo_exists():
                canv_pro.yview_scroll(1, "units")

        def on_mouse_wheel(event, canv_pro):
            if canv_pro.winfo_exists():
                if event.state & 0x01:
                    canv_pro.xview_scroll(-event.delta, "units")
                else:
                    canv_pro.yview_scroll(-event.delta, "units")
        
        #dict of first selections
        choose_lessons = ["Pure Mathematics", "Statistics", "Mechanics",
                          "Modules 2-4 and Module 1 Practical Skills", 
                            "Modules 5-6 and Module 1 Practical Skills",
                            "Papers 1, 2 and 3",
                         ]
        
        def start_from_sec(window, first_sub, second_sub, should_scroll):
            for var in self.winfo_children():
                if var not in obj:
                    var.pack_forget()

            # clear_set_children(obj_2)
            threading.Thread(target=self.main, args=(first_sub, second_sub, should_scroll)).start()
        
        def get_inner_sub(subject, val):
            sub_lessons = {
                    0: "depends/Pure.txt",
                    1: "depends/Statistics.txt",
                    2: "depends/Mechanics.txt",
                    3: "depends/Modules 2-4.txt",
                    4: "depends/Modules 5-6.txt",
                    5: "depends/Papers.txt",
                }
            
            clear_set_children(obj)
            
            #Configure scrollbars before moving on
            frame_pro = tk.Frame(self, )
            frame_pro.pack(side='left', fill='both', expand=True)
            
            canv_pro = tk.Canvas(frame_pro, )
            canv_pro.pack(side='top', fill='both', expand=True)
            
            #scrollabars
            proj_scroll_horiz = tk.Scrollbar(frame_pro, orient='horizontal', command=canv_pro.xview)
            proj_scroll_horiz.pack(side='bottom', fill='x')
                                    
            proj_scroll_vert = tk.Scrollbar(self, orient='vertical', command=canv_pro.yview)
            proj_scroll_vert.pack(side='right', fill='y')
            
            #configure scrollbars for canvas
            canv_pro.config(xscrollcommand=proj_scroll_horiz.set,
                            yscrollcommand=proj_scroll_vert.set,
                            )
            proj_frame = tk.Frame(canv_pro, )
            canv_pro.create_window((0,0), window = proj_frame, anchor = 'n')
            
            def upd_scroll_proj(event):
                if canv_pro.winfo_exists():
                    canv_pro.configure(scrollregion=canv_pro.bbox('all'))
            
            proj_frame.bind("<Configure>", upd_scroll_proj)
                                                                    
            self.bind("<Left>", lambda event: on_left_key_press(event, canv_pro))
            self.bind("<Right>", lambda event: on_right_key_press(event, canv_pro))
            self.bind("<Up>", lambda event: on_up_key_press(event, canv_pro))
            self.bind("<Down>", lambda event: on_down_key_press(event, canv_pro))
            self.bind("<MouseWheel>", lambda event: on_mouse_wheel(event, canv_pro))

            should_scroll = val > 2

            get_select_lvl2(proj_frame, subject, sub_lessons[val], should_scroll)


        def get_select_lvl2(window, subject, document, should_scroll):
            with open(document) as file:
                screen2_txt = file.read()
                screen2_txt = screen2_txt.split('\n')

            #show buttons of 2nd screen
            i, j = 1, 0
            for count, var in enumerate(screen2_txt):
                if count % 3 == 0 and count > 0:
                    i += 1
                    j = 0

                seco_screen = ttk_but(window, text=f"{var}", command = lambda window=window, subject = subject, subtopic=var, whether = should_scroll: start_from_sec(window, subject, subtopic, whether))
                seco_screen.grid(row=i, column=j, pady=30, padx=(20, 30), ipady=50, ipadx=50)
                j += 1


        #Show initial buttons on screen for user choice
        i, j = 1, 0
        for count, subject in enumerate(choose_lessons):
            if count % 3 == 0 and count > 0:
                i += 1
                j = 0

            subject_btn = ttk_but(self, text=f"{subject}", command=lambda val=count, subject=subject: get_inner_sub(subject, val))
            subject_btn.grid(row=i, column=j, pady=40, padx=(20, 30), ipady=50, ipadx=50)
            j += 1

        obj = self.winfo_children()

    def main(self, subject, subtopic, should_scroll):
        api = API()
        api.set_token(API_KEY)

        url = "https://web.uplearn.co.uk/login?" 

        service = Service("depends/msedgedriver.exe")
        driver = webdriver.Edge(service=service)

        driver.get(url)
        wait = WebDriverWait(driver, 17)

        def get_find(how, target):
            if how == "css":
                res = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target)))
                return res
            
            #only check with id if only presence should be checked
            if how == "id":
                res = wait.until(EC.presence_of_element_located((By.ID, target)))
                return res

            elif how == "name":
                res = wait.until(EC.element_to_be_clickable((By.NAME, target)))
                return res
            
            elif how == "path":
                res = wait.until(EC.element_to_be_clickable((By.XPATH, target)))
                return res

            else:
                return "Enter a valid find method!"

        try:
            privy = get_find("css", 'a[data-order="0"]')
            privy.click()
        except:
            pass

        enter_email = get_find("name", "email")
        enter_email.send_keys(USER)

        enter_password = get_find("name", "password")
        enter_password.send_keys(PASSW)
        enter_password.submit()
        time.sleep(2)
        driver.maximize_window()

        if should_scroll:
            total_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, arguments[0]);", (total_height/2))

        else:
            pass

        math = get_find("path", f"//h4[text()='{subject}']")
        time.sleep(1)
        math.click()

        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, arguments[0]);", total_height / 3.5)
        time.sleep(1)

        # #added line for scraping elements##################
        # written = driver.find_elements(By.CSS_SELECTOR, 'p[class="sc-fqkvVR fjuAnp"]')
        # with open(subtopic, 'w') as file:
        #     for var in written:
        #         file.write(var.text + '\n')

        # #######################
        tot = driver.execute_script("return document.body.scrollHeight")
        total_height = tot / 7
        # driver.execute_script("window.scrollTo(0, arguments[0]);", total_height)

        while True:
            for i in range(7):
                try:
                    driver.execute_script("window.scrollTo(0, arguments[0]);", total_height)
                    time.sleep(1)
                    poly_nom = get_find("path", f"//p[text()='{subtopic}']")
                    time.sleep(2)
                    poly_nom.click()
                    break
                except:
                    total_height += (tot/7)
                    pass

            break
        
        time.sleep(2)

        try:
            skip_know = get_find("css", 'i[class="sc-jwZKMi bIHcKA fa fa-close"]')
            skip_know.click()
        except:
            pass

        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, arguments[0]);", total_height / 3.5)

        math_things = driver.find_elements(By.XPATH, "//span[@class='sc-fqkvVR jqGhmw']")
        math_times = [var.text for var in math_things]
        scheds = []
        tot_tim = 0

        for char in math_times:
            if "quiz" in char:
                scheds.append(tot_tim)
                scheds.append('quest')
                tot_tim = 0
            else:
                spl_item = (char.split())[0]
                val = ''.join(spl_item[1:])
                tot_tim += (int(val) * 60) + 10
        
        scheds.append(tot_tim)

        inner_sub = driver.find_elements(By.CSS_SELECTOR, 'p[class="sc-fqkvVR eEQpb"]')
        time.sleep(2)
        inner_sub[0].click()

        for ting in scheds:
            if ting == 'quest':
                api.send_note("SCHOOL WORK!!", "Yh, the tutorial stuff is on pause now, just answer the questions and leave me (please press continue) :)")
                pass
            else:
                start_time = time.time() + ting
                while time.time() <= start_time:
                    try:
                        time.sleep(5)
                        check_necess = driver.execute_script("return document.getElementById('numQuizzes').textContent;")
                    except:
                        pass

                    if int(check_necess) < 1:
                        pass
                    else:
                        quizzes = driver.find_elements(By.CSS_SELECTOR, 'div[class="quizDiv videoQuizOverlay pquizOverlay newQuizSystem"]')
                        quiz_times = [float(var.get_attribute('data-time')) for var in quizzes]
                        quiz_times.sort()
                        
                        for var in quiz_times:
                            while True:
                                vid_tim = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Playbar"]').get_attribute("aria-valuenow")

                                if float(vid_tim) >= var - 2:
                                    api.send_note("SCHOOL WORK!!", "Yh, the tutorial stuff is on pause now, just answer the questions and leave me (please press continue) :)")
                                    time.sleep(10)

                                    new = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Playbar"]').get_attribute("aria-valuenow")
                                    if float(new) > float(vid_tim):
                                        break

                                time.sleep(2)

        #Signify that selenium is done
        selenium_done_event.set()

        print("Hey")
        messagebox.showinfo("Success", "Program successfully executed....")

if __name__ == "__main__":
    app = Kaeto()

    selenium_done_event = threading.Event()
    app.mainloop()

    selenium_done_event.wait()

#modify code to calc time based on where user starts from
