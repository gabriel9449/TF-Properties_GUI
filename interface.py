# Copyright <2025> <INSTITUTO TECNOLÓGICO Y DE ESTUDIOS SUPERIORES DE MONTERREY>

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN 
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# If you use this code r any file this repertory in a scientific publication, we would appreciate citations to the following paper:
# Unlocking the Potential of Insect and Plant Proteins: Predicting Techno-Functional Properties with Machine Learning, Brena-Melendez et al.

import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tkinter import *
import pandas as pd
import pickle
from mypythonlib import data_parse

#Models directory#
model_dir = r"best_version"
model_1 = pickle.load(open(os.path.join(model_dir,"SL_AllIn_AllOut.sav"),'rb'))
model_2 = pickle.load(open(os.path.join(model_dir,"SL_LessIn_WHC.sav"),'rb'))
model_3 = pickle.load(open(os.path.join(model_dir,"SL_LessIn_OHC.sav"),'rb'))
model_4 = pickle.load(open(os.path.join(model_dir,"RF_LessIn_FC.sav"),'rb'))
model_5 = pickle.load(open(os.path.join(model_dir,"SL_LessIn_ECOIL.sav"),'rb'))
model_6 = pickle.load(open(os.path.join(model_dir,"RF_LessIn_ECH20.sav"),'rb'))

#Database directory#
database = pd.read_excel('My Mixes.xlsx', sheet_name='Sheet1')
db_names = database["Ingredient ID"]
db_data = database[["Protein", "Fat", "Ashes", "Insoluble dietary fiber", "Soluble dietary fiber", "Total Dietary Fiber", "NNE", "Moisture"]]

database_parsed, scaler = data_parse.insect_plant_preproc(database)

mix_data = database_parsed.tail(1)
mix_data = mix_data.rename(index={mix_data.index.values[0]:0})

gui = Tk()

ingredient1 = StringVar()
ingredient2 = StringVar()
proportion1 = DoubleVar()
proportion2 = DoubleVar()

gui.title("Mix Insects-Plants Interface")
gui.geometry('1500x700')
gui.configure(background="light blue")

frame_1 = Frame(gui, height=20,width=280)
frame_1.place(x=10,y=10)
lbl = Label(frame_1, text="Choose ingredients and proportion: ")
lbl.place(x=0,y=0)

frame_2 = Frame(gui)
frame_2.place(x=10,y=40)
list_ing1 = Listbox(frame_2, height=5, width=15, activestyle='dotbox', exportselection=0)
list_lbl1 = Label(frame_2, text="Ingredient 1:", justify='left')
for i in db_names.index.values:
    if(~db_names.isna().iloc[i]):
        list_ing1.insert(i, "%d - "%(i+1)+db_names.iloc[i])
    else:
        break
list_lbl1.pack(side = TOP)
list_sb1 = Scrollbar(frame_2)
list_sb1.pack(side = RIGHT, fill = BOTH)
list_ing1.select_set(0)
list_ing1.pack(side = RIGHT, fill = BOTH)
list_ing1.config(yscrollcommand=list_sb1)
list_sb1.config(command = list_ing1.yview)

frame_3 = Frame(gui)
frame_3.place(x=10,y=155)
list_ing2 = Listbox(frame_3, height=5, width=15, activestyle='dotbox', exportselection=0)
list_lbl2 = Label(frame_3, text="Ingredient 2:")
for i in db_names.index.values:
    if(~db_names.isna().iloc[i]):
        list_ing2.insert(i, "%d - "%(i+1)+db_names.iloc[i])
    else:
        break
list_lbl2.pack(side = TOP)
list_sb2 = Scrollbar(frame_3)
list_sb2.pack(side = RIGHT, fill = BOTH)
list_ing2.select_set(0)
list_ing2.pack(side = RIGHT, fill = BOTH)
list_ing2.config(yscrollcommand=list_sb1)
list_sb2.config(command = list_ing2.yview)

frame_4 = Frame(gui)
frame_4.place(x=130, y=40)
txt_lbl = Label(frame_4, text="Mixture Composition")
txt = Label(frame_4, text="")
txt_lbl.pack(side=TOP)
txt.pack(side=LEFT)
mix_txt = "%s at %0.1f and %s at %0.1f" % ("", 0, "", 0)
txt.config(text=mix_txt)

frame_5 = Frame(gui)
frame_5.place(x=360, y=40)

