from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext
from requests import get
from os import remove
import webbrowser


def dwnld_all_channel():
    url = mp3u_entry.get()
    my_file = get(url)
    open('temp.m3u8', 'wb').write(my_file.content)
    json_list = []
    with open('temp.m3u8', 'r', encoding='utf-8') as f:
        for k in f:
            if '#EXTINF' in k:
                json_list.append(k.split(',')[1].strip())
    json_list.sort()
    n = 1
    for k in json_list:
        all_channels.insert('end', f'{n}.\t{k}\n')
        n += 1
    remove('temp.m3u8')


def convert_playlist():
    url = mp3u_entry.get()
    my_file = get(url)
    open('temp.m3u8', 'wb').write(my_file.content)
    json_list = []
    temp_lst = []
    temp = 0
    group_del_list = []
    num_on_list = []
    with open('temp.m3u8', 'r', encoding='utf-8') as f:
        temp_dict = {}
        for i in f:
            if '#EXTINF' in i:
                temp_dict['tvg-name'] = i.split(',')[1].strip()
                temp_dict['tvg-rec'] = i.split(',')[0][10:]
                temp_dict['tvg-logo'] = 'https://tv.sdckz.com/logo/' + temp_dict['tvg-name'].replace(' ', '') + '.png'
            elif '#EXTGRP' in i:
                temp_dict['group-title'] = i.replace('#EXTGRP:', '').strip()
            elif 'http' in i:
                temp_dict['link'] = i.strip()
                json_list.append(temp_dict)
                temp_dict = {}
    remove('temp.m3u8')
    if group_del_state_1.get():
        group_del_list.append('Новый сайт - edemtv.me')
    if group_del_state_2.get():
        group_del_list.append('новости')
    if group_del_state_3.get():
        group_del_list.append('кино')
    if group_del_state_4.get():
        group_del_list.append('музыка')
    if group_del_state_5.get():
        group_del_list.append('познавательные')
    if group_del_state_6.get():
        group_del_list.append('детские')
    if group_del_state_7.get():
        group_del_list.append('развлекательные')
    if group_del_state_8.get():
        group_del_list.append('другие')
    if group_del_state_9.get():
        group_del_list.append('спорт')
    if group_del_state_10.get():
        group_del_list.append('HD')
    if group_del_state_11.get():
        group_del_list.append('взрослые')
    if group_del_state_12.get():
        group_del_list.append('Հայկական')
    if group_del_state_13.get():
        group_del_list.append('українські')
    if group_del_state_14.get():
        group_del_list.append('USA')
    if group_del_state_15.get():
        group_del_list.append('беларускія')
    if group_del_state_16.get():
        group_del_list.append('azərbaycan')
    if group_del_state_17.get():
        group_del_list.append('ქართული')
    if group_del_state_18.get():
        group_del_list.append('қазақстан')
    if group_del_state_19.get():
        group_del_list.append('точик')
    if group_del_state_20.get():
        group_del_list.append('o\'zbek')
    if group_del_state_21.get():
        group_del_list.append('moldovenească')
    if group_del_state_22.get():
        group_del_list.append('türk')
    if group_del_state_23.get():
        group_del_list.append('ישראלי')
    if group_del_state_24.get():
        group_del_list.append('HD Orig')
    if group_del_state_25.get():
        group_del_list.append('4K')
    with open('temp.m3u8', 'w', encoding='utf-8') as f:
        f.write('#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"\n')
        for d in json_list:
            if d['group-title'] not in group_del_list:
                f.write(
                    f'''#EXTINF:0 group-title="{d['group-title']}" tvg-name="{d['tvg-name']}"\
 tvg-logo="{d['tvg-logo']}" {d['tvg-rec']},{d['tvg-name']}''' + '\n')
                f.write(d['link'] + '\n')
    with open('temp.m3u8', 'r', encoding='utf-8') as f:
        for k in f:
            temp_lst.append(k)
    favorites_list = favorites_channels.get('1.0', END)
    favorites_list = favorites_list.split('\n')
    del favorites_list[-1]

    while temp < len(favorites_list):
        with open('temp.m3u8', 'r', encoding='utf-8') as f:
            for num, val in enumerate(f):
                if favorites_list[temp] in val:
                    num_on_list.append(num)
                    num_on_list.append(num + 1)
            temp += 1
    remove('temp.m3u8')

    finish_fav_list_1 = ['#EXTM3U x-tvg-url="http://epg.it999.ru/epg.xml.gz"\n']
    for k in num_on_list:
        finish_fav_list_1.append(temp_lst[k])

    for k in sorted(num_on_list, reverse=True):
        del temp_lst[k]
    del temp_lst[0]
    finish_fav_list_both = finish_fav_list_1 + temp_lst

    with open('pl.m3u8', 'w', encoding='utf-8') as f:
        for k in finish_fav_list_both:
            f.write(k)


