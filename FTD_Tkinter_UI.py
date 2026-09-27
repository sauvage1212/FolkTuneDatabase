import sqlite3

FolkTuneDatabase = sqlite3.connect("FolkTuneDatabase.db")
FTD_Cursor = FolkTuneDatabase.cursor()

# res = FTD_Cursor.execute("SELECT name FROM sqlite_master")
# print(res.fetchone())

def readDatabase(SQL):
    command = FTD_Cursor.execute(SQL)
    return command.fetchall()

def writeDatabase(SQL):
    command = FTD_Cursor.execute(SQL)
    FolkTuneDatabase.commit()

# writeDatabase(".mode box")
# print(readDatabase("SELECT * FROM tunes;"))

#Create the table if it doesn't exist (db created automatically by sqlite3.connect)
writeDatabase("""CREATE TABLE IF NOT EXISTS "tunes" (
name varchar(255) UNIQUE NOT NULL,
other_names varchar(255),
writer varchar(255) DEFAULT 'trad' NOT NULL,
discovered_at varchar(255) NOT NULL,
record varchar(255),
notes varchar(255),
year_learned INT CHECK (year_learned BETWEEN 1000 AND 9999),
type varchar(255),
key varchar(255)
)""")

import tkinter as tk

window = tk.Tk()
window.title("FolkTuneDatabase")
window.minsize(210, 150)
window.maxsize(1000, 500)
window.geometry("270x150+50+50")

def searchTunes():
    main_frame.pack_forget()
    updateSearchedTunes("")
    search_tunes_frame.pack(fill="both", expand=True)
    window.geometry("1000x500+50+50")

def searchInputChange(*args):
    current_input = [search_input_box.get()]
    current_input = current_input[0].split("&&")
    SQL_string = ""
    for clause in current_input:
        if "name:" in clause:
            SQL_string += clause.replace("name:", "")
        elif "key:" in clause:
            SQL_string += f"%%' AND key LIKE '%%{clause.replace("key:", "")}"
        elif "other_names:" in clause:
            SQL_string += f"%%' AND other_names LIKE '%%{clause.replace("other_names:", "")}"
        elif "writer:" in clause:
            SQL_string += f"%%' AND writer LIKE '%%{clause.replace("writer:", "")}"
        elif "discovered_at:" in clause:
            SQL_string += f"%%' AND discovered_at LIKE '%%{clause.replace("discovered_at:", "")}"
        elif "type:" in clause:
            SQL_string += f"%%' AND type LIKE '%%{clause.replace("type:", "")}"
        elif "year:" in clause:
            SQL_string += f"%%' AND year_learned LIKE '%%{clause.replace("year:", "")}"
        else:
            SQL_string += clause
        updateSearchedTunes(SQL_string)

def addEditTunes():
    main_frame.pack_forget()
    add_edit_tunes_frame.pack(fill="both", expand=True)
    window.geometry("500x208+50+50")
    # add_edit_tune_input.set("")

def back():
    search_tunes_frame.pack_forget()
    add_edit_tunes_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)
    window.geometry("270x150+50+50")

def clear():
    global add_edit_index, add_SQL, edit_SQL, add_name, edit_name
    add_edit_index = 0
    add_name = ""
    edit_name = "<collumn>:<value>"
    add_SQL = "INSERT INTO tunes VALUES (<name>, <other_names>, <writer>, <discovered_at>,\n NULL, <notes>, <year_learned>, <type>, <key>);"
    add_tune_text.set(add_SQL)
    edit_SQL = "UPDATE tunes SET <collumn> = <value> WHERE <condition>;"
    edit_tune_text.set(edit_SQL)


def updateSearchedTunes(query):
    tunes = readDatabase(f"SELECT * FROM tunes WHERE name LIKE '%%{query}%%' ORDER BY year_learned;")
    structured_tunes = structureTunes(tunes)
    scrollable_label.config(state="normal")
    scrollable_label.delete("1.0", "end")
    scrollable_label.insert("1.0", structured_tunes)
    scrollable_label.config(state="disabled")

