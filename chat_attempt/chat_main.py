
#для единственного sleep, который по сути и не нужен
import time 

# для проверки(одной из) валидности ip
from re import fullmatch 

# вообще в chat_client, chat_server библа импортируется поностью, нехорошо
from socket import SHUT_WR 


from threading import Thread

#from datetime import now, isoformat
import datetime

from UI_classes import *
import chat_client, chat_server




def main():

    window = UI_window()
    enable_styles()
    context = context_store(window)

    def close_window():
        exit_message(context)
        close_thread(context)
        close_connection(context)
        print("Закрытие окна")
        window.destroy()
    window.protocol("WM_DELETE_WINDOW", close_window)
    
    enter_settings_frame(context)

    window.mainloop()


def enable_styles():
    frame_style = ttk.Style()    
    frame_style.configure(
        "fr_style.TFrame",
        background = "#4000FF"
        )
    
    label_style = ttk.Style()    
    label_style.configure(
        "lbl_style.TLabel",
        background = "#4000FF",
        foreground = "#FFFFFF"
        )
    
    button_style = ttk.Style()    
    button_style.configure(
        "btn_style.TButton",
        background = "#0000FF",
        foreground = "#0000FF"
        )
    
    entry_style = ttk.Style()
    entry_style.configure(
        "entr_style.TEntry",
        background = "#0000FF",
        foreground = "#0000FF"
        )


def enter_settings_frame(context):
    wind = context.window

    #сбрасываем значения на начальные
    context.ip_string.set(chat_server.local_ip() )#начальное значение, свой адрес.по хорошему, не важно что здесь
    context.port_string.set("1408") #начальное значение, от балды
    context.status.set("")
    context.disconnect()

    clear_widgets(wind.winfo_children() )

    frame = SettingsFrame(wind)
    frame.display(  )

    label1 = UI_label(frame, "Выберите способ подключения")
    label1.display( [0,0,2] )

    label2 = UI_label(frame, "Сервер")
    label2.display( [1,0,1] )

    label3 = UI_label(frame, "Клиент")
    label3.display( [1,1,1] )

    widget_list = []

    button1 = UI_button(frame, "Хост", server_button_click(frame, widget_list, context) )
    button1.display( [2,0,1] )

    button2 = UI_button(frame, "Клиент", client_button_click(frame, widget_list, context) )
    button2.display( [2,1,1] )





def server_button_click(fr, w_list, context): #способ передать контекст в функцию. хороший ли?
    
    
    def add_dialog():
        clear_widgets(w_list)
        context.choose_server()

        label4 = UI_label(fr,"Введите порт")
        label4.display([3,0,2])
        w_list.append(label4)

        label5 = UI_label(fr,f"Ваш IP - {chat_server.local_ip()}")
        label5.display([4,0,1])
        w_list.append(label5)

        #context.ip_string.set(chat_server.local_ip() ) #вроде так делать не надо
        context.ip_string.set( "0.0.0.0" ) #...примерное объяснение которое я нашел: компьютер может иметь несколько адресов, через нулевой - способ обратиться ко всем

        entry1 = UI_entry(fr, context.port_string)
        entry1.display([4,1,1])
        w_list.append(entry1)        

        add_bottom(fr,context)


    return add_dialog #функция



def client_button_click(fr, w_list, context):

    
    def add_dialog():
        clear_widgets(w_list)
        context.choose_client()

        label4 = UI_label(fr,"Введите IP адрес и порт")
        label4.display([3,0,2])
        w_list.append(label4)

        entry1 = UI_entry(fr, context.ip_string)
        entry1.display([4,0,1])

        w_list.append(entry1)        

        entry2 = UI_entry(fr, context.port_string)
        entry2.display([4,1,1])
        w_list.append(entry2)   

        add_bottom(fr, context)

    return add_dialog #функция

def add_bottom(fr, context):
    button3 = UI_button(fr, "Коннект", connect_button_click(context) )
    button3.display([5,0,2])

    label6 = UI_label(fr,"Статус", context.status)
    label6.display([6,0,2])


def connect_button_click(context):
    def connection():
        
        if check_ip_valid( context.ip_string.get() ) and check_port_valid(context.port_string.get() ):
            context.status.set("Корректные данные")
            print("Налаживаем соединение")
            t = Thread(target=connect, args=(context, ) ) # 
            t.daemon = True
            t.start()
            #...ошибка? создается поток. поток подключается/слушает подключения, выводит статус происходящего
            # когда связь налажена, в этом же потоке происходит переход в chat_frame
            # все дальнейшее - открытие слушающего потока, обмен сообщениями, закрытие сокетов - происходит в этом созданном потоке
            # чем занят основной поток? возможно я чего-то не понимаю, недостает теории
            # есть ощущение, что оно, конечно, работает, но неправильно
        else:
            context.status.set("Неверные данные")

    return connection

def connect(context):
    if context.is_server_chosen:
        res = chat_server.server_listen_for_connect(context)
    elif context.is_client_chosen:
        res = chat_client.client_connect(context)
    
    if res: #если получилось - празднуем 5 секунд
        time.sleep(5) # чисто чтобы было время увидеть надпись "подключился"
        
        context.is_open = True
        enter_chat_frame(context)