root = Tk()
root.title('IEDEM Converter')
root.resizable(width=False, height=False)

mainframe = ttk.Frame(root, borderwidth=5, width=200, height=100)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
font_bold = font.Font(weight='bold')

ttk.Label(mainframe, text='Введите ссылку на плейлист:', font=font_bold)\
    .grid(column=0, row=0, sticky=W, columnspan=2)

mp3u_entry = ttk.Entry(mainframe, width=98)
mp3u_entry.grid(column=0, row=1, sticky=W, columnspan=6)
mp3u_entry.focus()

ttk.Label(mainframe, text='Выберите группы, которые необходимо исключить:', font=font_bold)\
    .grid(column=0, row=2, sticky=W, columnspan=6)

group_del_state_1 = BooleanVar()
group_del_state_1.set(True)
group_del_1 = ttk.Checkbutton(mainframe, text='Новый сайт - edemtv.me', var=group_del_state_1)\
    .grid(column=0, row=3, sticky=W)

group_del_state_2 = BooleanVar()
group_del_state_2.set(False)
group_del_2 = ttk.Checkbutton(mainframe, text='новости', var=group_del_state_2)\
    .grid(column=0, row=4, sticky=W)

group_del_state_3 = BooleanVar()
group_del_state_3.set(False)
group_del_3 = ttk.Checkbutton(mainframe, text='кино', var=group_del_state_3)\
    .grid(column=0, row=5, sticky=W)

group_del_state_4 = BooleanVar()
group_del_state_4.set(False)
group_del_4 = ttk.Checkbutton(mainframe, text='музыка', var=group_del_state_4)\
    .grid(column=0, row=6, sticky=W)

group_del_state_5 = BooleanVar()
group_del_state_5.set(False)
group_del_5 = ttk.Checkbutton(mainframe, text='познавательные', var=group_del_state_5)\
    .grid(column=0, row=7, sticky=W)

group_del_state_6 = BooleanVar()
group_del_state_6.set(False)
group_del_6 = ttk.Checkbutton(mainframe, text='детские', var=group_del_state_6)\
    .grid(column=0, row=8, sticky=W)

group_del_state_7 = BooleanVar()
group_del_state_7.set(False)
group_del_7 = ttk.Checkbutton(mainframe, text='развлекательные', var=group_del_state_7)\
    .grid(column=0, row=9, sticky=W)

group_del_state_8 = BooleanVar()
group_del_state_8.set(False)
group_del_8 = ttk.Checkbutton(mainframe, text='другие', var=group_del_state_8)\
    .grid(column=1, row=3, sticky=W)

group_del_state_9 = BooleanVar()
group_del_state_9.set(False)
group_del_9 = ttk.Checkbutton(mainframe, text='спорт', var=group_del_state_9)\
    .grid(column=1, row=4, sticky=W)

group_del_state_10 = BooleanVar()
group_del_state_10.set(False)
group_del_10 = ttk.Checkbutton(mainframe, text='HD', var=group_del_state_10)\
    .grid(column=1, row=5, sticky=W)

group_del_state_11 = BooleanVar()
group_del_state_11.set(False)
group_del_11 = ttk.Checkbutton(mainframe, text='взрослые', var=group_del_state_11)\
    .grid(column=1, row=6, sticky=W)

group_del_state_12 = BooleanVar()
group_del_state_12.set(False)
group_del_12 = ttk.Checkbutton(mainframe, text='Հայկական', var=group_del_state_12)\
    .grid(column=1, row=7, sticky=W)

group_del_state_13 = BooleanVar()
group_del_state_13.set(False)
group_del_13 = ttk.Checkbutton(mainframe, text='українські', var=group_del_state_13)\
    .grid(column=1, row=8, sticky=W)