def structureTunes(tunes):
    output = "name                      key     other names      writer           discovered at                   type     year learned\n----                      ------- -----------      ------           -------------                   ----     ------------\n"
    for tune in tunes:
        if len(tune[0]) < 25:
            output += tune[0]
            for space in range(26-len(tune[0])):
                output += " "
            output += (tune[8] or "       ")
        else:
            output += tune[0][:22] + "... " + tune[8]
        output += " "
        if len(tune[1] or "") < 17:
            output += tune[1] or ""
            for space in range(16-len(tune[1] or "")):
                output += " "
        else:
            output += tune[1][:13] + "..."
        output += " "
        if len(tune[2] or "") < 17:
            output += tune[2] or ""
            for space in range(16-len(tune[2] or "")):
                output += " "
        else:
            output += tune[2][:13] + "..."
        output += " "
        if len(tune[3] or "") < 32:
            output += tune[3] or ""
            for space in range(31-len(tune[3] or "")):
                output += " "
        else:
            output += tune[3][:28] + "..."
        output += " "
        if len(tune[7] or "") < 9:
            output += tune[7] or ""
            for space in range(8-len(tune[7] or "")):
                output += " "
        else:
            output += tune[7][:5] + "..."
        output += " "
        output += str(tune[6] or "    ")
        output += "        "
        output += "\n"
    return output

def addEditTexBoxEnter(*args):
    global add_edit_index, add_SQL, edit_SQL, add_name, edit_name
    if add_edit_tune_input.get() == "":
        add_edit_tune_input.set("NULL")
    if add_edit_index == 0:
        add_name = add_edit_tune_input.get()
        add_SQL = add_SQL.replace("<name>", formatInput(add_edit_tune_input.get()))
        add_tune_text.set(add_SQL)
        edit_name = edit_name.replace("<collumn>", add_edit_tune_input.get())
        edit_SQL = edit_SQL.replace("<collumn>", add_edit_tune_input.get())
        edit_tune_text.set(edit_SQL)
    elif add_edit_index == 1:
            add_SQL = add_SQL.replace("<other_names>", formatInput(add_edit_tune_input.get()))
            add_tune_text.set(add_SQL)
            edit_name = edit_name.replace("<value>", formatInput(add_edit_tune_input.get()))
            edit_SQL = edit_SQL.replace("<value>", formatInput(add_edit_tune_input.get()))
            edit_tune_text.set(edit_SQL)
    elif add_edit_index == 2:
                add_SQL = add_SQL.replace("<writer>", formatInput(add_edit_tune_input.get()))
                add_tune_text.set(add_SQL)
                edit_SQL = edit_SQL.replace("<condition>", add_edit_tune_input.get())
                edit_tune_text.set(edit_SQL)
    elif add_edit_index == 3:
                    add_SQL = add_SQL.replace("<discovered_at>", formatInput(add_edit_tune_input.get()))
                    add_tune_text.set(add_SQL)
    elif add_edit_index == 4:
                        add_SQL = add_SQL.replace("<notes>", formatInput(add_edit_tune_input.get()))
                        add_tune_text.set(add_SQL)
    elif add_edit_index == 5:
                            add_SQL = add_SQL.replace("<year_learned>", formatInput(add_edit_tune_input.get()))
                            add_tune_text.set(add_SQL)
    elif add_edit_index == 6:
                                add_SQL = add_SQL.replace("<type>", formatInput(add_edit_tune_input.get()))
                                add_tune_text.set(add_SQL)
    elif add_edit_index == 7:
                                    add_SQL = add_SQL.replace("<key>", formatInput(add_edit_tune_input.get()))
                                    add_tune_text.set(add_SQL)
    else:
        add_edit_tune_input.set("")
        return
    add_edit_index += 1
    add_edit_tune_input.set("")

