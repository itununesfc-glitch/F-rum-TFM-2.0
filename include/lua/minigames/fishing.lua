tfm.exec.disableAfkDeath(true)
tfm.exec.disableAutoScore(true)
tfm.exec.disableAutoShaman(true)
tfm.exec.disableAutoNewGame(true)
tfm.exec.newGame('<C><P d="x_transformice/x_maps/x_peche2014/x_montagne2.png" D="x_transformice/x_maps/x_peche2014/x_montagne.jpg" Ca="" /><Z><S><S H="400" X="-5" o="12bd94" L="10" Y="200" P="0,0,0.3,0.2,0,0,0,0" m="" T="12" /><S H="10" X="46" o="12bd94" L="100" Y="66" P="0,0,0.3,0.2,20,0,0,0" m="" T="12" /><S H="10" X="121" o="12bd94" L="80" Y="107" P="0,0,0.5,0.2,40,0,0,0" m="" T="12" /><S H="10" X="169" o="12bd94" L="80" Y="165" P="0,0,0.5,0.2,60,0,0,0" m="" T="12" /><S H="10" X="216" o="12bd94" L="80" Y="207" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="270" o="12bd94" L="80" Y="241" P="0,0,0.5,0.2,60,0,0,0" m="" T="12" /><S H="10" X="468" o="12bd94" L="100" Y="249" P="0,0,0.5,0.2,-40,0,0,0" m="" T="12" /><S H="10" X="559" o="12bd94" L="100" Y="168" P="0,0,0.5,0.2,-10,0,0,0" m="" T="12" /><S H="10" X="500" o="12bd94" L="100" Y="219" P="0,0,0.5,0.2,-70,0,0,0" m="" T="12" /><S H="10" X="627" o="12bd94" L="100" Y="118" P="0,0,0.5,0.2,-50,0,0,0" m="" T="12" /><S H="10" X="708" o="12bd94" L="50" Y="90" P="0,0,0.5,0.2,-90,0,0,0" m="" T="12" /><S H="10" X="728" o="12bd94" L="50" Y="65" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="754" o="12bd94" L="50" Y="42" P="0,0,0.5,0.2,-60,0,0,0" m="" T="12" /><S H="400" X="806" o="12bd94" L="10" Y="200" P="0,0,0.3,0.2,0,0,0,0" m="" T="12" /><S H="10" X="461" o="12bd94" L="100" Y="353" P="0,0,0.5,0.2,-10,0,0,0" m="" T="12" /><S H="10" X="379" o="12bd94" L="100" Y="361" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="304" o="12bd94" L="100" Y="358" P="0,0,0.5,0.2,10,0,0,0" m="" T="12" /><S H="10" X="212" o="12bd94" L="100" Y="349" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="22" o="12bd94" L="100" Y="315" P="0,0,0.5,0.2,90,0,0,0" m="" T="12" /><S H="10" X="689" o="12bd94" L="50" Y="93" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="660" o="12bd94" L="50" Y="92" P="0,0,0.5,0.2,-90,0,0,0" m="" T="12" /><S H="10" X="58" o="12bd94" L="100" Y="374" P="0,0,0.5,0.2,10,0,0,0" m="" T="12" /><S H="10" X="123" o="12bd94" L="100" Y="365" P="0,0,0.5,0.2,-20,0,0,0" m="" T="12" /><S H="10" X="550" o="12bd94" L="100" Y="346" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="638" o="12bd94" L="100" Y="362" P="0,0,0.5,0.2,20,0,0,0" m="" T="12" /><S H="10" X="691" o="12bd94" L="100" Y="363" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /><S H="10" X="769" o="12bd94" L="100" Y="317" P="0,0,0.5,0.2,-80,0,0,0" m="" T="12" /><S H="10" X="371" o="12bd94" L="70" Y="319" P="0,0,0.5,0.2,0,0,0,0" m="" T="12" /></S><D><DS X="558" Y="148" /></D><O /></Z></C>')
tfm.exec.setUIMapName("<r><j>Fishing Event")
tfm.exec.setGameTime(83)
part=0
goz=0
lang={}

p={}
function eventNewPlayer(name)
tfm.exec.addImage("LuaImage5ae5c227100207.92473254.png","?0",0,0)
p[name]={sure=0}
for key=1,600,1 do
tfm.exec.bindKeyboard(name,key,true)
end
if tfm.get.room.playerList[name].community=="tr" or tfm.get.room.playerList[name].community=="en" or tfm.get.room.playerList[name].community=="pl" then
if tfm.get.room.playerList[name].community=="tr" then
lang[name]={
help="<j>Merhaba Küçük Fareler,2018 Balık Eventimiz Aktiftir !<br><v>Mor Okların Olduğu Bölgelere Gidip <r>Space<v> Tuşuna Basarsanız İtem Tutmaya Başlarsınız.<br><g>Yapımcılar : <vp> Database",
stay="<j>Burda sabit bir şekilde bekleyin lütfen",
notplace="<j>Burası Uygun biyer değil Lütfen su olan bir yere gidiniz.",
notstop="<r>Sabit Durmadığınız İçin işlem iptal edildi !",
bitti="<j>Şimdilik Sona Erdi Tekrar Başlayacaktır !",
gift="<v>Hediye alındı !",
thx="<vp>Dil Çevirisi İçin Teşekkürler <g>: <v>EN <g>:<bv> Fys <g>| <v>PL <g>: <bv>Eveye"
}
end
if tfm.get.room.playerList[name].community=="en" then
lang[name]={
help="<j>Hello little mice! The 2018 Fishing Event is now ACTIVE!<br><v>Follow the purple arrows and press the <r>space<v> button to start catching items for your inventory!<br><g>DEVS : <vp> Database",
stay="<j>Please stay here!",
notplace="<j>There is no puddle here! Find another place. ",
notstop="<r>Oops, stay steady!",
bitti="<j>The event is finished (for now!)",
gift="<v>Gift received!",
thx="<vp>Thanks for Language Translation <g>: <v>EN <g>: <bv>Fys <g>| <v>PL <g>: <bv>Eveye"
}
end

