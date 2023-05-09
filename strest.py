from distutils.command.build import build
import tkinter as tk
import os
import utils.baojia as bj
import json 

#frame_status??

class MainApp():
    def __init__(self):
        self.strategy_headline = ['啟動','策略名稱','最大金額','槓桿比率','商品數','持倉金額','損益']
        self.app = tk.Tk()
        self.bj_api = bj.Baojia('GtkUuyiFXt8F1j3VZiR3DjL7jHA1KdGmrEN1zBC9fVBT','DZtABEjocvim4QEDswNHoajm85NdqM9AEgbP8RbfA3uv')
        self.frame_strategy = tk.Frame(self.app)
        self.frame_strategy.grid(column = 0, row = 0,sticky='n')    
        self.build_headline()
        self.frame_symbol = tk.Frame(self.app)
        self.frame_symbol.grid(column = 1, row = 0, sticky = tk.N)
        self.frame_status = tk.Frame(self.app)
        self.frame_status.grid(column = 0, row = 1, columnspan = 2)
        self.strategy_pos = 1
        self.strategy_dict = {}
        self.strategy_info_dict = {}
        self.strategy_info = {}
        self.strategies_settings = {}
        self.read_strategy()
        self.read_strategy_info()
        self.signal_output()
        self.subscribe_symbols()
        self.initial_ui = {
           '商品':{},
           '部位':{},
           '庫存':{},
           '目標庫存':{},
           '未實現':{},
           '今日已實現':{},
           '進場時間':{},
           '出場時間':{},
           '模式':{},
           '狀態':{},
           '現價':{}
           }
        self.ui_headline_dict:dict[str,tk.Label] = {}   
        self.build_uiheadline()
        self.symbol_list = SymbolList(self)  
        self.symbol_list.add_symbol(list(self.strategies_settings.keys())[0])
        # print(list(self.strategies_settings.keys())[0])
        
        
        
    def build_uiheadline(self):
        for x,i in enumerate(self.initial_ui):
            self.ui_headline_dict[i] = tk.Label(self.frame_symbol,text = i, width =(None,10)[x==10])
            self.ui_headline_dict[i].grid(column=x ,row=0,sticky = tk.N)
        
    def read_strategy(self):
        self.strategies = os.listdir('strategies/stock_picking')
        # self.strategies_settings = {}
        for i in self.strategies:
            with open('strategies/stock_picking/'+i,'r+') as f:
                rl = f.readlines()
            # print(rl)
            rl = {i.split(' ')[0]:[j.rstrip() for j in i.split(' ')] for i in rl}
            # print(rl)
            self.strategies_settings[i.replace('.txt','')] = rl
            
        for i in self.strategies_settings:
            self.strategy_dict[i]=Strategy_info(self,i[0:15],'500','0.9',self.strategies_settings[i],'stock_picking')   
#         print(self.strategies_settings)
        
    def build_headline(self):
        self.headline_list = [tk.Label(self.frame_strategy, text = i) for i in self.strategy_headline]
        for x,i in enumerate(self.headline_list):
            i.grid(column = x,row = 0)  #,ipadx=5
    def add_strategy(self,strategy_name):
        pass

    def subscribe_symbols(self):
        for i in self.strategies_settings:
            for j in self.strategies_settings[i]:
                self.bj_api.add_symbol(j)
    
    def read_strategy_info(self):
        with open('strategy_info/strategy_info.json') as f:
            self.strategy_info = json.load(f)
        print(self.strategy_info)
        # print(self.strategies_settings)
        
    def signal_output(self):
        for i in self.strategy_info:
            print(self.strategy_info[i])
        for i in self.strategies_settings:
            print(self.strategies_settings[i])


    def run(self):
        self.app.mainloop()