def formatInput(input_var):
    # if isinstance(input_var, str):
    if input_var == "NULL" or input_var.isdigit():
        return input_var
    # elif input_var.isdigit():
    #     return int(input_var)
    else:
        return "'" + input_var + "'"

def addTune():
    global add_SQL, add_name
    writeDatabase(add_SQL)
    add_edit_tunes_frame.pack_forget()
    window.geometry("270x150+50+50")
    searchTunes()
    search_input_box.set(add_name)
    clear()

def editTune():
    global edit_SQL, edit_name
    writeDatabase(edit_SQL)
    add_edit_tunes_frame.pack_forget()
    window.geometry("270x150+50+50")
    searchTunes()
    search_input_box.set(edit_name)
    clear()

main_frame = tk.Frame(window)
main_frame.pack()
tk.Label(main_frame, text="Welcome Rory!", font=("Arial", 16, "bold")).pack()
tk.Label(main_frame, text="-What can we do today?", font=("Arial", 10, "normal")).pack()
tk.Button(main_frame, text="Search tunes", command=searchTunes).pack(padx=0, pady=10)
tk.Button(main_frame, text="Add/edit tunes", command=addEditTunes).pack()

search_tunes_frame = tk.Frame(window)

searched_tunes = "tunes..."
search_input_box = tk.StringVar()
search_input_box.trace_add("write", searchInputChange)
# searched_tunes = tk.StringVar(search_tunes_frame)
# searched_tunes.set("tunes...")
# search_tunes_frame.pack()

tk.Button(search_tunes_frame, text="Back", font=("Arial", 10, "normal"), command=back).pack(anchor="nw", padx=8, pady=8)
tk.Entry(search_tunes_frame, width=42, textvariable=search_input_box).pack()
scrollable_label = tk.Text(search_tunes_frame, wrap="none", height=100, width=100)
scrollable_label.insert("1.0", searched_tunes)
scrollable_label.config(state="disabled")
scrollable_label.pack(pady=(10, 0), fill="x")
# myscroll = tk.Scrollbar(search_tunes_frame, orient='vertical', command=buck.yview)
# search_tunes_frame.configure(xscrollcommand=myscroll.set)
# print(searched_tunes_label)

add_edit_tunes_frame = tk.Frame(window)

add_tune_text = tk.StringVar()
edit_tune_text = tk.StringVar()
add_edit_tune_input = tk.StringVar()
add_edit_index = 0
add_name = ""
edit_name = "<collumn>:<value>"
add_SQL = "INSERT INTO tunes VALUES (<name>, <other_names>, <writer>, <discovered_at>,\n NULL, <notes>, <year_learned>, <type>, <key>);"
add_tune_text.set(add_SQL)
edit_SQL = "UPDATE tunes SET <collumn> = <value> WHERE <condition>;"
edit_tune_text.set(edit_SQL)

btn_container = tk.Frame(add_edit_tunes_frame)
btn_container.pack(anchor="nw", fill="x")
tk.Button(btn_container, text="Back", font=("Arial", 10, "normal"), command=back).pack(side="left", padx=8, pady=8)
tk.Button(btn_container, text="Clear", font=("Arial", 10, "normal"), command=clear).pack(side="right", padx=8, pady=8)
add_edit_text_box = tk.Entry(add_edit_tunes_frame, width=42, textvariable=add_edit_tune_input)
add_edit_text_box.bind("<Return>", addEditTexBoxEnter)
add_edit_text_box.pack()
tk.Label(add_edit_tunes_frame, textvariable=add_tune_text, font=("Arial", 10, "normal")).pack()
tk.Button(add_edit_tunes_frame, text="Add tune", command=addTune).pack(anchor="nw", padx=8, pady=8)
tk.Label(add_edit_tunes_frame, textvariable=edit_tune_text, justify="left", font=("Arial", 10, "normal")).pack(anchor="nw")
tk.Button(add_edit_tunes_frame, text="Edit tune", command=editTune).pack(anchor="nw", padx=8, pady=8)

window.mainloop()