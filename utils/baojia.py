import typing
import shiopyaji as sj
from shioaji import contracts as sjContracts
from shioaji import BidAskSTKv1,TickSTKv1, Exchange


class Baojia():
    def __init__(self,api_key,sec_key):
        self.api = sj.Shioaji()
        self.api_key = api_key
        self.sec_key = sec_key
        self.login()
        self.symbol_dict:dict[str,Symbol] = {}


        @self.api.on_tick_stk_v1()
        def quote_callback(exchange: Exchange, tick:TickSTKv1):
            if tick.simtrade == 0 :
                self.symbol_dict[tick.code].ticks = tick
                self.symbol_dict[tick.code].run_all_tickevents()
            
        @self.api.on_bidask_stk_v1()
        def quote_callback(exchange: Exchange, bidask:BidAskSTKv1):
            self.symbol_dict[bidask.code].bidask = bidask

    def login(self):
        self.api.login(self.api_key,self.sec_key)

    def add_symbol(self,symbol_code):
        code = str(symbol_code).split('.')[0]
        if code in self.symbol_dict:
            return
        self.symbol_dict[code] = Symbol(self,code)

    
class Symbol():
    def __init__(self,bj:Baojia,symbol_code) -> None:
        self.symbol_code = str(symbol_code).split('.')[0]
        self.baojia = bj
        self.activate = False
        self.contract = None
        self.snapshot = None
        self.ticks = None
        self.bidask = None
        self.tick_events = []
        print()
        if self.baojia.api.Contracts.Stocks[self.symbol_code] != None:
            self.contract = self.baojia.api.Contracts.Stocks[self.symbol_code]
            self.snapshot = self.baojia.api.snapshots([self.contract])[0]
            self.subscribe_bidask()
            self.subscribe_ticks()
            self.activate = True

    def subscribe_ticks(self):
        self.baojia.api.quote.subscribe(
            self.contract,
            quote_type = sj.constant.QuoteType.Tick,
            version = sj.constant.QuoteVersion.v1
        )
    
    def subscribe_bidask(self):
        self.baojia.api.quote.subscribe(
            self.contract,
            quote_type = sj.constant.QuoteType.BidAsk,
            version = sj.constant.QuoteVersion.v1
        )

    def add_ticks_event(self,func):
        self.tick_events.append(func)

    def run_all_tickevents(self):
        for i in self.tick_events:
            i()