def update_txt(event):
    ingredient1 = db_names[list_ing1.index(list_ing1.curselection())]
    ingredient2 = db_names[list_ing2.index(list_ing2.curselection())]
    proportion2.set(1-proportion1.get())
    mix_txt = "%s at %0.1f and %s at %0.1f" % (ingredient1, proportion1.get(), ingredient2, proportion2.get())
    txt.config(text=mix_txt)
    for i in range(4):
        e1 = Entry(frame_5, width=15, justify='center')
        if(i==0):
            e1.grid(row=i, column=0)
            e1.insert(END, "Ingredients")
        elif(i==1):
            e1.grid(row=i, column=0)
            e1.insert(END, "%s" % ingredient1)
        elif(i==2):
            e1.grid(row=i, column=0)
            e1.insert(END, "%s" % ingredient2)
        else:
            e1.grid(row=i, column=0)
            e1.insert(END, "Mix")
        for j in range(1,len(db_data.columns)+1):
            e1 = Entry(frame_5, width=20, justify='center')
            if(i==0):
                e1.grid(row=i, column=j)
                e1.insert(END, db_data.columns.values[j-1])
            elif(i==1):
                e1.grid(row=i, column=j)
                e1.insert(END, "%.02f" %float(db_data.iloc[list_ing1.index(list_ing1.curselection()), j-1]))
                mix_data.loc[0, db_data.columns.values[j-1]] = db_data.iloc[list_ing1.index(list_ing1.curselection()), j-1]*proportion1.get()
            elif(i==2):
                e1.grid(row=i, column=j)
                e1.insert(END, "%.02f" %float(db_data.iloc[list_ing2.index(list_ing2.curselection()), j-1]))
                mix_data.loc[0, db_data.columns.values[j-1]] = mix_data.loc[0, db_data.columns.values[j-1]] + db_data.iloc[list_ing2.index(list_ing2.curselection()), j-1]*proportion2.get()
            else:
                e1.grid(row=i, column=j)
                e1.insert(END, "%.02f" %mix_data.loc[0, db_data.columns.values[j-1]])
    mix_data.loc[0, "Ingredient 1 (Location)"] = list_ing1.index(list_ing1.curselection())+1
    mix_data.loc[0, "Proportion"] = proportion1.get()
    mix_data.loc[0, "Ingredient 2 (Location)"] = list_ing2.index(list_ing2.curselection())+1
    mix_data.loc[0, "Proportion.1"] = proportion2.get()
    
list_ing2.bind('<<ListboxSelect>>', update_txt)
list_ing1.bind('<<ListboxSelect>>', update_txt)

frame_6 = Frame(gui)
frame_6.place(x=130, y=90)
sc1 = Scale(frame_6, from_=0.2, to=0.8, orient=HORIZONTAL, 
            resolution=0.1, command=update_txt, variable=proportion1)
sc1_lbl = Label(frame_6, text="Ingredient 1 proportion:")
sc1_lbl.pack(side = TOP)
sc1.pack(side = LEFT, fill = BOTH)

frame_7 = Frame(gui)
frame_7.place(x=360, y=170)