group_del_state_14 = BooleanVar()
group_del_state_14.set(False)
group_del_14 = ttk.Checkbutton(mainframe, text='USA', var=group_del_state_14)\
    .grid(column=1, row=9, sticky=W)

group_del_state_15 = BooleanVar()
group_del_state_15.set(False)
group_del_15 = ttk.Checkbutton(mainframe, text='беларускія', var=group_del_state_15)\
    .grid(column=3, row=3, sticky=W)

group_del_state_16 = BooleanVar()
group_del_state_16.set(False)
group_del_16 = ttk.Checkbutton(mainframe, text='azərbaycan', var=group_del_state_16)\
    .grid(column=3, row=4, sticky=W)

group_del_state_17 = BooleanVar()
group_del_state_17.set(False)
group_del_17 = ttk.Checkbutton(mainframe, text='ქართული', var=group_del_state_17)\
    .grid(column=3, row=5, sticky=W)

group_del_state_18 = BooleanVar()
group_del_state_18.set(False)
group_del_18 = ttk.Checkbutton(mainframe, text='қазақстан', var=group_del_state_18)\
    .grid(column=3, row=6, sticky=W)

group_del_state_19 = BooleanVar()
group_del_state_19.set(False)
group_del_19 = ttk.Checkbutton(mainframe, text='точик', var=group_del_state_19)\
    .grid(column=3, row=7, sticky=W)

group_del_state_20 = BooleanVar()
group_del_state_20.set(False)
group_del_20 = ttk.Checkbutton(mainframe, text='o\'zbek', var=group_del_state_20)\
    .grid(column=3, row=8, sticky=W)

group_del_state_21 = BooleanVar()
group_del_state_21.set(False)
group_del_21 = ttk.Checkbutton(mainframe, text='moldovenească', var=group_del_state_21)\
    .grid(column=3, row=9, sticky=W)

group_del_state_22 = BooleanVar()
group_del_state_22.set(False)
group_del_22 = ttk.Checkbutton(mainframe, text='türk', var=group_del_state_22)\
    .grid(column=4, row=3, sticky=W)

group_del_state_23 = BooleanVar()
group_del_state_23.set(False)
group_del_23 = ttk.Checkbutton(mainframe, text='ישראלי', var=group_del_state_23)\
    .grid(column=4, row=4, sticky=W)

group_del_state_24 = BooleanVar()
group_del_state_24.set(False)
group_del_24 = ttk.Checkbutton(mainframe, text='HD Orig', var=group_del_state_24)\
    .grid(column=4, row=5, sticky=W)

group_del_state_25 = BooleanVar()
group_del_state_25.set(False)
group_del_25 = ttk.Checkbutton(mainframe, text='4K', var=group_del_state_25)\
    .grid(column=4, row=6, sticky=W)

ttk.Label(mainframe, text='Все каналы:', font=font_bold)\
    .grid(column=0, row=10, sticky=W)
ttk.Label(mainframe, text='Избранные каналы:', font=font_bold)\
    .grid(column=3, row=10, sticky=W)

all_channels = scrolledtext.ScrolledText(mainframe, width=33, height=15)
all_channels.grid(column=0, row=11, columnspan=3)

favorites_channels = scrolledtext.ScrolledText(mainframe, width=33, height=15)
favorites_channels.grid(column=3, row=11, columnspan=3)


ttk.Button(mainframe, text="Загрузить", command=dwnld_all_channel)\
    .grid(column=1, row=10, sticky=W)

ttk.Button(mainframe, text='КОНВЕНТИРОВАТЬ!', command=convert_playlist)\
    .grid(column=0, row=12, sticky=(W, E), columnspan=6)


author = ttk.Label(mainframe, text='daradan')
author.grid(column=5, row=13, sticky=E)
author.bind('<Button-1>', lambda event: webbrowser.open("https://github.com/daradan?tab=repositories"))

donate = ttk.Label(mainframe, text='donate')
donate.grid(column=0, row=13, sticky=W)
donate.bind('<Button-1>', lambda event: webbrowser.open("https://www.paypal.me/daradan?locale.x=ru_RU"))

version = ttk.Label(mainframe, text='v0.1(20200620)')
version.grid(column=3, row=13, sticky=(W, E))


for child in mainframe.winfo_children():
    child.grid_configure(padx=0, pady=2)

root.mainloop()
