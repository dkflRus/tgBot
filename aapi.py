# #################
token="5755974499:AAGS24gQXFg0UyjPjXqlfIUFN-ZqB5E0ucs"
debug=True
# #################

import telebot,json
# import sched
# from datetime import *
import time
states={}
class stateLib:
    default="00"
    class notifications:
        head="1"
    class changeName:
        head="2"
        nameInput=head+"0"
        timeInput=head+"1"
    class delete:
        head="3"
        indexInput=head+"0"
    class settings:
        head="4"
        printMode=head+"0"
        modMode=head+"1"
        inpMode=head+"2"


    
db={}
defaultSettings=[[["Name","user"]]]
# queue={}
admins=json.load(open("/home/dkfl/Prog/Python/tg/admins.json","r"))
print(admins)

bot=telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def pv(message):
    user=message.chat.id
    request=message.text
    if not user in states:states[user]=stateLib.default
    currState=states[user]

    # Core
    ans=""
    if not user in db:db[user]=defaultSettings
    try:
        if debug and request[0]=='=':
            args=request.split()[1:]
            if len(args)==0:ans="DBG" if user in admins else "Not allowed"
            elif args[0]=="chat":ans=str(user)
            elif user in admins:
                if args[0]=="cmd":
                    exec(args[1])
                    ans="OK"
                if args[0]=="get":
                    ans=globals()[args[1]]
                else:raise "DBG bad arg"
                
                # except:ans=str([globals(),[globals()[q] for q in globals()]])
            # elif args[0]=="set":
        elif currState==stateLib.default:
            if request==stateLib.notifications.head:
                ans=("🗃🔔NOTIFICATIONS:\n")
                if db[user][1:]!=[]:
                    for q in range(1,len(db[user])):
                        ans+=f"• {q}:{db[user][q][0]}-{time.strftime('%Y-%m-%d %H:%M',db[user][q][1])}\n"
                else:ans=("Nothing to show")
            elif request==stateLib.changeName.head:
                ans="*️⃣📋Write name:"
                currState=stateLib.changeName.nameInput
            elif request==stateLib.delete.head:
                if len(db[user])>1:
                    ans="🗑️Write ID to delete or * to cancel:"
                    currState=stateLib.delete.indexInput
                else:ans="Nothing to delete"
            elif request==stateLib.settings.head:
                ans="⚙SETTINGS\n"
                for q in range(len(db[user][0])):
                    ans=f"{q} - "+db[user][0][q][0]+":"
                    if db[user][0][q][1]==True:ans+="✅"
                    elif db[user][0][q][1]==False:ans+="❌"
                    else:ans+=str(db[user][0][q][1])
                    ans+="\n"
                ans+="Write id to change or * to exit"
                currState=stateLib.settings.modMode
        else:
            head=currState[0]
            if head==stateLib.changeName.head:
                if currState==stateLib.changeName.nameInput:
                    if request=="*":
                        ans="Cancelled"
                        currState=stateLib.default
                    else:
                        db[user].append([request])
                        ans="*️⃣⏰Write date/time"
                        currState=stateLib.changeName.timeInput
                elif currState==stateLib.changeName.timeInput:
                    if request=="*":
                        ans="Cancelled"
                        currState=stateLib.default
                        db[user].pop(-1)
                    else:
                        ints=[""]
                        I=1
                        for q in list(request):
                            if q in list("1234567890"):ints[-1]=ints[-1]+q
                            else:
                                I+=1
                                ints.append("")
                        try:
                            # print(ints)
                            if I==1:
                                goalTimeStr=time.strftime("%Y-%m-%d-%H-",time.localtime())+ints[0]
                                # print(1,time.strftime("%Y-%m-%d-%H-",time.localtime()),ints[0],goalTimeStr)
                            elif I==2:goalTimeStr=time.strftime("%Y-%m-%d-",time.localtime())+"-".join(request.split(ints))
                            elif I==3:goalTimeStr=time.strftime("%Y-%m-",time.localtime())+"-".join(request.split(ints))
                            elif I==4:goalTimeStr=time.strftime("%Y-",time.localtime())+"-".join(request.split(ints))
                            elif I==5:goalTimeStr="-".join(request.split(ints))
                            anss=time.strptime(goalTimeStr,"%Y-%m-%d-%H-%M")
                            db[user][-1].append(anss)
                            ans="OK" 
                        except:
                            ans="FAIL"
                            db[user].pop(-1)

                        currState=stateLib.default
            elif head==stateLib.delete.head:
                try:
                    delID=int(request)
                    if delID<0:0/0
                    db[user].pop(delID)
                    ans="OK"
                except ValueError:ans="Cancelled"
                except:ans="FAIL"
                currState=stateLib.default
            elif head==stateLib.settings.head:
                if currState==stateLib.settings.modMode:
                    error=True
                    try:
                        n=int(request)
                        if db[user][0][n][1] in [True,False]:
                            db[user][0][n][1]=not db[user][0][n][1]
                            ans="Toogled"
                            # continue
                        else:
                            ans="Write new value: "
                            currState=stateLib.settings.inpMode+str(n)
                        error=False
                    except ValueError:ans="Cancelled"
                    except:ans="FAIL"
                    print(error)
                    if error:currState=stateLib.default
                    # else:currState=stateLib.settings.inpMode
                    print(currState[:2])
                elif currState[:2]==stateLib.settings.inpMode:
                    n=int(currState[-1])
                    isCancel=False
                    if request=="*":
                        ans="Cancelled"
                        isCancel=True
                    elif type(db[user][0][n][1])==type(1):db[user][0][n][1]=int(request)
                    elif type(db[user][0][n][1])==type(.1):db[user][0][n][1]=float(request)
                    else:db[user][0][n][1]=request
                    if not isCancel:ans="Changed"
                    currState=stateLib.default
        if ans=="":
            print(currState)
            ans=f"\nDear {db[user][0][0][1]}, write one of this commands:\n\
            1:List\n\
            2:Add\n\
            3:Delete\n\
            4:Settings list"
        
        states[user]=currState

    except Exception as e:ans=e if debug else "Sorry, we had an error"

    bot.send_message(user,ans)
    # bot.set_chat_menu_button(message.chat.id,menu_button=telebot.b)

bot.polling(none_stop=True)