def clicked():
    mix_scaled = pd.DataFrame(scaler.transform(mix_data), columns=mix_data.columns)
    X_1 = mix_scaled.drop(columns=['WHC ', 'OHC', 'FC', 'EC Oil', 'EC H20'])
    X_23456 = mix_scaled.drop(columns=['Stage','Part','Treatment','Defatting treatment', 'Drying ', 'WHC ', 'OHC', 'FC', 'EC Oil', 'EC H20'])

    y_1 = mix_scaled[['WHC ', 'OHC', 'FC', 'EC Oil', 'EC H20']]
    y_2 = mix_scaled[['WHC ']]
    y_3 = mix_scaled[['OHC']]
    y_4 = mix_scaled[['FC']]
    y_5 = mix_scaled[['EC Oil']]
    y_6 = mix_scaled[['EC H20']]

    pred_1 = model_1.predict(X_1)
    pred_1 = pd.DataFrame(pred_1, columns=y_1.columns, index=y_1.index)
    results_1 = pd.concat([X_1, pred_1], axis=1)
    results_1 = pd.DataFrame(scaler.inverse_transform(results_1), columns=mix_scaled.columns)

    pred_2 = model_2.predict(X_23456)
    pred_2 = pd.DataFrame(pred_2, columns=y_2.columns, index=y_2.index)
    results_2 = pd.concat([X_23456, mix_scaled[['Stage','Part','Treatment','Defatting treatment', 'Drying ']], pred_2, 
                        mix_scaled[['OHC', 'FC', 'EC Oil', 'EC H20']]], axis=1)
    results_2 = pd.DataFrame(scaler.inverse_transform(results_2), columns=mix_scaled.columns)

    pred_3 = model_3.predict(X_23456)
    pred_3 = pd.DataFrame(pred_3, columns=y_3.columns, index=y_3.index)
    results_3 = pd.concat([X_23456, mix_scaled[['Stage','Part','Treatment','Defatting treatment', 'Drying ', 'WHC ']], pred_3, 
                        mix_scaled[['FC', 'EC Oil', 'EC H20']]], axis=1)
    results_3 = pd.DataFrame(scaler.inverse_transform(results_3), columns=mix_scaled.columns)

    pred_4 = model_4.predict(X_23456)
    pred_4 = pd.DataFrame(pred_4, columns=y_4.columns, index=y_4.index)
    results_4 = pd.concat([X_23456, mix_scaled[['Stage','Part','Treatment','Defatting treatment', 'Drying ', 'WHC ', 'OHC']], pred_4,
                        mix_scaled[['EC Oil', 'EC H20']]], axis=1)
    results_4 = pd.DataFrame(scaler.inverse_transform(results_4), columns=mix_scaled.columns)

    pred_5 = model_5.predict(X_23456)
    pred_5 = pd.DataFrame(pred_5, columns=y_5.columns, index=y_5.index)
    results_5 = pd.concat([X_23456, mix_scaled[['Stage','Part','Treatment','Defatting treatment', 'Drying ', 'WHC ', 'OHC', 'FC']], pred_5,
                        mix_scaled[['EC H20']]], axis=1)
    results_5 = pd.DataFrame(scaler.inverse_transform(results_5), columns=mix_scaled.columns)

    pred_6 = model_6.predict(X_23456)
    pred_6 = pd.DataFrame(pred_6, columns=y_6.columns, index=y_6.index)
    results_6 = pd.concat([X_23456, mix_scaled[['Stage','Part','Treatment','Defatting treatment', 'Drying ', 'WHC ', 'OHC', 'FC', 'EC Oil']], pred_6], axis=1)
    results_6 = pd.DataFrame(scaler.inverse_transform(results_6), columns=mix_scaled.columns)
    
    for i in range(3*6):
        e2 = Entry(frame_7, width=36, justify='center')

        match i:
            case 0 | 1 | 2:
                y = y_1 
                results = results_1 
                name = "All inputs - All outputs"
            case 3 | 4 | 5: 
                y = y_2 
                results = results_2
                name = "Less inputs - WHC"
            case 6 | 7 | 8:
                y = y_3 
                results = results_3
                name = "Less inputs - OHC"
            case 9 | 10 | 11:
                y = y_4
                results = results_4
                name = "Less inputs - FC"
            case 12 | 13 | 14:
                y = y_5
                results = results_5
                name = "Less inputs - EC Oil"
            case 15 | 16 | 17: 
                y = y_6 
                results = results_6
                name = "Less inputs - EC H20"


        if((i%3)==0):
            e2.grid(row=i, column=0)
            e2.insert(END, name)
        elif((i%3)==1):
            e2.grid(row=i, column=0)
            e2.insert(END, "Predictions")
        else:
            e2.grid(row=i, column=0)
            e2.insert(END, "Results")
        
        for j in range(1,len(y.columns)+1):
            e2 = Entry(frame_7, width=20, justify='center')
            match y.columns.values[j-1]:
                case "WHC ":
                    j_aux = 1
                case "OHC":
                    j_aux = 2
                case "FC":
                    j_aux = 3
                case "EC Oil":
                    j_aux = 4
                case "EC H20":
                    j_aux = 5
            if((i%3)==1):
                e2.grid(row=i, column=j_aux)
                e2.insert(END,  y.columns.values[j-1])
            elif((i%3)==2):
                e2.grid(row=i, column=j_aux)
                e2.insert(END, "%.03f" %results.loc[0, y.columns.values[j-1]])
            

frame_8 = Frame(gui)
frame_8.place(x=150, y=170) 
btn = Button(frame_8, text = "Run predictions" ,
             fg = "red", command=clicked)
btn.pack(side= TOP)

gui.mainloop()