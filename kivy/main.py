from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.network.urlrequest import UrlRequest
from socket import *
import threading
import time

class ClientApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.tcpClicSock = None
        self.ip_stu = 1
        self.stop_stu = 1
        
        self.ip_input = TextInput(hint_text='Enter IP Address')
        self.add_widget(self.ip_input)
        
        self.status_label = Label(text='Disconnected', size_hint_y=None, height=40)
        self.add_widget(self.status_label)
        
        self.connect_btn = Button(text='Connect')
        self.connect_btn.bind(on_press=self.connect_click)
        self.add_widget(self.connect_btn)
        
        self.forward_btn = Button(text='Forward')
        self.forward_btn.bind(on_press=self.call_forward)
        self.forward_btn.bind(on_release=self.call_stop)
        self.add_widget(self.forward_btn)
        
        self.backward_btn = Button(text='Backward')
        self.backward_btn.bind(on_press=self.call_back)
        self.backward_btn.bind(on_release=self.call_stop)
        self.add_widget(self.backward_btn)
        
        self.left_btn = Button(text='Left')
        self.left_btn.bind(on_press=self.call_left)
        self.left_btn.bind(on_release=self.call_stop)
        self.add_widget(self.left_btn)
        
        self.right_btn = Button(text='Right')
        self.right_btn.bind(on_press=self.call_right)
        self.right_btn.bind(on_release=self.call_stop)
        self.add_widget(self.right_btn)

    def connect_click(self, instance):
        if self.ip_stu == 1:
            threading.Thread(target=self.socket_connect, daemon=True).start()
    
    def socket_connect(self):
        print("socket_connect")
        ip_adr = self.ip_input.text.strip()
        print(ip_adr)
        if not ip_adr:
            self.status_label.text = 'Invalid IP'
            return
        
        SERVER_IP = ip_adr
        SERVER_PORT = 333
        BUFSIZ = 1024
        ADDR = (SERVER_IP, SERVER_PORT)
        
        self.tcpClicSock = socket(AF_INET, SOCK_STREAM)
        print("debug")
        try:
            print("connected")
            self.tcpClicSock.connect(ADDR)
            self.status_label.text = f'Connected to {SERVER_IP}'
            self.ip_stu = 0
        except Exception as e:
            print("not connected")
            self.status_label.text = 'Connection Failed'
            print(e)
    
    def call_forward(self, instance):
        if self.stop_stu and self.tcpClicSock:
            self.tcpClicSock.send(('1').encode())
            self.stop_stu = 0
    
    def call_back(self, instance):
        if self.stop_stu and self.tcpClicSock:
            self.tcpClicSock.send(('2').encode())
            self.stop_stu = 0
    
    def call_left(self, instance):
        if self.stop_stu and self.tcpClicSock:
            self.tcpClicSock.send(('4').encode())
            self.stop_stu = 0
    
    def call_right(self, instance):
        if self.stop_stu and self.tcpClicSock:
            self.tcpClicSock.send(('3').encode())
            self.stop_stu = 0
    
    def call_stop(self, instance):
        if self.tcpClicSock:
            self.tcpClicSock.send(('9').encode())
        self.stop_stu = 1
    
class MyApp(App):
    def build(self):
        return ClientApp()

if __name__ == '__main__':
    MyApp().run()

