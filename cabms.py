import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("./cab.db")
curr = conn.cursor()
curr.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT PRIMARY KEY, password TEXT NOT NULL, mobile TEXT NOT NULL, email TEXT NOT NULL, gender TEXT NOT NULL)''')
conn.commit()
conn.close()

def get_from():
	conn = sqlite3.connect("./distances.db")
	curr = conn.cursor()
	temp = curr.execute("""SELECT "from" FROM distance""").fetchall()
	OPTIONS = [i[0] for i in temp]
	conn.close()
	return OPTIONS

def get_to():
	conn = sqlite3.connect("./distances.db")
	curr = conn.cursor()
	temp = curr.execute("""SELECT "to" FROM distance""").fetchall()
	OPTIONS = [i[0] for i in temp]
	conn.close()
	return OPTIONS

def calculate_fare():
	return "fare"

def insert_into_database(u,p,m,e,g):
	if g==1:
		g = "male"
	else:
		g = "female"
	conn = sqlite3.connect("./cab.db")
	curr = conn.cursor()
	curr.execute('''INSERT INTO users(name,password,mobile,email,gender) VALUES(?,?,?,?,?)''' ,  (u,p,m,e,g))
	conn.commit()
	conn.close()

def availability(u,m,e,):
	conn = sqlite3.connect("./cab.db")
	curr = conn.cursor()

	query1 = f"""SELECT name FROM users WHERE name='{u}'"""
	if curr.execute(query1).fetchone() is not None:
		tk.messagebox.showerror("duplicate", "username is taken")
		return False

	query2 = f"""SELECT mobile FROM users WHERE mobile='{m}'"""
	if curr.execute(query2).fetchone() is not None:
		tk.messagebox.showerror("duplicate", "mobile already registered")
		return False

	query3 = f"""SELECT email FROM users WHERE email='{e}'"""
	if curr.execute(query3).fetchone() is not None:
		tk.messagebox.showerror("duplicate", "email is taken")
		return False

	curr.close()
	conn.close()
	return True

def register_user():
	username_info = username.get()
	password_info = password.get()
	mobile_info = mobile.get()
	email_info = email.get()
	gender_info = v.get()


	if username_info=="" or password_info=="" or mobile_info=="" or email_info=="":
		tk.messagebox.showerror("enter all the details")
	
	print(username_info,password_info, mobile_info, email_info, gender_info)
	
	if availability(username_info,mobile_info,gender_info):
		insert_into_database(username_info,password_info,mobile_info,email_info,gender_info)
		tk.Label(screen1,text = "Registraion successfull", fg="green", font=("Calibri,11")).pack()
	else:
		tk.Label(screen1,text = "Registraion unsuccessfull", fg="red", font=("Calibri,11")).pack()
	
	username_entry.delete(0, tk.END)
	password_entry.delete(0, tk.END)
	mobile_entry.delete(0, tk.END)
	email_entry.delete(0, tk.END)

def register():
	global screen1
	screen1 = tk.Toplevel(screen)
	screen1.title("Register")
	screen1.geometry("400x320")

	global username
	global password
	global mobile
	global email
	global v

	global username_entry
	global password_entry
	global mobile_entry
	global email_entry

	username = tk.StringVar()
	password = tk.StringVar()
	mobile = tk.StringVar()
	email = tk.StringVar()
	v = tk.IntVar() #Gender

	tk.Label(screen1, text="please enter details below").pack()
	tk.Label(screen1, text="").pack()

	tk.Label(screen1, text="Username * ").pack()
	username_entry = tk.Entry(screen1, textvariable=username)
	username_entry.pack()

	tk.Label(screen1, text="Password * ").pack()
	password_entry = tk.Entry(screen1, textvariable=password)
	password_entry.pack()

	tk.Label(screen1, text="Mobile no *").pack()
	mobile_entry = tk.Entry(screen1, textvariable=mobile)
	mobile_entry.pack()

	tk.Label(screen1, text="email id *").pack()
	email_entry = tk.Entry(screen1, textvariable=email)
	email_entry.pack()

	
	tk.Label(screen1, text="gender * ").pack()
	tk.Radiobutton(screen1, text="male", variable=v ,value=1).pack()
	tk.Radiobutton(screen1, text="female", variable=v ,value=2).pack()
	
	tk.Button(screen1,text="Register",width=10, height=1, command=register_user).pack()

def bookit():
	FROM = frm.get()
	TO = to.get()
	MOBILE = book_mobile.get()
	TIME = time.get()
	DAY = day.get()
	conn = sqlite3.connect("./bookings.db")
	curr = conn.cursor()
	curr.execute("""CREATE TABLE IF NOT EXISTS booking(userid TEXT PRIMARY KEY, mobile TEXT, frm TEXT, t TEXT, day TEXT, tm TEXT)""")
	curr.execute("""INSERT INTO booking VALUES(?,?,?,?,?,?)""", (current_user, MOBILE, FROM, TO, DAY, TIME))
	conn.commit()
	conn.close()
	print("inserted ",current_user, MOBILE, FROM, TO, DAY, TIME)

def show_bookings(books):
	global screen5
	screen5 = tk.Toplevel(screen)
	screen5.title("booking already made!!")
	scrollbar = tk.Scrollbar(screen5)
	scrollbar.pack(side = tk.RIGHT, fill = tk.Y ) 
	mylist = tk.Listbox(screen5, yscrollcommand = scrollbar.set, width=50) 
	for line in range(len(books)): 
   		mylist.insert(tk.END, books[line]) 
	mylist.pack( side = tk.LEFT, fill = tk.BOTH ) 
	scrollbar.config( command = mylist.yview )

def prevbook():
	check_user = current_user
	conn = sqlite3.connect("./bookings.db")
	curr = conn.cursor()
	q = f"""SELECT * FROM booking WHERE userid='{check_user}'"""
	res = curr.execute(q).fetchall()
	if len(res) == 0:
		tk.messagebox.showinfo("info", "no booking have been made yet!!")
	else:
		show_bookings(res)

def bookcab(user):
	global current_user
	current_user = user

	global screen4
	screen4 = tk.Toplevel(screen)
	screen4.title("fill in the details to book your cab!")
	screen4.geometry("400x370")

	#mobile
	global book_mobile
	book_mobile = tk.StringVar()
	tk.Label(screen4, text="mobile no").pack()
	username_entry = tk.Entry(screen4, textvariable=book_mobile)
	username_entry.pack()

	#from
	global frm
	from_options = get_from()
	frm = tk.StringVar(screen4)
	frm.set("FROM")
	w = tk.OptionMenu(screen4, frm, *from_options)
	w.pack()

	#to
	global to
	to_options = get_to()
	to = tk.StringVar(screen4)
	to.set("TO")
	w2 = tk.OptionMenu(screen4, to, *to_options)
	w2.pack()

	#fare
	tk.Label(screen4, text=calculate_fare(), height=2, font=("Calibri,15")).pack()

	#day
	global day
	day_options = [i for i in range(1,32)]
	day = tk.StringVar(screen4)
	day.set("DATE THIS MONTH")
	w3 = tk.OptionMenu(screen4, day, *day_options)
	w3.pack()

	#time
	global time
	time = tk.StringVar()
	tk.Label(screen4, text="time").pack()
	time_entry = tk.Entry(screen4)
	time_entry.pack()
	time_entry.insert(0, "enter like, 5 30")
	time_entry.bind("<FocusIn>", lambda args: time_entry.delete('0', 'end'))

	tk.Label(screen4).pack()
	tk.Button(screen4, text="Book It",width="30",height="2",command=bookit).pack()

	tk.Label(screen4).pack()
	tk.Button(screen4, text="Previous bookings",width="30",height="2",command=prevbook).pack()

def login_verify():
	username1 = username_verify.get()
	password1 = password_verify.get()
	username_entry1.delete(0,tk.END)
	password_entry1.delete(0,tk.END)

	db = sqlite3.connect("./cab.db")
	curr = db.cursor()
	query = f"""SELECT name,password FROM users WHERE name='{username1}'"""
	if curr.execute(query).fetchone() != (username1,password1):
		tk.messagebox.showerror("invalid credentials", "wrong username or password")
	else:
		tk.Label(screen2,text = "Login successfull", fg="green", font=("Calibri,11")).pack()
		tk.messagebox.showinfo("successfull", "Login successfull")
		bookcab(username1)
	db.close()

def login():
	global screen2
	screen2 = tk.Toplevel(screen)
	screen2.title("Login")
	screen2.geometry("300x250")
	tk.Label(screen2, text="please enter details below").pack()
	tk.Label(screen2, text="").pack()

	global username_verify
	global password_verify
	username_verify = tk.StringVar()
	password_verify = tk.StringVar()

	tk.Label(screen2, text="Username").pack()
	global username_entry1
	username_entry1 = tk.Entry(screen2, textvariable=username_verify)
	username_entry1.pack()

	tk.Label(screen2, text="").pack()

	tk.Label(screen2, text="Password").pack()
	global password_entry1
	password_entry1 = tk.Entry(screen2, textvariable=password_verify)
	password_entry1.pack()

	tk.Label(screen2, text="").pack()

	tk.Button(screen2, text="Login", width="10", height="1", command=login_verify).pack()

def routes():
	with open("./routes.txt", "r") as file:
		routes = list()
		for line in file.readlines():
			routes.append(line.strip())

	global screen3
	screen3 = tk.Toplevel(screen)
	screen3.title("available routes")
	scrollbar = tk.Scrollbar(screen3)
	scrollbar.pack(side = tk.RIGHT, fill = tk.Y ) 
	mylist = tk.Listbox(screen3, yscrollcommand = scrollbar.set, width=50) 
	for line in range(len(routes)): 
   		mylist.insert(tk.END, routes[line]) 
	mylist.pack( side = tk.LEFT, fill = tk.BOTH ) 
	scrollbar.config( command = mylist.yview )

def main_screen():
	global screen
	screen = tk.Tk()
	screen.geometry("450x250")
	screen.title("cab booking system")
	tk.Label(text="book a cab", bg="grey", width="300",height="2", font=("Calibri,13")).pack()
	tk.Label(text="").pack()
	tk.Button(text="Login",width="30",height="2", command=login).pack()
	tk.Label(text="").pack()
	tk.Button(text="Register",width="30",height="2", command=register).pack()
	tk.Label(text="").pack()
	tk.Button(text="Available Routes",width="30",height="2", command=routes).pack()

	#test
	# tk.Label(text="").pack()
	# tk.Button(text="book",width="30",height="2", command=bookcab).pack()


	screen.mainloop()

main_screen()