def check_ip_valid(candidate): 
    reg = fullmatch(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", candidate ) 
    if reg != None:
        nums = candidate.split(".")
        for num in nums:
            if int(num) > 255:
                return False
        return True
    else:
        return False

def check_port_valid(candidate):
    dig = candidate.isdigit()
    if dig:
        if int(dig) > 65535 or int(dig) == 0:
            return False
        return True
    else:
        return False

def enter_chat_frame(context):
    wind = context.window

    context.output_message.set("сообщение") # начальное значение, чтобы в окне высветилось и было понятно для чего ввод
    context.my_name.set(["сервер","клиент"][context.is_client_chosen*1])


    clear_widgets(wind.winfo_children() )
    frame = ChatFrame(wind)
    frame.display()
    
    textbox = UI_text(frame)
    textbox.display( [0,0,3] )

    name_entry =  UI_entry(frame, context.my_name)
    
    name_entry.display([1,0,1])

    message_entry = UI_entry(frame, context.output_message)
    message_entry.display([1,1,3])

    send_button = UI_button(frame, "Отправить", send_button_click(textbox, context) )
    send_button.display([2,2,1])

    exit_button = UI_button(frame, "Выход из чата", exit_button_click(context) )
    exit_button.display( [2,0,1] )

    def listen_for_messages():

        while True:

            conn = context.my_sock
            try:
                message = conn.recv(1024)
            except: # закрываемся через ошибку, не хотелось бы
                print( ["Сервер","Клиент"][context.is_client_chosen*1] + " закрывает слушающий поток с ошибками")
                close_connection(context) #не слишком? мало ли почему могло накрыться соединение
                break
            else: 
                if not message: # закрываемся без ошибки
                    context.my_sock.shutdown(SHUT_WR) #чтобы оппонент тоже закрылся аккуратно
                    print("Слушающий поток принял сообщение от собеседника о закрытии потока")
                    print(["Сервер","Клиент"][context.is_client_chosen*1] + " закрывает слушающий поток без ошибок" )
                    close_connection(context)
                    break
                else: # получили сообщение
                    message = message.decode('utf-8')  # расшифровали 
            
            context.input_message.set(message) # перевели в удобный вид
            get_message(textbox, context.input_message) # написали на доске
        

    t = Thread(target=listen_for_messages)
    t.daemon = True # будет выполняться фоном + уничтожится основным потоком 
    t.start()
    context.thread = t


def send_button_click(txtbox, context):
    
    def send():

        date = datetime.datetime.now().strftime('%H:%M:%S') 
        for_send = f"[{date}] {context.my_name.get()}: {context.output_message.get()}"
        if context.is_open:  
            message = bytes( for_send, 'utf-8') # другому - зашифровываем 
            context.my_sock.send(message)# и отправляем
        else:
            context.output_message.set("Никого нет, никто не услышит")   
            txtbox.write( context.output_message )    

        context.output_message.set(for_send) # следующий write сбросит строку, так что пока сохраним строку сюда
        txtbox.write( context.output_message ) # у себя просто пишем

    return send

def get_message(txtbox, message_string):
    
    txtbox.write(message_string)


def exit_button_click(context):
    def exit():
        exit_message(context)
        close_thread(context)
        close_connection(context)   
        enter_settings_frame(context)
    return exit


def exit_message(context):
    if context.is_open:
        print(["Сервер","Клиент"][context.is_client_chosen*1] + " высылает сообщение о закрытии потока")
        date = datetime.datetime.now().strftime('%H:%M:%S') 
        for_send = f"[{date}] Собеседник покинул чат."
        message = bytes( for_send, 'utf-8')
        context.my_sock.send(message)
        
        context.my_sock.shutdown(SHUT_WR) 

def close_thread(context): #тот кто выходит, сам закрывает свой поток. тот кто остается, у него поток тихо-мирно завершается сам
    if context.thread.is_alive(): #true если поток еще слушает. а если он закрыт?
        try:
            print("Закрываю слушающий поток")
            context.thread.join()
        except:
            print("Поток закрыт с ошибками")
        else:
            print("Поток закрыт без ошибок")

def close_connection(context): 
    if context.is_open:
        try: 
            context.my_sock.close()
            context.is_open = False 
        finally:
            context.is_open = False # а если он не закрылся? а если не написать, будет хуже

def clear_widgets( list ):
    # по-другому надо бы
    # чтобы не создавать-удалять а убирать-вытаскивать
    # вроде бы есть forget специально для такого
    for wid in list:
        wid.destroy()

class context_store: #класс контекста, объект которого таскаем по всему ходу программы, храним в нем нужные данные
    #наверное можно и нужно организовать лучше
    #можно вообще глобальным сделать и оно только лучше станет. однозначно не лучшее описание
    def __init__(self, wind):

        self.window = wind  #главное окно 

        self.thread = None # поток, слушающий сообщения. Сохраним здесь, когда откроем

        self.my_sock = None #сокет. сохраним здесь, когда создадим
        self.is_conn_open = False # открываем соединение - true, закрываем - false, сначала закрыто

        self.input_message = tk.StringVar() #строка для входящих сообщений 
        self.output_message = tk.StringVar() #строка для исходящих сообщений

        self.my_name = tk.StringVar() # строка с именем

        self.ip_string = tk.StringVar() # строка с введенным ip-адресом

        self.port_string= tk.StringVar() # строка с введенным портом

        self.is_server_chosen = False  # подлючается ли как сервер
        self.is_client_chosen = False  # подлючается ли как клиент
        self.status = tk.StringVar() # строка об правильности введенных данных и успешности подключения
 
    def choose_server(self): 
        self.is_server_chosen = True
        self.is_client_chosen = False

    def choose_client(self): 
        self.is_server_chosen = False
        self.is_client_chosen = True

    def disconnect(self):
        self.is_server_chosen = False
        self.is_client_chosen = False


main()