class Strategy_info():
    def __init__(self,parent:MainApp,
                 strategy_name,
                 max_amount,  
                 leverage,
                 strategy_info,
                 strategy_type
                ):
        self.parent = parent
        self.strategy_info = strategy_info  
        self.strategy_name = strategy_name
        self.headline_list = self.parent.strategy_headline  
        self.act_dict = {
            'btn': self.build_button,
            'lab': self.build_label
        }
        self.dict = {
            '啟動':{'type':'btn','text':'啟動','command':None,'x':0,'y':0},
            '策略名稱': {'type':'btn','text':strategy_name,'command':self.test,'x':1,'y':0,'w':20},
            '最大金額': {'type':'lab','text':max_amount,'command':None,'x':2,'y':0 },
            '槓桿比率': {'type':'lab','text':leverage,'command':None,'x':3,'y':0 },
            '商品數': {'type':'lab','text':len(self.strategy_info),'command':None,'x':4,'y':0 },
            '持倉金額': {'type':'lab','text':'0','command':None,'x':5,'y':0},
            '損益':  {'type':'lab','text':'0','command':None,'x':6,'y':0 },
        }
        self.build_info()
        
    def build_info(self):
        self.build_dict = {}
        for i in self.dict:
            info = self.dict[i]  
            if not 'w' in info:
                info['w'] = None  
            self.build_dict[i] = self.act_dict[info['type']](info['text'],info['command'],width = info['w'])                                
            self.build_dict[i].grid(column = info['x'],row = info['y']+self.parent.strategy_pos,sticky = tk.W)
        self.parent.strategy_pos += 1
            
    def build_button(self,btn_name,command=None,width=None):
        return tk.Button(self.parent.frame_strategy,text = btn_name ,width = width,command = command,anchor='w')
    
    def build_label(self,lab_name,command=None,width=None):
        return tk.Label(self.parent.frame_strategy,text = lab_name,width = width)
    
    def test(self):
        self.parent.symbol_list.add_symbol(self.strategy_name)
        
class SymbolList():
    def __init__(self,parent):
        self.info_dict = {}
        self.parent:MainApp = parent
        self.info_component = {}
        self.input_symbol(self.parent.strategies_settings)
        #self.show_symbol_info()
        self.ui_info_list = {}

    def input_symbol(self,symbol_dict):
        self.info_dict = symbol_dict
#         print(self.info_dict)
        self.info_component
        
    def add_symbol(self,strategies):
        # print(self.ui_info_list)
        for i in self.ui_info_list:
            # print(i)
            self.ui_info_list[i].symbol_code.grid_forget()
            self.ui_info_list[i].tick_price.grid_forget()
        self.ui_info_list:dict[str,StrategySymboInfo] = {}
        
        for i in self.parent.strategies_settings[strategies]:
            if not i in self.ui_info_list:
                self.ui_info_list[i] = StrategySymboInfo(self.parent,strategies,i)
                self.parent.bj_api.symbol_dict[i].add_ticks_event(self.ui_info_list[i].update_price)

class StrategySymboInfo():
    def __init__(self,mnapp,strategy,symbol):
        self.mnapp:MainApp = mnapp
        self.strategy = strategy
        self.symbol = symbol
        self.make_labels(self.mnapp.bj_api.symbol_dict[self.symbol].activate) 

    def make_labels(self,if_activate):

        if if_activate:
            self.snapshots = self.mnapp.bj_api.symbol_dict[self.symbol].snapshot
            fg = 'black'
        else :
            self.snapshots = SymbolError()
            self.snapshots.close = 'ERROR'
            self.update_price = self.do_nothing
            fg = 'red'
        self.symbol_code = tk.Label(master=self.mnapp.frame_symbol,text = self.symbol, fg = fg)
        self.symbol_code.grid(column=0, row = len(self.mnapp.symbol_list.ui_info_list)+1)
        self.tick_price = tk.Label(master=self.mnapp.frame_symbol, text = self.snapshots.close, fg = fg)
        self.tick_price.grid(column=10 ,row= len(self.mnapp.symbol_list.ui_info_list)+1)

    def update_price(self):
        self.tick_price['text'] = str(float(self.mnapp.bj_api.symbol_dict[self.symbol].ticks.close))

    def do_nothing(self):
        pass

class SymbolError():
    def __init__(self):
        self.error = True

class SymbolPosition():
    def __init__(self,parent,strategy,symbol,position=0,filled=0,average_cost=0):
        self.strategy = strategy
        self.symbol = symbol
        self.position = position
        self.filled = filled
        self.average_cost = average_cost
        self.ui_head_line = 0

    def makeInfoUI(self):
        pass


window = MainApp()
window.run()