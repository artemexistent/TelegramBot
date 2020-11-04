import telebotimport sqlite3from telebot import typesTOKEN = "1375970362:AAE8ZdZHn46q-R3lfQnZHsCJ3_GmL5-hpeE"bot = telebot.TeleBot(TOKEN)def get(message):    connection = sqlite3.connect("info.dp")    cursor = connection.cursor()    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int, name text)")    cursor.execute("SELECT id, name FROM users WHERE id = ?", (message.chat.id,))    exist = cursor.fetchone()    cursor.close()    connection.close()    return existdef get2(s):    connection = sqlite3.connect("info.dp")    cursor = connection.cursor()    cursor.execute("SELECT * FROM price WHERE url = ?", (s,))    exist = cursor.fetchone()    cursor.close()    connection.close()    return existdef get_info(message):    connection = sqlite3.connect("info.dp")    cursor = connection.cursor()    cursor.execute("SELECT url FROM url WHERE id = ?", (message.chat.id,))    exist = cursor.fetchall()    cursor.close()    connection.close()    return exist@bot.message_handler(commands=['start'])def start(message):    print('User {id} press start'.format(id=message.chat.id))    exist = get(message)    if exist:        bot.send_message(message.chat.id, 'You are already registered.')    else:        sent = bot.send_message(message.chat.id, 'What is your name?')        bot.register_next_step_handler(sent, hello)def hello(message):    connection = sqlite3.connect("info.dp")    info = message.chat.id, message.text    cursor = connection.cursor()    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int, name text)")    cursor.execute("INSERT INTO users VALUES (?, ?)", info)    print("New user: {name}".format(name=message.text))    bot.send_message(message.chat.id, 'Hello, {name}. I am glad to see you.'.format(name=message.text))    connection.commit()    cursor.close()    connection.close()@bot.message_handler(commands=['help'])def help(message):    print('User {id} press help'.format(id=message.chat.id))    bot.send_message(message.chat.id, helps())def helps():    ans = '/start - registration\n'    ans += '/help - output of all commands\n'    ans += '/get_price - \n'    ans += '/add_product - \n'    ans += '/settings - edit profile'    return ans@bot.message_handler(commands=['settings'])def settings(message):    print('User {id} press settings'.format(id=message.chat.id))    exist = get(message)    if exist:        keyboard = types.InlineKeyboardMarkup()        callback_button = types.InlineKeyboardButton(text="Изменить Имя", callback_data="update_name")        keyboard.add(callback_button)        e = get_info(message)        if e:            for i in e:                print(i[0])                r = get2(i[0])                callback = types.InlineKeyboardButton(text="{name}".format(name=r[2]), callback_data="get_product")                keyboard.add(callback)            bot.send_message(message.chat.id, 'Your name: {name}'.format(name=exist[1]), reply_markup=keyboard)    else:        bot.send_message(message.chat.id, 'I do not know you, please register')@bot.message_handler(regexp="Hello")def handler_message(message):    print('User {id} write {text}'.format(id=message.chat.id, text=message.text))    exist = get(message)    if exist:        bot.send_message(message.chat.id, 'Hello, {name}. I am glad to see you.'.format(name=exist[1]))    else:        bot.send_message(message.chat.id, 'I do not know you, please register')@bot.message_handler(commands=['get_users'])def get_users(message):    print('User {id} want show'.format(id=message.chat.id))    if message.chat.id == 334396592:        output = ''        connection = sqlite3.connect("info.dp")        cursor = connection.cursor()        cursor.execute("SELECT * FROM users")        while True:            row = cursor.fetchone()            if row == None:                break            output += '{one} - {two}'.format(one=row[0], two=row[1]) + '\n'        bot.send_message(message.chat.id, output)        cursor.close()        connection.close()    else:        bot.send_message(message.chat.id, 'You are not an admin')@bot.callback_query_handler(func=lambda call: True)def callback_inline(call):    if call.data == "update_name":        sent = bot.send_message(call.message.chat.id, 'Enter a new name?')        bot.register_next_step_handler(sent, update_name)    if call.data == "get_product":        e = get_info(call.message)        call.message.text = str(e[0])        e = get2(call.message.text)        bot.send_message(call.message.chat.id, e[1])def update_name(message):    connection = sqlite3.connect("info.dp")    cursor = connection.cursor()    exist = get(message)    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (message.text, message.chat.id))    print('{old} name changed : {name}'.format(old=exist[1], name=message.text))    bot.send_message(message.chat.id, 'Name changed!')    connection.commit()    cursor.close()    connection.close()@bot.message_handler(commands=['get_price'])def get_url(message):    sent = bot.send_message(message.chat.id, 'Введите ссылку')    bot.register_next_step_handler(sent, price)def price(message):    from get_price import get_price    print(message.text)    bot.send_message(message.chat.id, "Это займет меньше 2 минут")    url = message.text    info = get_price(url)    if info[0]==-1:        bot.send_message(message.chat.id, "This product sell")    else :        bot.send_message(message.chat.id, info[0])        bot.send_message(message.chat.id, info[1])@bot.message_handler(commands=['add_product'])def add(message):    exist = get(message)    if exist:        sent = bot.send_message(message.chat.id, 'Введите ссылку')        bot.register_next_step_handler(sent, url)    else:        bot.send_message(message.chat.id, 'I do not know you, please register')def url(message):    connection = sqlite3.connect("info.dp")    cursor = connection.cursor()    cursor.execute("CREATE TABLE IF NOT EXISTS price (url text, price text, name text)")    from get_price import get_url    from get_price import get_price    get_url(message)    info = get_price(message.text)    bot.send_message(message.chat.id, 'You url added!')    if info[0]==-1:        bot.send_message(message.chat.id, "This product sell")    else:        bot.send_message(message.chat.id, info[0])        bot.send_message(message.chat.id, info[1])        if get2(message.text):            r = ""        else:            cursor.execute("INSERT INTO price VALUES (?, ?, ?)", (message.text, info[1], info[0]))        connection.commit()        cursor.close()        connection.close()@bot.message_handler(regexp='')def handler_message(message):    print('User {id} write {text}'.format(id=message.chat.id, text=message.text))    bot.send_message(message.chat.id, 'I do not understand you')bot.polling()