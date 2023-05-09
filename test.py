import utils.baojia as bj

bj_api = bj.Baojia('GtkUuyiFXt8F1j3VZiR3DjL7jHA1KdGmrEN1zBC9fVBT','DZtABEjocvim4QEDswNHoajm85NdqM9AEgbP8RbfA3uv')
bj_api.add_symbol('2330')


def test_print():
    global bj_api
    print(bj_api.symbol_dict['2330'].ticks)

bj_api.symbol_dict['2330'].add_ticks_event(test_print)

input()