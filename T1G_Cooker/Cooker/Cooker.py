import time
import utilities.api.item_ids as ids
import utilities.color as clr
import utilities.random_util as rd
from model.osrs.osrs_bot import OSRSBot
from model.runelite_bot import BotStatus
from utilities.api.morg_http_client import MorgHTTPSocket
from utilities.api.status_socket import StatusSocket
from utilities.geometry import RuneLiteObject
import pyautogui as pag
import model.osrs.Cooker.BotSpecImageSearch as imsearch
import utilities.game_launcher as launcher
import pathlib
import utilities.T1G_API as T1G_API
import utilities.ScreenToClient as stc
import utilities.BackGroundScreenCap as bcp
import utilities.RIOmouse as Mouse



    
class OSRSCooker(OSRSBot):
    api_m = MorgHTTPSocket()
    def __init__(self):
        bot_title = "ThatOneGuys Cooker"
        description = "Cooker"
        super().__init__(bot_title=bot_title, description=description)
        self.potion_to_make = None
        self.running_time = 1
        self.take_breaks = False
        self.break_length_min = 1
        self.break_length_max = 500
        self.time_between_actions_min =0.8
        self.time_between_actions_max =5
        self.potion_to_make = None
        self.mouse_speed = "medium"
        self.break_probabilty = 0.13
        self.Client_Info = None
        self.win_name = None
        self.pid_number = None
        self.Input = "failed to set mouse input"
        self.setupran = False
        self.alchedItems = 0

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 500)
        self.options_builder.add_checkbox_option("take_breaks", "Take breaks?", [" "])
        self.options_builder.add_slider_option("break_probabilty", "Chance to take breaks (percent)",1,100)
        self.options_builder.add_slider_option("break_length_min", "How long to take breaks (min) (Seconds)?", 1, 300)
        self.options_builder.add_slider_option("break_length_max", "How long to take breaks (max) (Seconds)?", 2, 300)    
        self.options_builder.add_checkbox_option("mouse_speed", "Mouse Speed (must choose & only select one)",[ "slowest", "slow","medium","fast","fastest"])
        self.options_builder.add_slider_option("time_between_actions_min", "How long to take between actions (min) (MiliSeconds)?", 600,3000)
        self.options_builder.add_slider_option("time_between_actions_max", "How long to take between actions (max) (MiliSeconds)?", 600,3000)
        
        self.options_builder.add_process_selector("Client_Info")
        self.options_builder.add_checkbox_option("Input","Choose Input Method",["Remote","PAG"])
        
                                               
    def save_options(self, options: dict):
        for option in options:        
            if option == "running_time":
                self.running_time = options[option]
            elif option == "take_breaks":
                self.take_breaks = options[option] != []
            elif option == "break_length_min":
                self.break_length_min = options[option]
            elif option == "break_length_max":
                self.break_length_max = (options[option])
            elif option == "mouse_speed":
                self.mouse_speed = options[option]
            elif option == "time_between_actions_min":
                self.time_between_actions_min = options[option]/1000
            elif option == "time_between_actions_max":
                self.time_between_actions_max = options[option]/1000
            elif option == "break_probabilty":
                self.break_probabilty = options[option]/100
                
            elif option == "Client_Info":
                self.Client_Info = options[option]
                client_info = str(self.Client_Info)
                win_name, pid_number = client_info.split(" : ")
                self.win_name = win_name
                self.pid_number = int(pid_number)
                self.win.window_title = self.win_name
                self.win.window_pid = self.pid_number
                stc.window_title = self.win_name
                Mouse.Mouse.clientpidSet = self.pid_number
                bcp.window_title = self.win_name
                bcp
            elif option == "Input":
                self.Input = options[option]
                if self.Input == ['Remote']:
                    Mouse.Mouse.RemoteInputEnabledSet = True
                elif self.Input == ['PAG']:
                    Mouse.Mouse.RemoteInputEnabledSet = False
                
                
            else:
                self.log_msg(f"Unknown option: {option}")
                print("Developer: ensure that the option keys are correct, and that options are being unpacked correctly.")
                self.options_set = False
                return
        self.log_msg(f"Running time: {self.running_time} minutes.")
        self.log_msg(f"Bot will{' ' if self.take_breaks else ' not '}take breaks.")
        self.log_msg(f"We are making {self.potion_to_make}s")
        self.log_msg("Options set successfully.")
        self.options_set = True
        
        

    def main_loop(self):
        start_time = time.time()
        end_time = self.running_time * 60
        print(self.mouse_speed)
        start_time = time.time()
        end_time = self.running_time * 60
        while time.time() - start_time < end_time:
            if rd.random_chance(probability=self.break_probabilty) and self.take_breaks:
                self.take_break(min_seconds =self.break_length_min, max_seconds=self.break_length_max, fancy=True)   
        
            self.update_progress((time.time() - start_time) / end_time)
            self.bot_loop_main()
        self.update_progress(1)
        self.log_msg("Finished.")
        self.logout()
        self.stop()
         
    
            

            
    def bot_loop_main(self):
        if self.setupran == False:
            self.setup()
        self.click_nearest_bank()
        self.deposit_all()
        self.find_food_item()
        self.close_bank()
        self.find_nearest_oven()
        self.SendKeyForCooking()
        self.find_nearest_bank()
        self.wait_until_idle()
        

        
        

    def find_food_item(self):
        raw_Food_Image = imsearch.BOT_IMAGES.joinpath("Cooker_IMG", "Raw_anglerfish_bank.png")
 
        raw_Food_Image = imsearch.search_img_in_rect(raw_Food_Image_Image, self.win.game_view)
      
        
        if  raw_Food_Image:
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            self.mouse.move_to(raw_Food_Image.random_point())
            time.sleep(Sleep_time)
            self.mouse.click()
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            time.sleep(Sleep_time)
        else:
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            time.sleep(Sleep_time)
            self.find_food_item()
    
    def close_bank(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        Close_Bank_img = imsearch.BOT_IMAGES.joinpath("Cooker_IMG", "x.png")
        
        if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
            self.mouse.move_to(Close_bank.random_point(),mouseSpeed=self.mouse_speed[0])
            self.mouse.click()
            time.sleep(0.65)
            if Close_bank := imsearch.search_img_in_rect(Close_Bank_img, self.win.game_view):
                self.close_bank()
            else:
                time.sleep(.1)
                
                
        else:
            self.log_msg(f"Could not close bank")
            self.stop()       
            
            
    def setup(self):
        self.find_nearest_bank()
        self.setupran = True
            
            
    def wait_until_idle(self):
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        raw_food_item_img = imsearch.BOT_IMAGES.joinpath("Cooker_IMG", "Raw_anglerfish.png")
        if raw_food_item := imsearch.search_img_in_rect(raw_food_item_img, self.win.inventory_slots[27]):
            time.sleep(0.5)
            self.wait_until_idle()
        else:
            print("idle")
            time.sleep(rd.fancy_normal_sample(1.3,8.29))
    
    def find_nearest_bank(self):
          
        if banks := self.get_all_tagged_in_rect(self.win.game_view, clr.CYAN):
            banks = sorted(banks, key=RuneLiteObject.distance_from_rect_center)             
            self.mouse.move_to(banks[0].random_point(),mouseSpeed=self.mouse_speed[0]) 
        else:
            self.log_msg(f"aay you moron stand near a bank tagged cyan")
            
    def click_nearest_bank(self):
            self.mouse.click(check_red_click=True)

            
    def find_nearest_oven(self):
          
        if banks := self.get_all_tagged_in_rect(self.win.game_view, clr.PINK):
            banks = sorted(banks, key=RuneLiteObject.distance_from_rect_center)             
            self.mouse.move_to(banks[0].random_point(),mouseSpeed=self.mouse_speed[0])
            if self.mouseover_text(contains="Cook", color=clr.OFF_WHITE):
                self.mouse.click()
            else:
                self.find_nearest_oven()
        else:
            self.log_msg(f"aay you moron stand near a oven tagged pink") 
            
    def deposit_all(self):
        Desposit_all_img = imsearch.BOT_IMAGES.joinpath("Cooker_IMG", "deposit.png")  
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        counter = 0

        while True:
            Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)
            if Desposit_all:  
                break
            time.sleep(0.5)
            counter = counter + 1
            if counter ==10:
                self.find_nearest_bank()
                time.sleep(Sleep_time)
                self.click_nearest_bank()
            if counter == 20:
                self.logout()
                self.stop()
        Desposit_all = imsearch.search_img_in_rect(Desposit_all_img, self.win.game_view)  
        self.log_msg(f"depositing all items")
        self.mouse.move_to(Desposit_all.random_point(),mouseSpeed=self.mouse_speed[0])
        self.mouse.click()
        time.sleep(Sleep_time)
       
            
            
    def SendKeyForCooking(self):
        make_menu_open_img = imsearch.BOT_IMAGES.joinpath("Cooker_IMG", "make_menu_shark.png") #change this to the chat image of your item you want to cook
        Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
        if make_menu_open := imsearch.search_img_in_rect(make_menu_open_img, self.win.chat):
            time.sleep(Sleep_time)
            self.mouse.send_key(400,"1")
            Sleep_time = rd.fancy_normal_sample(self.time_between_actions_min, self.time_between_actions_max)
            time.sleep(Sleep_time)
        else:
            self.SendKeyForCooking()