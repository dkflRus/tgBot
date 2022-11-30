import time,sched
db=[]
settings=[["Notifications",True]]
while True:
    print("\nWrite one ot the commands:\n"
        "1:List\n"
        "2:Add\n"
        "3:Delete\n"
        "4:Settings")
    i=input()
    if i=="1":
        print("🗃🔔NOTIFICATIONS:")
        if db!=[]:
            for q in range(len(db)):
                print(f"* {q}:{db[q][0]}-{time.strftime('%Y-%m-%d %H:%M',db[q][1])}")
        else:print("Nothing to show")
    elif i=="2":
        curr=[input("*️⃣📋Write name:")]
        i=input("*️⃣⏰Write date/time")
        ints=[""]
        I=1
        for q in list(i):
            if q in list("1234567890"):ints[-1]=ints[-1]+q
            else:
                I+=1
                ints.append("")
        # try:
            if I==1:goalTimeStr=time.strftime("%Y-%m-%d-%H-",time.localtime())+ints[0]
            elif I==2:goalTimeStr=time.strftime("%Y-%m-%d-",time.localtime())+"-".join(i.split(ints))
            elif I==3:goalTimeStr=time.strftime("%Y-%m-",time.localtime())+"-".join(i.split(ints))
            elif I==4:goalTimeStr=time.strftime("%Y-",time.localtime())+"-".join(i.split(ints))
            elif I==5:goalTimeStr="-".join(i.split(ints))
            curr.append(time.strptime(goalTimeStr,"%Y-%m-%d-%H-%M"))
            db.append(curr)
            print("OK")
        # except:print("Error")
    elif i=="3":
        try:
            db.pop(int(input("🗑️Write ID to delete:")))
            print("OK")
        except:print("Error")
    elif i=="4":
        print("⚙SETTINGS")
        for q in range(len(settings)):
            i=f"(preReleaseID={q})"+settings[q][0]+":"
            if settings[q][1]==True:i+="✅"
            elif settings[q][1]==True:i+="❌"
            else:i+=str(settings[q][1])
            print(i)
        try:
            n=int(input("Write ID to change: "))
            if settings[n][1] in [True,False]:
                settings[n][1]=not settings[n][1]
                print("Toogled")
                continue
            else:
                i=input("Write new value: ")
                if type(settings[n][1]) in "int":settings[n][1]=int(i)
                elif type(settings[n][1]) in "float":settings[n][1]=float(i)
                else:settings[n][1]=i
        except:print("Error")
        
    else:print("Нет такой команды")