if tfm.get.room.playerList[name].community=="pl" then
lang[name]={
help="<j>Witajcie myszki - Event łowienia został aktywowany!<br><v>Fioletowe strzałki pokazują miejsce, gdzie musisz stanąć oraz kliknij <r>spacje<v> w tym miejscu, aby zacząć łowić.<br><g>Event stworzony przez : <vp> Database",
stay="<j>Stój tutaj!",
notplace="<j>W tym miejscu nie znaleziono wody, przejdź do innego miejsca",
notstop="<r>Proces łowienia nie został dokończony do końca, dlatego został anulowany",
bitti="<j>Event zakończony!",
gift="<v>Otrzymałeś/aś nagrodę!",
thx="<vp>Podziękowania za tłumaczenie dla <g>: <v>EN <g>: <bv>Fys <g>| <v>PL <g>: <bv>Eveye"
}
end

else

lang[name]={
help="<j>Hello little mice! The 2018 Fishing Event is now ACTIVE!<br><v>Follow the purple arrows and press the <r>space<v> button to start catching items for your inventory!<br><g>DEVS : <j>Cucumberon<g> ,<vp> Klarkoo",
stay="<j>Please stay here!",
notplace="<j>There is no puddle here! Find another place. ",
notstop="<r>Oops, stay steady!",
bitti="<j>The event is finished (for now!)",
gift="<v>Gift received!",
thx="<vp>Thanks for Language Translation <g>: <v>EN <g>: <bv>Fys <g>| <v>PL <g>: <bv>Eveye"
}
tfm.exec.chatMessage("<r>Not Maked Your Language Your Community : "..tfm.get.room.playerList[name].community.." but Available Language TR - EN - PL",name)

end
end

for name in pairs(tfm.get.room.playerList) do
eventNewPlayer(name)
tfm.exec.chatMessage(lang[name].help,name)
tfm.exec.chatMessage(lang[name].thx,name)

end
function pythag(x1,y1,x2,y2,r) 
local x=x2-x1
 local y=y2-y1 
local r=r+r 
return x*x+y*y<r*r 
end
for name in pairs(tfm.get.room.playerList) do
eventNewPlayer(name)
end



function eventKeyboard(name, key, down, x,y)
if  p[name].sure>=1 then
p[name].sure=0
tfm.exec.chatMessage(lang[name].notstop,name)
tfm.exec.playEmote(name,"9")
end
if key==32 and p[name].sure<=0  then
if pythag(704,42, tfm.get.room.playerList[name].x, tfm.get.room.playerList[name].y,20) or pythag(206,186, tfm.get.room.playerList[name].x, tfm.get.room.playerList[name].y,20)  or pythag(59,356, tfm.get.room.playerList[name].x, tfm.get.room.playerList[name].y,20) or pythag(678,347, tfm.get.room.playerList[name].x, tfm.get.room.playerList[name].y,20) then 
tfm.exec.playEmote(name,"11")
p[name].sure=1
tfm.exec.chatMessage(lang[name].stay,name)
else
tfm.exec.chatMessage(lang[name].notplace,name)
end
end
end
function eventLoop(t,r)
for name,v in pairs(tfm.get.room.playerList) do
if v.movingLeft and p[name].sure>=1  then
p[name].sure=0
tfm.exec.chatMessage(lang[name].notstop,name)
tfm.exec.playEmote(name,"9")
elseif v.movingRight and p[name].sure>=1 then
p[name].sure=0
tfm.exec.chatMessage(lang[name].notstop,name)
tfm.exec.playEmote(name,"9")
end
end

for name in pairs(tfm.get.room.playerList) do
--ui.addTextArea(1,r)
if r<=700 then
tfm.exec.chatMessage(lang[name].bitti,name)
end
if r<=0 then
system.exit()
end
end
part=part+1
if part==3 and goz <=2 then
part=0
goz=goz+1
tfm.exec.addShamanObject(0,704,42-15,0,10,0) 
tfm.exec.addShamanObject(0,206,186-15,0,10,0) 
tfm.exec.addShamanObject(0,59,356-15,0,10,0) 
tfm.exec.addShamanObject(0,678,347-15,0,10,0) 
end
for name in pairs(tfm.get.room.playerList) do
if p[name].sure>=1 then
p[name].sure=p[name].sure+1
end
if p[name].sure>=15 then
p[name].sure=0

tfm.exec.giveConsumables(name, math.random(0,35), math.random(1,3))
tfm.exec.chatMessage(lang[name].gift,name)
tfm.exec.playEmote(name,"9")
end
end
end