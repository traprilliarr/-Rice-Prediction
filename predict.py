import customtkinter
import os
from PIL import Image
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import END
import customtkinter
import math
import random
import copy
import xlsxwriter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox

from tkinter import filedialog

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Rice Prediction")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Dataset",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Hasil & Visualisasi",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
   
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self.home_frame, placeholder_text="Pilih file...")
        self.entry.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        
        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Pilih Excel",  compound="right", command=self.select_file)
        self.home_frame_button_1.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.home_frame, dynamic_resizing=False,
                                                        values=["FTS", "FTS + EHO"], command=self.getinputmetode)
        self.optionmenu_1.grid(row=2, column=3, padx=20, pady=(20, 10))

        self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="Jalankan Program!", command=self.execute_next_functions)
        self.home_frame_button_2.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # create second frame
        self.second_frame = customtkinter.CTkTextbox(self, corner_radius=0, fg_color="transparent")
        # create textbox
        self.second_frame_text = customtkinter.CTkTextbox(self.second_frame)
        self.second_frame_text.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        

        self.third_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        

        self.canvas = tk.Canvas(self.third_frame, width=800, height=600, bg="white")
        self.canvas.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.canvas.pack()

        self.table = ttk.Treeview(self.third_frame, columns=('tahun','dataset', 'prediksi', 'galat','mape'), show='headings')
        self.table.heading('tahun', text='Tahun')
        self.table.heading('dataset', text='Dataset')
        self.table.heading('prediksi', text='Prediksi')
        self.table.heading('galat', text='Galat')
        self.table.heading('mape', text='Mape')
        self.table.pack()
        
    
        # select default frame
        self.select_frame_by_name("home")


        #set default values:
        
        self.optionmenu_1.set("Pilih Metode")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            df = pd.read_excel(file_path)
            self.dataset = df
            self.display_table(df)

            self.entry.delete(0, "end")
            self.entry.insert(0, file_path)

    def display_table(self, df):
        self.second_frame_text.delete("1.0", "end")

        # Set the column spacing value
        column_spacing = 10

        # Get the header and format it with column spacing
        header = " ".join(str(col).ljust(column_spacing) for col in df.columns) + "\n"

        # Format the DataFrame rows with column spacing
        formatted_data = header
        for _, row in df.iterrows():
            formatted_row = " ".join(str(val).ljust(column_spacing) for val in row) + "\n"
            formatted_data += formatted_row

        # Insert the formatted data into the text widget
        self.second_frame_text.insert("1.0", formatted_data)

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

   
    def execute_next_functions(self):
        if not hasattr(self, 'dataset'):
            text = "Tidak ada data terpilih!"
            messagebox.showinfo("Popup", text)
            return
       
        
        dataset = self.dataset
        
        
        if hasattr(self, 'entry2') and self.entry2.get().isdigit():
            self.nClan = int(self.entry2.get())
        else:
            self.nClan = 2
            
        if hasattr(self, 'entry3') and self.entry3.get().isdigit():
            print(":this", self.entry3.get())
            user_input = int(self.entry3.get())
            if user_input % 2 == 0:
                self.nGajah  = user_input
            else:
                text = "Nilai Gajah harus genap!"
                messagebox.showinfo("Popup", text)
                return
        else:
            self.nGajah = 2

        print("user input", self.nClan,self.nGajah)
        
        
        if  hasattr(self, 'plot') and self.canvas is not None:
            self.canvas.destroy()

            self.canvas = tk.Canvas(self.third_frame, width=800, height=600, bg="white")
            self.canvas.pack()
            
        if hasattr(self, 'table') and self.table is not None:
            self.table.destroy()
            self.table = ttk.Treeview(self.third_frame, columns=('tahun','dataset', 'prediksi', 'galat','mape'), show='headings')
            self.table.heading('tahun', text='Tahun')
            self.table.heading('dataset', text='Dataset')
            self.table.heading('prediksi', text='Prediksi')
            self.table.heading('galat', text='Galat')
            self.table.heading('mape', text='Mape')
            self.table.pack()

        # if hasattr(self, 'opsi_param'):
           
        if hasattr(self, 'opsi_param'):
            if self.opsi_param == 'FTS':
                self.param_fts(self.dataset)

                # Extract galat values from fts and eho dictionaries
                fts_galat = self.fts['galat'][0][1:]

                # Create the figure and subplot
                num_data_points = len(fts_galat) 
                figsize = (num_data_points * 0.8, 6)
                fig = plt.Figure(figsize=figsize, dpi=100)
                plot = fig.add_subplot(111)

                # Plot fts galat values
                plot.plot(range(len(fts_galat)), fts_galat, label='fts', color='red', marker='o')

               
                plot.set_title('Nilai Galat FTS', fontsize=14)
                plot.set_xlabel('Index', fontsize=14)
                plot.set_ylabel('Galat', fontsize=14)
                plot.grid(True)
                plot.legend()

                # Convert the figure to a Tkinter-compatible format
                canvas = FigureCanvasTkAgg(fig, master=self.canvas)
                canvas.draw()

                # Display the figure in the canvas
                canvas.get_tk_widget().pack()

            if self.opsi_param == 'FTS + EHO':
                self.param_eho(self.dataset)
            
        else:
            text = "Pilih Metode terlebih dahulu!"
            messagebox.showinfo("Popup", text)
            return
            
        text = "Penghitungan selesai!"
        messagebox.showinfo("Popup", text)

    def getinputmetode(self, param):
        self.opsi_param = param
        
        if hasattr(self, 'opsi_param'):
            if self.opsi_param == 'FTS':
                if hasattr(self, 'entry2') and hasattr(self, 'entry3'):
                    self.entry2.destroy()
                    self.entry3.destroy()
                
            if self.opsi_param == 'FTS + EHO':
                self.entry2 = customtkinter.CTkEntry(self.home_frame, placeholder_text="input Jumlah Clan")
                self.entry2.grid(row=2, column=1,  padx=(20, 0), pady=(20, 20), sticky="nsew")
                self.entry3 = customtkinter.CTkEntry(self.home_frame, placeholder_text="Input Jumlah Gajah")
                self.entry3.grid(row=2, column=2,  padx=(20, 0), pady=(20, 20), sticky="nsew")
    
    def calculate_values(self, df):
        if isinstance(df, list):
            df = df
        else:
            df = df.iloc[:, 1].tolist()
        Dmin = min(df)
        Dmax = max(df)
        D1 = Dmin - math.floor(Dmin)
        D2 = math.ceil(Dmax) - Dmax
        self.U1 = math.floor(Dmin)
        self.U2 = math.ceil(Dmax)

        row_length = len(df)
        self.n_interval = math.ceil(1 + 3.33 * math.log10(row_length))
        self.interval = (self.U2 - self.U1) / self.n_interval
        print("values calc", Dmin, Dmax, D1, D2, self.U1,self.U2, self.n_interval, self.interval)    
        
    def partisi_u(self, df):
        u_interval = self.n_interval
        interval = self.interval

        self.ulow = [self.U1]
        self.uhi = [self.U1 + interval]
        self.umid = [0.5 * (self.ulow[0] + self.uhi[0])]
        
        for i in range(1, u_interval):
            self.ulow.append(self.uhi[i-1])
            self.uhi.append(self.ulow[i] + interval)
            self.umid.append(0.5 * (self.ulow[i] + self.uhi[i]))

    def fuzifikasi(self, df):
        if isinstance(df, list):
            df = df
        else:
            df = df.iloc[:, 1].tolist()
        lenlist = len(df)
        ceklenu = len(self.ulow)
        self.fuzzy = []

        
        for index, value in enumerate(df):
            fuzzy_value = None
            
            for k in range(1, ceklenu + 1):
                if value <= self.uhi[k-1] and value >= self.ulow[k-1]:
                    fuzzy_value = 'A{}'.format(k)
                    self.fuzzy.append(fuzzy_value)
                
        print(self.fuzzy)
        lenfuzzy = len(self.fuzzy)   
        print("inilenfuzy", lenfuzzy)
        self.prevfuzzy = []         
        for l in range(lenfuzzy):
            if l == 0:
                self.prevfuzzy.append(None)
            else:
                prevfuzzy_val = self.fuzzy[l-1]
                self.prevfuzzy.append(prevfuzzy_val)
    
    
    def flrg(self,df):
        nlist = self.n_interval
        list1 = self.prevfuzzy
        list2 = self.fuzzy

        lists = {}

        for i in range(1, nlist + 1):
            list_name = 'A{}'.format(i)
            lists[list_name] = []

        for i in range(1, nlist + 1): 
            for j in range(1, len(list1) + 1): 
                if list1[j-1] == 'A{}'.format(i): 
                    for k in range(1, nlist + 1):   
                        if list2[j-1] == 'A{}'.format(k): 
                            lists['A{}'.format(i)].append('A{}'.format(k)) 
        
        self.defuzifikasi = []
        for l in range(1, nlist + 1):
            index = 'A{}'.format(l)
            lenlista = len(lists[index])
            count = 0

            if lenlista > 0:
                for m in range(lenlista):
                    val = lists[index][m]
                    if val is not None:
                        number_value = int(val[1:])
                    else:
                        number_value = l
                    count = count + self.umid[number_value-1]

                self.defuzifikasi.append(count / lenlista)  
            else:
                self.defuzifikasi.append(self.umid[l-1])

    def forecast(self,df):
        self.prediksi = []
        lenprev = len(self.prevfuzzy)
        print("ini lenprev",lenprev)
        for l in range(1, lenprev + 1): 
            lenlista = len(self.prevfuzzy)
            
            val = self.prevfuzzy[l-1]
            if val == None:
                self.prediksi.append(None)
            else:
                number_value = int(val[1:]) 
                count = self.defuzifikasi[number_value-1]
                self.prediksi.append(count)

    def error(self,df):
        self.galat=[]
        if isinstance(df, list):
            df = df
        else:
            df = df.iloc[:, 1].tolist()
        # error = ( prediksi(n) - df(n-1) )/ df(n-1)

        # iter dari prediksi
        lenpred = len(df)
        print("lenprednya",lenpred)
        print("preadnya",len(self.prediksi))
        for i in range(lenpred):
            hitung = 0
            if self.prediksi[i] is None:
                self.galat.append(None)
            else:
                hitung = abs((self.prediksi[i] - df[i]) / df[i])
                self.galat.append(hitung)
        count = sum(1 for element in self.galat if element is not None)
        total = sum(element for element in self.galat if element is not None)
        if count != 0 or total != 0:
            self.mape =  abs (100/count*total)

    def param_fts(self,df):
        if isinstance(df, list):
            df = df
        else:
            df = df.iloc[:, 1].tolist()

        self.calculate_values(df)
        self.partisi_u(df)
        self.fuzifikasi(df)
        self.flrg(df)
        self.forecast(df)
        self.error(df)
       
        if self.opsi_param == 'FTS':
            self.fts = {}
            eho = {}
            if 'dataset' not in self.fts:
                self.fts['dataset'] = []
            if 'prediksi' not in self.fts:
                self.fts['prediksi'] = []
            if 'galat' not in self.fts:
                self.fts['galat'] = []
            if 'mape' not in self.fts:
                self.fts['mape'] = []
            self.fts['dataset'].append(df)
            self.fts['prediksi'].append(self.prediksi)
            self.fts['galat'].append(self.galat)
            self.fts['mape'].append(self.mape)


            style = ttk.Style()

            style.configure("Treeview",
                            rowheight=30,       
                            font=('Arial', 12)
                            )
            
            tahun = self.dataset.iloc[:, 0].tolist()
            dataset = self.fts['dataset'][0]
            prediksi = self.fts['prediksi'][0]
            galat = self.fts['galat'][0]
            mape = self.fts['mape'][0]

            print("initahun", tahun)
            print(dataset)
            print(prediksi)
            print(galat)
            print(mape)

            for i, (tahun, data, pred, gal) in enumerate(zip(tahun, dataset, prediksi, galat)):
                values = (
                    tahun if tahun is not None else "",
                    "{:.2f}".format(float(data)) if data is not None else "",
                    "{:.2f}".format(pred) if pred is not None else "",
                    "{:.5f}".format(gal) if gal is not None else "",
                )
                if i == 0:
                    values += ("{:.5f}".format(mape),)
                else:
                    values += ("",)
                self.table.insert(parent='', index=END, values=values)
         
    def param_eho(self,df):
        fts = {}
        eho = {}
        if 'dataset' not in fts:
            fts['dataset'] = []
        if 'prediksi' not in fts:
            fts['prediksi'] = []
        if 'galat' not in fts:
            fts['galat'] = []
        if 'mape' not in fts:
            fts['mape'] = []

        if 'dataset' not in eho:
            eho['dataset'] = []
        if 'prediksi' not in eho:
            eho['prediksi'] = [] 
        if 'galat' not in eho:
            eho['galat'] = []
        if 'mape' not in eho:
            eho['mape'] = []


        # lakukan fts
        self.param_fts(df)
        datasave = df.iloc[:, 1].tolist()
        fts['dataset'].append(datasave)
        fts['prediksi'].append(self.prediksi)
        fts['galat'].append(self.galat)
        fts['mape'].append(self.mape)

        alpa = 0.5 
        beta = 1
        
        nDimensi = self.n_interval - 1
        nlist = self.nClan * self.nGajah 
        print("iniloh",nlist)
        print("iniloh",self.nGajah)
        print("iniloh",self.nClan)
        lists = {}
        center_lists = {}
        old_lists = {}
        fitness_lists = {}
        # mape_lists = {}

        #buat list sebanyak nlist
        for i in range(1, nlist + 1): #total list
            for j in range(1, self.nClan + 1 ): #total clan
                for k in range(1, self.nGajah + 1): #total gajah
                    list_name = 'clan{}_gajah{}'.format(j,k)
                    lists[list_name] = []

        #buat fitneass masing2 list
        for l in range(1, nlist + 1):
            for m in range(1, self.nClan + 1):
                for n in range(1, self.nGajah + 1):
                    list_name = 'fitness_clan{}_gajah{}'.format(m, n)
                    fitness_lists[list_name] = []   

        n = nDimensi 
        a = self.U1  
        b = self.U2

        # Append random numbers to each list
        for key in lists:
            for i in range(n):
                random_number = random.uniform(a, b)
                lists[key].append(random_number)

        #inisialisasi
        #lakukan fts untuk tiap gajah
        list_of_names = list(lists.keys())
        
        for o in range(1, nlist + 1):
                    
            df = list(lists.values())[o-1]
            self.param_fts(df)
            print("fts init",o)
            name = "fitness_"+list_of_names[o-1]
            ##print(name)
            fitness_lists[name].append(self.mape)

        old_fitness_lists = copy.deepcopy(fitness_lists)
        old_lists = copy.deepcopy(lists)
        #ambil best fitness masing2 clan
        # initlist = fitness_lists
        max_values = {}
        for key, value in fitness_lists.items():
            max_value = min(value)
            max_values[key] = max_value

        max_results = {}
        for key in max_values.keys():
            prefix = key.split('clan')[1].split('_')[0]
            if prefix not in max_results:
                max_results[prefix] = (key, max_values[key])
            else:
                if max_values[key] > max_results[prefix][1]:
                    max_results[prefix] = (key, max_values[key])
        print("here")
        print(fitness_lists)
        print(max_results)
        #clan updating
        #cari center masing2 clan
        center_lists = {}

        #mencari nilai center
        for i in range(1, self.nClan + 1):
            clan_key = 'clan{}'.format(i)
            clan_values = []
            for j in range(self.nGajah):
                gajah_key = '{}_gajah{}'.format(clan_key, j + 1)
                clan_values.append(old_lists[gajah_key])
            clan_avg = [sum(elements) / self.nGajah for elements in zip(*clan_values)]
            center_lists[clan_key] = clan_avg

        # mengalikan center dengan beta
        for key in center_lists:
            center_lists[key] = [beta * value for value in center_lists[key]]

        # mengganti nilai best fitness
        for prefix, (list_name, max_value) in max_results.items():
            ##print(f"Max value of clan{prefix}: {list_name} which is {max_value}")
            #buang 
            part_to_remove = 'fitness_'
            result = list_name.replace(part_to_remove, '')
            # ##print(result) 
            lists[result].clear()

            print(lists)
            #insert data baru
            clan_value = center_lists[result.split('_')[0]].copy()
            lists[result] = clan_value
        print(old_lists)
        #mengganti nilai gajah lainnya
        unchanged_lists = []

        for key, value in lists.items():
            if value != center_lists[key.split('_')[0]]:
                unchanged_lists.append(key)

        ##print("Unchanged list_name:")
        for list_name in unchanged_lists:
            lists[list_name].clear()
            ##print(list_name)

        #membuat nilai baru untuk gajah lainnya
        # import random

        # Iterate over the unchanged lists
        for list_name, old_values in old_lists.items():
            if list_name  in unchanged_lists:
                # Extract clan and gajah names from list_name
                clan_name, gajah_name = list_name.split('_')

                # Get the values of the other gajah in the same clan
                other_gajah_name = [name for name in old_lists.keys() if name != list_name and name.startswith(clan_name)][0]
                other_gajah_values = old_lists[other_gajah_name]

                # Perform the calculation for each value in the unchanged list
                new_values = []
                for i in range(len(old_values)):
                    value = old_values[i]
                    other_value = other_gajah_values[i]
                    random_number = random.uniform(0, 1)
                    new_value = value + alpa * (value - other_value) * random_number
                    new_values.append(new_value)

                # Update the list in the 'lists' dictionary with the new values
                lists[list_name] = new_values


        print('untuk cek list sebelum diganti', lists)
        #lakukan fts untuk tiap gajah
        list_of_names = list(lists.keys())
        
        print(lists)
        for o in range(1, nlist + 1):       
            df = list(lists.values())[o-1]
            print(len(df))
            print("fts updating",o)
            self.param_fts(df)
            name = "fitness_"+list_of_names[o-1]
            ##print(name)
            #print(fitness_lists[name])
            fitness_lists[name].clear()
            fitness_lists[name].append(self.mape)
            #print(fitness_lists[name])
            #total list
        #print(fitness_lists)        
                    
        # cari fitness worst
        #ambil worst fitness masing2 clan
        # initlist = fitness_lists
        min_values = {}
        for key, value in fitness_lists.items():
            min_value = min(value)
            min_values[key] = min_value

        min_results = {}
        for key in min_values.keys():
            prefix = key.split('clan')[1].split('_')[0]
            if prefix not in min_results:
                min_results[prefix] = (key, min_values[key])
            else:
                if min_values[key] > min_results[prefix][1]:
                    min_results[prefix] = (key, min_values[key])
                    
        
        #clan separate

        #buang value worst ganti dengan data baru
        for key in min_results:
            value = min_results[key][0]
            value = value.replace('fitness_', '')
            lists[value].clear()
            #insert data baru
            for i in range(nDimensi):
                random_number = random.uniform(0, 1)
                new_value = self.U1 + ( self.U2 - self.U1 + 1) * random_number
                # =ROUNDUP(46 + (52-46+1)*W27;2)
                lists[value].append(new_value)

        print(fitness_lists)
        print(min_results)
        print(lists)

        #lakukan fts untuk tiap gajah
        list_of_names = list(lists.keys())
        
        #print(lists)
        for o in range(1, nlist + 1):       
            df = list(lists.values())[o-1]
            self.param_fts(df)
            name = "fitness_"+list_of_names[o-1]
            ##print(name)
            #print(fitness_lists[name])
            fitness_lists[name].clear()
            fitness_lists[name].append(self.mape)
        print("cek fitness baru", fitness_lists)
        print("fitness lama", old_fitness_lists)
        #clan merge
        # membandingkan mape
        
        # Get the minimum value and corresponding key in fitness lama
        min_lama_key = min(old_fitness_lists, key=lambda k: old_fitness_lists[k][0])
        min_lama_value = old_fitness_lists[min_lama_key][0]

        # Get the minimum value and corresponding key in fitness baru
        min_baru_key = min(fitness_lists, key=lambda k: fitness_lists[k][0])
        min_baru_value = fitness_lists[min_baru_key][0]

        # Compare the minimum values and retrieve the corresponding key-value pair
        if min_lama_value < min_baru_value:
            min_key = min_lama_key
            min_value = min_lama_value
            min_source = "old_fitness_lists"
            min_lama_key = min_lama_key.replace('fitness_', '')
            df = old_lists[min_lama_key]
        else:
            min_key = min_baru_key
            min_value = min_baru_value
            min_source = "fitness_lists"
            min_lama_key = min_lama_key.replace('fitness_', '')
            df = lists[min_lama_key]

        newdf = df
        # self.param_fts(df)
        df = self.dataset.iloc[:, 1].tolist()
        self.calculate_values(df)

        self.ulow.clear()
        self.ulow.append(self.U1)
        self.ulow.extend(newdf)

        self.uhi.clear()
        self.uhi.extend(newdf)
        self.uhi.append(self.U2)

        self.umid.clear()
        for i in range(1, self.n_interval + 1):
            self.umid.append(0.5 * (self.ulow[i-1] + self.uhi[i-1]))
        print("nilai uhi",self.uhi)
        print("nilai ulow", self.ulow)
        print("nilai ulow", self.umid)

       
        self.fuzifikasi(df)
        self.flrg(df)
        self.forecast(df)
        print("dfnya",df)
        print("preadiksinya",self.prediksi)
        print(df)
        self.error(df)
        eho['dataset'].append(df)
        eho['prediksi'].append(self.prediksi)
        eho['galat'].append(self.galat)
        eho['mape'].append(self.mape)

        print("Minimum value:")
        print("Key:", min_key)
        print("Value:", min_value)
        print("Source:", min_source)
    
        data1=fts
        data2 = eho
        
        print(fts)
        print(eho)
        
        # Extract galat values from fts and eho dictionaries
        fts_galat = fts['galat'][0][1:]
        eho_galat = eho['galat'][0][1:]

        # Create the figure and subplot
        num_data_points = len(fts_galat) if len(fts_galat) > len(eho_galat) else len(eho_galat)
        figsize = (num_data_points * 0.8, 6)
        fig = plt.Figure(figsize=figsize, dpi=100)
        plot = fig.add_subplot(111)

        # Plot fts galat values
        plot.plot(range(len(fts_galat)), fts_galat, label='fts', color='red', marker='o')

        # Plot eho galat values
        plot.plot(range(len(eho_galat)), eho_galat, label='fts + eho', color='blue', marker='o')

        plot.set_title('Comparison of Galat Values', fontsize=14)
        plot.set_xlabel('Index', fontsize=14)
        plot.set_ylabel('Galat', fontsize=14)
        plot.grid(True)
        plot.legend()

        # Convert the figure to a Tkinter-compatible format
        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()

        # Display the figure in the canvas
        self.plot = canvas.get_tk_widget().pack()
        # canvas.get_tk_widget().destroy()
        
        print(self.dataset)
        # Create a style object
        style = ttk.Style()

        # Configure the style properties for the table
        style.configure("Treeview",
                        rowheight=30,       # Adjust the row height (change the value as needed)
                        font=('Arial', 12)  # Adjust the font size and family (change the values as needed)
                        )
        
        tahun = self.dataset.iloc[:, 0].tolist()
        dataset = eho['dataset'][0]
        prediksi = eho['prediksi'][0]
        galat = eho['galat'][0]
        mape = eho['mape'][0]


        for i, (tahun, data, pred, gal) in enumerate(zip(tahun, dataset, prediksi, galat)):
            values = (
                tahun if tahun is not None else "",
                "{:.2f}".format(float(data)) if data is not None else "",
                "{:.2f}".format(pred) if pred is not None else "",
                "{:.5f}".format(gal) if gal is not None else "",
            )
            if i == 0:
                values += ("{:.5f}".format(mape),)  # Add mape value to the first row
            else:
                values += ("",)  # Empty string for mape in other rows
            self.table.insert(parent='', index=END, values=values)

if __name__ == "__main__":
    app = App()
    app.mainloop()

