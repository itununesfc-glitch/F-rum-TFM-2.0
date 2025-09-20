local json = { _version = "0.1.1" }
-------------------------------------------------------------------------------
-- Encode
-------------------------------------------------------------------------------
local encode
local escape_char_map = {
  [ "\\" ] = "\\\\",
  [ "\"" ] = "\\\"",
  [ "\b" ] = "\\b",
  [ "\f" ] = "\\f",
  [ "\n" ] = "\\n",
  [ "\r" ] = "\\r",
  [ "\t" ] = "\\t",
}
local escape_char_map_inv = { [ "\\/" ] = "/" }
for k, v in pairs(escape_char_map) do
  escape_char_map_inv[v] = k
end
local function escape_char(c)
  return escape_char_map[c] or string.format("\\u%04x", c:byte())
end
local function encode_nil(val)
  return "null"
end
local function encode_table(val, stack)
  local res = {}
  stack = stack or {}

  -- Circular reference?
  if stack[val] then error("circular reference") end

  stack[val] = true

  if val[1] ~= nil or next(val) == nil then
    -- Treat as array -- check keys are valid and it is not sparse
    local n = 0
    for k in pairs(val) do
      if type(k) ~= "number" then
        error("invalid table: mixed or invalid key types")
      end
      n = n + 1
    end
    if n ~= #val then
      error("invalid table: sparse array")
    end
    -- Encode
    for i, v in ipairs(val) do
      table.insert(res, encode(v, stack))
    end
    stack[val] = nil
    return "[" .. table.concat(res, ",") .. "]"

  else
    -- Treat as an object
    for k, v in pairs(val) do
      if type(k) ~= "string" then
        error("invalid table: mixed or invalid key types")
      end
      table.insert(res, encode(k, stack) .. ":" .. encode(v, stack))
    end
    stack[val] = nil
    return "{" .. table.concat(res, ",") .. "}"
  end
end
local function encode_string(val)
  return '"' .. val:gsub('[%z\1-\31\\"]', escape_char) .. '"'
end
local function encode_number(val)
  -- Check for NaN, -inf and inf
  if val ~= val or val <= -math.huge or val >= math.huge then
    error("unexpected number value '" .. tostring(val) .. "'")
  end
  return string.format("%.14g", val)
end
local type_func_map = {
  [ "nil"     ] = encode_nil,
  [ "table"   ] = encode_table,
  [ "string"  ] = encode_string,
  [ "number"  ] = encode_number,
  [ "boolean" ] = tostring,
}
encode = function(val, stack)
  local t = type(val)
  local f = type_func_map[t]
  if f then
    return f(val, stack)
  end
  error("unexpected type '" .. t .. "'")
end
function json.encode(val)
  return ( encode(val) )
end
-------------------------------------------------------------------------------
-- Decode
-------------------------------------------------------------------------------
local parse
local function create_set(...)
  local res = {}
  for i = 1, select("#", ...) do
    res[ select(i, ...) ] = true
  end
  return res
end
local space_chars   = create_set(" ", "\t", "\r", "\n")
local delim_chars   = create_set(" ", "\t", "\r", "\n", "]", "}", ",")
local escape_chars  = create_set("\\", "/", '"', "b", "f", "n", "r", "t", "u")
local literals      = create_set("true", "false", "null")
local literal_map = {
  [ "true"  ] = true,
  [ "false" ] = false,
  [ "null"  ] = nil,
}
local function next_char(str, idx, set, negate)
  for i = idx, #str do
    if set[str:sub(i, i)] ~= negate then
      return i
    end
  end
  return #str + 1
end
local function decode_error(str, idx, msg)
  local line_count = 1
  local col_count = 1
  for i = 1, idx - 1 do
    col_count = col_count + 1
    if str:sub(i, i) == "\n" then
      line_count = line_count + 1
      col_count = 1
    end
  end
  error( string.format("%s at line %d col %d", msg, line_count, col_count) )
end
local function codepoint_to_utf8(n)
  local f = math.floor
  if n <= 0x7f then
    return string.char(n)
  elseif n <= 0x7ff then
    return string.char(f(n / 64) + 192, n % 64 + 128)
  elseif n <= 0xffff then
    return string.char(f(n / 4096) + 224, f(n % 4096 / 64) + 128, n % 64 + 128)
  elseif n <= 0x10ffff then
    return string.char(f(n / 262144) + 240, f(n % 262144 / 4096) + 128,
                       f(n % 4096 / 64) + 128, n % 64 + 128)
  end
  error( string.format("invalid unicode codepoint '%x'", n) )
end
local function parse_unicode_escape(s)
  local n1 = tonumber( s:sub(3, 6),  16 )
  local n2 = tonumber( s:sub(9, 12), 16 )
  -- Surrogate pair?
  if n2 then
    return codepoint_to_utf8((n1 - 0xd800) * 0x400 + (n2 - 0xdc00) + 0x10000)
  else
    return codepoint_to_utf8(n1)
  end
end
local function parse_string(str, i)
  local has_unicode_escape = false
  local has_surrogate_escape = false
  local has_escape = false
  local last
  for j = i + 1, #str do
    local x = str:byte(j)

    if x < 32 then
      decode_error(str, j, "control character in string")
    end

    if last == 92 then -- "\\" (escape char)
      if x == 117 then -- "u" (unicode escape sequence)
        local hex = str:sub(j + 1, j + 5)
        if not hex:find("%x%x%x%x") then
          decode_error(str, j, "invalid unicode escape in string")
        end
        if hex:find("^[dD][89aAbB]") then
          has_surrogate_escape = true
        else
          has_unicode_escape = true
        end
      else
        local c = string.char(x)
        if not escape_chars[c] then
          decode_error(str, j, "invalid escape char '" .. c .. "' in string")
        end
        has_escape = true
      end
      last = nil

    elseif x == 34 then -- '"' (end of string)
      local s = str:sub(i + 1, j - 1)
      if has_surrogate_escape then
        s = s:gsub("\\u[dD][89aAbB]..\\u....", parse_unicode_escape)
      end
      if has_unicode_escape then
        s = s:gsub("\\u....", parse_unicode_escape)
      end
      if has_escape then
        s = s:gsub("\\.", escape_char_map_inv)
      end
      return s, j + 1

    else
      last = x
    end
  end
  decode_error(str, i, "expected closing quote for string")
end
local function parse_number(str, i)
  local x = next_char(str, i, delim_chars)
  local s = str:sub(i, x - 1)
  local n = tonumber(s)
  if not n then
    decode_error(str, i, "invalid number '" .. s .. "'")
  end
  return n, x
end
local function parse_literal(str, i)
  local x = next_char(str, i, delim_chars)
  local word = str:sub(i, x - 1)
  if not literals[word] then
    decode_error(str, i, "invalid literal '" .. word .. "'")
  end
  return literal_map[word], x
end
local function parse_array(str, i)
  local res = {}
  local n = 1
  i = i + 1
  while 1 do
    local x
    i = next_char(str, i, space_chars, true)
    -- Empty / end of array?
    if str:sub(i, i) == "]" then
      i = i + 1
      break
    end
    -- Read token
    x, i = parse(str, i)
    res[n] = x
    n = n + 1
    -- Next token
    i = next_char(str, i, space_chars, true)
    local chr = str:sub(i, i)
    i = i + 1
    if chr == "]" then break end
    if chr ~= "," then decode_error(str, i, "expected ']' or ','") end
  end
  return res, i
end
local function parse_object(str, i)
  local res = {}
  i = i + 1
  while 1 do
    local key, val
    i = next_char(str, i, space_chars, true)
    -- Empty / end of object?
    if str:sub(i, i) == "}" then
      i = i + 1
      break
    end
    -- Read key
    if str:sub(i, i) ~= '"' then
      decode_error(str, i, "expected string for key")
    end
    key, i = parse(str, i)
    -- Read ':' delimiter
    i = next_char(str, i, space_chars, true)
    if str:sub(i, i) ~= ":" then
      decode_error(str, i, "expected ':' after key")
    end
    i = next_char(str, i + 1, space_chars, true)
    -- Read value
    val, i = parse(str, i)
    -- Set
    res[key] = val
    -- Next token
    i = next_char(str, i, space_chars, true)
    local chr = str:sub(i, i)
    i = i + 1
    if chr == "}" then break end
    if chr ~= "," then decode_error(str, i, "expected '}' or ','") end
  end
  return res, i
end
local char_func_map = {
  [ '"' ] = parse_string,
  [ "0" ] = parse_number,
  [ "1" ] = parse_number,
  [ "2" ] = parse_number,
  [ "3" ] = parse_number,
  [ "4" ] = parse_number,
  [ "5" ] = parse_number,
  [ "6" ] = parse_number,
  [ "7" ] = parse_number,
  [ "8" ] = parse_number,
  [ "9" ] = parse_number,
  [ "-" ] = parse_number,
  [ "t" ] = parse_literal,
  [ "f" ] = parse_literal,
  [ "n" ] = parse_literal,
  [ "[" ] = parse_array,
  [ "{" ] = parse_object,
}
parse = function(str, idx)
  local chr = str:sub(idx, idx)
  local f = char_func_map[chr]
  if f then
    return f(str, idx)
  end
  decode_error(str, idx, "unexpected character '" .. chr .. "'")
end
function json.decode(str)
  if type(str) ~= "string" then
    error("expected argument of type string, got " .. type(str))
  end
  local res, idx = parse(str, next_char(str, 1, space_chars, true))
  idx = next_char(str, idx, space_chars, true)
  if idx <= #str then
    decode_error(str, idx, "trailing garbage")
  end
  return res
end

local yazilar = {
	["tr"] = {
		["hosgeldin"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Hoşgeldin</font>\n\n<font color='#9a9a9a'>Lidertablosu için</font><font color='#F272A5'><b> !lb</b>\n<font color='#9a9a9a'>kişisel rekorlar için</font></b><font color='#F272A5'><b> !lsrec</b></font>",
		["rec"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Rekor\n</font><font color='#F272A5'>%s</font>(<V>%s</V>s)!",
		["recguncel"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Yeni rekor\n</font><font color='#F272A5'>%s</font>(<V>%s</V>s)!",
		["banned"] = "<R>Fastracing'den banlandın!</R>",
		["won"] = "<font color='#F272A5'>%s</font> roundu kazandı",
		["alrbanned"] = "<R>Bu oyuncu zaten banlı</R>",
		["urcantban"] = "<R>Kendini banlayamazsın</R>",
		["banlandi"] = "<R>%s banlandı</R>",
		["banlidegil"] = "<R>Bu oyuncu zaten banlı değil</R>",
		["unban"] = "<R>%s banı açıldı</R>",
		["clog"] = "<R>BanList temizlendi</R>",
		["bansayi"] = "Banlı oyuncu sayısı:",
		--skortablo
		["lbbaslik"] = "LİDER TABLOSU",
		["lbplayer"] = "Oyuncu",
		["lbrecord"] = "Rekor",
		--lsrec
		["xrekor"] = "<font color='#F272A5'>%s</font><font color='#9a9a9a'> isimli oyuncunun rekorları</font>:<font color='#F272A5'> %s\n\n</font>",
		["norec"] = "<R>Bu oyuncunun hiç rekoru yok.</R>",
		["syntax"] = "<R>Lütfen bir isim gir! Syntax: !lsrec nick </R>",
		["yourrec"] = "<font color='#9a9a9a'>Rekorların</font>:<font color='#F272A5'> %s\n\n</font>",
		["recinyok"] = "<R>Hiç rekorun yok.</R>",
	},
	["en"] = {
		["hosgeldin"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Welcome</font>\n\n<font color='#9a9a9a'>use </font><font color='#F272A5'><b>!lb</font></b><font color='#9a9a9a'> for Leaderboard</font>\n<font color='#F272A5'><b>!lsrec</font></b></b><font color='#9a9a9a'> for personal records.</font>",
		["rec"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Record\n</font><font color='#F272A5'>%s</font>(<V>%s</V>s)!",
		["recguncel"] = "<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Record updated\n</font><font color='#F272A5'>%s</font>(<V>%s</V>s)!",
		["banned"] = "<R>You are banned from fastracing</R>",
		["won"] = "<font color='#F272A5'>%s</font> is winner",
		["alrbanned"] = "<R>This user already banned</R>",
		["urcantban"] = "<R>You can't ban yourself</R>",
		["banlandi"] = "<R>%s banned</R>",
		["banlidegil"] = "<R>This user isn't in BanList</R>",
		["unban"] = "<R>%s unbanned</R>",
		["clog"] = "<R>BanList cleared</R>",
		["bansayi"] = "Banned user count:",
		--skortablo
		["lbbaslik"] = "LEADERBOARD",
		["lbplayer"] = "Player",
		["lbrecord"] = "Record",
		--lsrec
		["xrekor"] = "<font color='#F272A5'>%s</font><font color='#9a9a9a'>'s records</font>:<font color='#F272A5'> %s\n\n</font>",
		["norec"] = "<R>This username hasn't any record.</R>",
		["syntax"] = "<R>Please define username Syntax: !lsrec username </R>",
		["yourrec"] = "<font color='#9a9a9a'>Your records</font>:<font color='#F272A5'> %s\n\n</font>",
		["recinyok"] = "<R>You don't have any record.</R>",
	},
}



local tablo,maplar,kayitlar,bostablo,sayfalar = {},{},{},{},{}
local banlar ={ 
	["Banlilar"] = {},
	["Kayitlar"]={},
	["Yetkililer"] = { 
		["Adminler"] = {["Depwesso"] = true,["Vangoth"] = true,["Napolyy"] = true,}, 
		["Modlar"] = {}, 
	},
} 
--[[ tablo haritalari;
	tablo = {isim,map,sure}
	maplar = maplar[map] = {isim,sure}
	kayitlar = kayitlar[isim] = {map,sure}
	örnekkler=
	tablo = {
		[1] = {"Napolyy",@3131,31.13},
	}
	maplar = {
		[@3131] = {"Napolyy",31.13},
	}
	kayitlar = {
		["Napolyy"] = {
			[1] = {@3131,31.13},
			[2] = {@3132,31.14},
		},
	}
]]	

local first,yuklendi,resim = false,false,false
local mapkod

admin={
    ["Depwesso"] = true,
    ["Hotdexq"] = true, 
    ["Vangoth"] = true,
    ["Quash"] = true,
    ["Joymasq"] = true,
}
sil = { -- burdaki isimlerin recleri map başlangıcında silinir
    ["Myszkaedzio"] = true,
    ["Tamam"] = true,
    ["Lule"] = true,
    ["Vuashimazhan"] = true,
    ["Layrikkk"] = true,
    ["Sawgir"] = true,
    ["+Layrik"] = true,
    ["Layrik"] = true,
    ["Qqqqqqqqqqq"] = true,
    ["Tyebsking"] = true,
    ["Bogagibiboga"] = true,
    ["Maraaakasaaa"] = true,
    ["Sodium"] = true,
    ["Zixyn"] = true,
    ["Krynstop"] = true,
    ["Whistle"] = true,
    ["Mcszaa"] = true,
    ["Xwv"] = true,
    ["Billsko"] = true,
    ["Twnxx"] = true,
    ["St3llro"] = true,
    ["Suatking"] = true,
    ["Nilx"] = true,
    ["Azginkoala"] = true,
    ["Xrg"] = true,
    ["Selambnkaan"] = true,
    ["Berkdxn01"] = true,
    ["Xrgg"] = true,
    ["Pauzywashere"] = true,
    ["Blackpig"] = true,
    ["Darkrabbit"] = true,
    ["Mahmutkx"] = true,
}
levemaplar = {
	"@29415",
	"@29416",
	"@30938",
	"@30408",
	"@27983",
	"@28089",
	"@30934",
}
speedmaplar = {
	"@35723",
}
kodlar = {"rr","levetest","speedtest","npp","lb","lsrec","log","ban","unban","temizle"}

function ceviriYap(metin,isim)
	local diltablo = dilTabloCek(dilCek(isim))
	if isim then
		return diltablo[metin] or "no translate"
	else
		return metin
	end	
end

function mesajAt(metin,isim,...)
	if isim then
		tfm.exec.chatMessage(metin,isim)
	else
		for oyuncu in pairs(tfm.get.room.playerList) do
			tfm.exec.chatMessage(ceviriYap(metin,oyuncu):format(...),oyuncu)
		end
	end	
end

function dilCek(isim)
	if isim then
		return tfm.get.room.playerList[isim].community
	else
		return "en"
	end	
end 

function dilTabloCek(dil)
	if yazilar[tostring(dil)] then  
  		return yazilar[tostring(dil)]
	else
    	return yazilar["en"]
    end
end

function main()
	tfm.exec.disableAutoShaman(true)
	tfm.exec.disablePhysicalConsumables(true)
	tfm.exec.disableAutoTimeLeft(true)
	tfm.exec.disableAutoNewGame(true)
	for i,v in pairs(kodlar) do
		system.disableChatCommandDisplay(v, true)
	end	
	tfm.exec.newGame("#17")
end
	
function eventNewPlayer(name)
	sayfalar[name] = {}
	sayfalar[name].sayfa = 1
	sayfalar[name].sayfalimit = 0
	sayfalar[name].kayitlar = {}
    mesajAt(ceviriYap("hosgeldin",name), name)
	if admin[name] then
		system.bindMouse(name,true)
	end	
end

function rekorYukle(recisim,recsure,data)
	if recsure < 6 or sil[recisim] or banlar["Banlilar"][recisim]  then -- eğer rec 6dan küçükse
		for name in pairs(admin) do -- adminlre yazı at
			mesajAt("<ROSE>[CONSOLE]</ROSE>:<R> Silinen kayıt: "..recisim.."("..recsure.."s) ",name)
		end
		if data then
			system.savePlayerData(mapkod, recisim.." 0")
		end	
		local sira = siraCek(mapkod)
		if sira then
			table.remove(tablo,sira)
		end	
		maplar[mapkod] = nil -- bilgileri temizle
	else	-- eğer 6dan küçül değilse
		if data and yuklendi then
			tabloKaydet(recisim,mapkod,recsure)
		end	
		mesajAt("rec",nil,recisim,recsure)
	end	
end

function eventNewGame()
    mapkod = tfm.get.room.currentMap
    tfm.exec.setGameTime(63, false)
    first = false
	if not maplar[mapkod] then 
		if not system.loadPlayerData(mapkod) then -- eğer kayıt yoksa
			for name in pairs(admin) do -- adminlere yazı at
				mesajAt("<ROSE>[CONSOLE]</ROSE>:<R> Bu haritaya ait kayıt bulunamadı! :(",name)
			end
		end
	else
		local isim,sure = maplar[mapkod].isim,maplar[mapkod].sure -- bilgileri çek
		rekorYukle(isim,sure)
	end	
	if resim then tfm.exec.removeImage(resim) end
	local isim,skor = enBuyukSkorCek()
	if isim then
		resim = tfm.exec.addImage("LuaImage5bf585035e48a8.13686032.png","$"..isim,-21,-100)
	end	
end

function eventPlayerDied(name)
    local plrCount = 0
    for n,p in pairs(tfm.get.room.playerList) do
    	if not p.isDead then
    		plrCount = plrCount + 1
    	end
    end
    if plrCount < 1 then
    	tfm.exec.newGame("#17")
    end
end

function CountPlr()
	local c = 0
	for n,p in pairs(tfm.get.room.playerList) do
		c = c + 1
	end
	return c
end

function enBuyukSkorCek()
	local eisim,eskor = nil,nil
	for isim,p in pairs(tfm.get.room.playerList) do
		if not p.isDead then
			local skor = p.score
			if eskor then
				if eskor < skor then
					eisim,eskor = isim,skor	
				end	
			else
				eisim,eskor = isim,skor	
			end	
		end	
	end
	return eisim,eskor
end

function eventPlayerDataLoaded(isim, data)
	if isim ~= "FRKayit" then
		if isim ~= "FRLogs" then
			for name in pairs(admin) do
				mesajAt("Veri yüklendi: <R>("..data..")", name)
			end
			local sRec = data:find('%s')
			local rec = tonumber(string.sub(data,sRec + 1))
			local recName = string.sub(data,1,sRec -1)
			if not maplar[mapkod] then -- eğer maplar tablosunda değilse map
				rekorYukle(recName,rec,true)
			else
				local isim,sure = maplar[mapkod].isim,maplar[mapkod].sure
				rekorYukle(isim,sure)
			end
		else
			local veriler = json.decode(data)	
			banlar = veriler	
			print("Loglar yuklendi")
			tfm.exec.newGame("#17")	
		end
	else
		verileriYukle(data)
	end	
end

function verileriYukle(veriler)	
	local yuklenen = json.decode(veriler)	
	tablo = yuklenen
	local sayi = 0
	for i,v in pairs(yuklenen) do
		local isim,map,sure = v[1],v[2],v[3]
		maplar[map] = {isim=isim,sure=sure}
		if not kayitlar[isim] then kayitlar[isim] = {} end
		table.insert(kayitlar[isim], {map,sure})	
		sayi = sayi +1	
	end
	print("Rekorlar yüklendi:"..sayi)
	system.loadPlayerData("FRLogs")
	yuklendi = true
end

if not system.loadPlayerData("FRKayit") then
	system.savePlayerData("FRKayit",json.encode(tablo))
	system.savePlayerData("FRLogs",json.encode(banlar))
end


function eventPlayerWon(name,te,tr)
	if CountPlr() >= 0 then
		local tr = tr / 1000 -- 1000 yerine 100 böldük. Eskiden 1000'di! -- zaten 1000 orospu çocuğu
		local tr = tonumber(tr)
		if not first then
			first = true
			local isim,sure = nil,0
			if maplar[mapkod] then
				isim,sure = maplar[mapkod].isim,maplar[mapkod].sure
			end
			if not banlar["Banlilar"][name] then
				if not isim then -- eğer veriler yoksa
					if tr > 6 then
						tabloKaydet(name,mapkod,tr)
						mesajAt("recguncel",nil,name,tr)
					end	
				else -- eğer veriler varsa
					if tr < sure  then 
						if tr > 6 then 
							tabloKaydet(name,mapkod,tr)
							mesajAt("recguncel",nil,name,tr)
						end	
					end
				end
			else
				mesajAt(ceviriYap("banned",name),name)
			end	
	   		mesajAt("won",nil,name)
	   		tfm.exec.setGameTime(4, false)
	   	end
	else
		mesajAt("won",nil,name)
	   	tfm.exec.setGameTime(4, false)
	end
end

function tabloKaydet(isim,map,sure)
	if maplar[map] then	
		local sira = siraCek(map)
		tablo[sira] = {isim,map,sure}
		maplar[map] = {isim=isim,sure=sure}
		print("var")
	else
		table.insert(tablo, {isim,map,sure})
		maplar[map] = {isim=isim,sure=sure}
	end
	system.savePlayerData("FRKayit",json.encode(tablo))
	kayitlar = {}
	for i,v in pairs(tablo)	do
		local isim,map,sure = v[1],v[2],v[3]
		if not kayitlar[isim] then kayitlar[isim] = {} end
		table.insert(kayitlar[isim], {map,sure})	
	end
	-- local mmap,sure = kayitCek(isim,map)
	-- if not mmap then
		-- table.insert(kayitlar[isim], {map,sure})
	-- else
		
	-- end
end

function banla(banlayan,banlanan)
	if banlar["Banlilar"][banlanan] then
		mesajAt(ceviriYap("alrbanned",banlayan),banlayan)
		return
	end	
	if banlayan == banlanan then
		mesajAt(ceviriYap("urcantban",banlayan),banlayan)
		return
	end	
	-- if admin[banlanan] then
		-- mesajAt("<R>Bir yetkiliyi banlayamazsın</R>",banlayan)
		-- return
	-- end	
	banlar["Banlilar"][banlanan] = true
	local yazi = "[BAN] "..banlayan..", banned '"..banlanan..""
	logEkle(yazi)
	recTemizle(banlanan)
	mesajAt(ceviriYap("banlandi",banlayan):format(banlanan),banlayan)
	system.savePlayerData("FRLogs",json.encode(banlar))
end

function banac(banacan,banacilan)
	if not banlar["Banlilar"][banacilan] then
		mesajAt(ceviriYap("banlidegil",banacan),banacan)
		return
	end	
	banlar["Banlilar"][banacilan] = nil
	local yazi = "[UNBAN] "..banacan..", unbanned "..banacilan..""
	logEkle(yazi)
	mesajAt(ceviriYap("unban",banacan):format(banacilan),banacan)
	system.savePlayerData("FRLogs",json.encode(banlar))
end

function logEkle(yazi)
	table.insert(banlar["Kayitlar"],yazi)
end

function recTemizle(isim)
	for i,v in pairs(tablo) do
		local recisim,map = v[1],v[2]
		if recisim == isim then
			table.remove(tablo,i)
			maplar[map] = nil
		end	
	end
	kayitlar = {}
	for i,v in pairs(tablo)	do
		local isim,map,sure = v[1],v[2],v[3]
		if not kayitlar[isim] then kayitlar[isim] = {} end
		table.insert(kayitlar[isim], {map,sure})	
	end
	system.savePlayerData("FRKayit",json.encode(tablo))
end

function mapRecTemizle(mapcode)
	local sira = siraCek(mapcode)
	if sira then
		table.remove(tablo,sira)
	end
	if maplar[mapcode] then
		maplar[mapcode] = nil
	end	
	kayitlar = {}
	for i,v in pairs(tablo)	do
		local isim,map,sure = v[1],v[2],v[3]
		if not kayitlar[isim] then kayitlar[isim] = {} end
		table.insert(kayitlar[isim], {map,sure})	
	end
	system.savePlayerData("FRKayit",json.encode(tablo))
end

function temizle(temizleyen)
	banlar = {["Banlilar"] = {},["Kayitlar"]={}}
	mesajAt(ceviriYap("clog",temizleyen),temizleyen)
	local yazi = "[OH] '"..temizleyen.."' cleared all bans in list"
	table.insert(banlar["Kayitlar"],yazi)
	system.savePlayerData("FRLogs",json.encode(banlar))
end

function loggoster(isim)
	local yazi = "<font color='#F272A5'>"..ceviriYap("bansayi",isim).." %s\n\n</font>"	
	local rkayitlar = table.reverse(banlar["Kayitlar"])
	local sayi = 0
	for i,v in pairs(rkayitlar) do
		yazi = yazi..v.."\n"	
	end
	for i,v in pairs(banlar["Banlilar"]) do sayi = sayi+1 end
	ui.addLog(yazi:format(sayi),isim)
end

function siraCek(map)
	for i,v in pairs(tablo) do
		if v[2] == map then
			return i
		end	
	end
	return false
end	

function kayitCek(isim,map)
	for i,v in pairs(kayitlar[isim]) do
		if v[1] == map then
			return v[1],v[2]
		end	
	end
	return false
end	

function table.reverse(t) 
    local reversedTable = {} 
    local itemCount = #t  
    for k, v in ipairs(t) do 
        reversedTable[itemCount + 1 - k] = v  
    end 
    return reversedTable  
end 

local sx,sy = 800,400
local pg,pu = 410,340
local x,y = (sx-pg)/2,(sy-pu)/2
local ly = y+48

function siralamaGoruntule(kayitlar,isim)
	if bostablo[isim] then
		for i=0,36 do
			ui.removeTextArea(i,isim)
		end
		bostablo[isim] = nil
		return
	end
	bostablo[isim] = true
	local sayfasayi = math.ceil(#kayitlar/10)
	if sayfasayi < 1 then sayfasayi = 1 end	
	
	sayfalar[isim].kayitlar = kayitlar
	sayfalar[isim].sayfa = 1
	sayfalar[isim].sayfalimit = sayfasayi


	ui.addTextArea(0, "<p align='center'><font color='#F272A5'><b>"..ceviriYap("lbbaslik",isim).."</b></font></p>", isim, x,y, pg,pu, 0x111111, 0x111111, 0.9, true)
	ui.addTextArea(1, "" , isim, x+20, y+20, pg-40, 15, 0x111111, 0xFFFFFF, 0.1, true)
	ui.addTextArea(2, "<p align='center'><font color='#F272A5'>"..ceviriYap("lbplayer",isim).."</font></p>" , isim, x-80, y+20, pg-40, nil, 0x111111, 0xFFFFFF, 0, true)
	ui.addTextArea(3, "<p align='center'><font color='#F272A5'>"..ceviriYap("lbrecord",isim).."</font></p>" , isim, x+80, y+20, pg, nil, 0x324650, 0x000000, 0, true)
	ui.addTextArea(35, "<a href='event:geri'><font color='#F272A5'><</a> 1 / "..sayfasayi.." <a href='event:ileri'><b>></b></font></a>" , isim, x+80, pu+10, pg, nil, 0x324650, 0x000000, 0, true)	
	ui.addTextArea(36, "<a href='event:kapat'><font color='#F272A5'>X</font></a>" , isim, (x+pg)-11, y, 12, nil, 0x111111, 0x111111, 1, true)	
	local sira = 10
	if #kayitlar < 10 then
		sira = #kayitlar
	end	
	for i=1,sira do
		local recisim,rec = kayitlar[i].isim,kayitlar[i].kayit
		ui.addTextArea(3+i, string.rep(" ",16).."<font color='#F272A5'><b>"..recisim.."</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0.3, true)
		ui.addTextArea((13+i), "<p align='center'><font color='#F272A5'>"..rec.."</font></p>" , isim,  x+((pg/2)), ly+(27*(i-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 0.3, true)
		ui.addTextArea((24+i), "<font color='#F272A5'><b>"..i.."</font></b>", isim, x+20, ly+(27*(i-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, true)
	end	
end

function sayfaGoster(isim,sayfa,kayitlar)
	local baslangic = (sayfa*10) - 9
	local bitis = (sayfa*10)
	local ikincikayit = {}
	local sira = 0
	local sayfasayi = sayfalar[isim].sayfalimit
	ui.updateTextArea(35, "<a href='event:geri'><font color='#F272A5'><</a> "..sayfa.." / "..sayfasayi.." <a href='event:ileri'><b>></b></font></a>",isim)
	for i=baslangic,bitis do
		sira = sira +1
		if kayitlar[i] then
			local recisim,rec = kayitlar[i].isim,kayitlar[i].kayit
			-- ui.updateTextArea(sira+3, string.rep(" ",16)..recisim,isim)
			-- ui.updateTextArea(sira+13, "<p align='center'>"..rec.."</p>",isim)
			-- ui.updateTextArea(sira+24, "<b>"..i.."</b>",isim)
			ui.addTextArea(sira+3, string.rep(" ",16).."<font color='#F272A5'><b>"..recisim.."</font></b>", isim, x+20, ly+(27*(sira-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0.3, true)
			ui.addTextArea(sira+13, "<p align='center'><font color='#F272A5'>"..rec.."</font></p>" , isim,  x+((pg/2)), ly+(27*(sira-1)), (pg-40)/2, 18, 0xFFFFFF, 0x000000, 0.3, true)
			ui.addTextArea(sira+24, "<font color='#F272A5'><b>"..i.."</font></b>", isim, x+20, ly+(27*(sira-1)), (pg-40)/2-10, 18, 0xFFFFFF, 0x000000, 0, true)
		else
			ui.removeTextArea(sira+3,isim)
			ui.removeTextArea(sira+13,isim)
			ui.removeTextArea(sira+24,isim)
		end	
	end	
end

function eventTextAreaCallback(id, isim, olay)
	if olay == "ileri" then
		sayfalar[isim].sayfa = sayfalar[isim].sayfa+1
		local sonrakisayfa = sayfalar[isim].sayfa 
		local kayitlar = sayfalar[isim].kayitlar
		if sonrakisayfa > sayfalar[isim].sayfalimit then 
			sonrakisayfa = sayfalar[isim].sayfalimit 
			sayfalar[isim].sayfa = sayfalar[isim].sayfalimit 
		end	
		sayfaGoster(isim,sonrakisayfa,kayitlar)
	elseif olay == "geri" then
		sayfalar[isim].sayfa = sayfalar[isim].sayfa-1
		local oncekisayfa = sayfalar[isim].sayfa 
		local kayitlar = sayfalar[isim].kayitlar
		if oncekisayfa < 1 then 
			sayfalar[isim].sayfa = 1
			oncekisayfa = 1
		end	
		sayfaGoster(isim,oncekisayfa,kayitlar)
	elseif olay == "kapat" then
		siralamaGoruntule(nil,isim)
	end
end

function eventChatCommand(name, command)
	local arg={}
	for argument in command:gmatch('[^%s]+') do
	   table.insert(arg,argument)
	end
	if admin[name] then
    	if arg[1] == "rr" and arg[2] ~= nil then
    		if arg[2]:match("@") then
    			system.savePlayerData(arg[2], name .." 0")
				mapRecTemizle(arg[2])
    			mesajAt("<R>Removed Record! <g>: <v>"..arg[2].."</R>",name)
    		end
		elseif arg[1] == "levetest" then
			local randomid = math.random(#levemaplar)
			local randommap = levemaplar[randomid]
			tfm.exec.newGame(randommap)
		elseif arg[1] == "speedtest" then
			local randomid = math.random(#speedmaplar)
			local randommap = speedmaplar[randomid]
			tfm.exec.newGame(randommap)
		elseif arg[1] == "npp" and arg[2] ~= nil then
			if arg[2]:match("@") then
				tfm.exec.newGame(arg[2])	
			end	
		elseif arg[1] == "ban" and arg[2] ~= nil then
			banla(name,arg[2])
		elseif arg[1] == "unban" and arg[2] ~= nil then
			banac(name,arg[2])
		elseif arg[1] == "temizle" then
			temizle(name)	
		elseif arg[1] == "log" then
			loggoster(name)
		 elseif arg[1] == "rectemiz" then
			 --tablo = {}
			 --system.savePlayerData("FRKayit",json.encode(tablo))
    	 end
    end	
	if command=="help" then
		mesajAt("<font color='#A4936F'>\n[FR]</font> <CS>Welcome to Help !</font>\n<font color='#89A7F5'>This purpose The Fast Go to Cheese And hole !", name) 
	elseif command == "lb" then
		--mesajAt("<font color='#636363'>[FR]</font> <font color='#9a9a9a'>Rekorlar;</font><font color='#F272A5'></font>", name)
		local recler = {}
		local siraliRecler = {}
		for i,v in pairs(tablo) do
			local isim, mapkod, sure = v[1],v[2],v[3]
			if not recler[isim] then recler[isim] = 0 end
			recler[isim] = recler[isim] + 1
			--mesajAt("<font color='#636363'></font> <font color='#9a9a9a'></font><font color='#F272A5'>"..isim.."</font>"..mapkod.."(<V>" ..sure.."</V>)", name)
		end
		for i,v in pairs(recler) do table.insert(siraliRecler, {isim=i,kayit=v}) end
		table.sort(siraliRecler, function( a, b ) return( tonumber( a.kayit ) or 0 ) > ( tonumber( b.kayit ) or 0  ) end )
		siralamaGoruntule(siraliRecler,name)
		--for i,v in pairs(siraliRecler) do
			--mesajAt("<font color='#636363'></font> <font color='#9a9a9a'></font><font color='#F272A5'>"..v.isim.."</font> (<V>" ..v.kayit.."</V>)", name)
		--end	
	elseif arg[1] == "lsrec" then
		local isim = arg[2]
		if isim then
			if admin[name] then
				if isim then
					if kayitlar[isim] then
						local yazi = ceviriYap("xrekor",name)
						local sayi = 0
						for i,v in pairs(kayitlar[isim]) do
							local mapkod, sure = v[1],v[2]
							yazi = yazi.." <font color='#F272A5'>"..mapkod.."</font> <font color='#9a9a9a'>- </font><font color='#F272A5'>"..sure.."</font><font color='#9a9a9a'>s</font><font color='#9a9a9a'></font>\n"
							sayi = sayi +1	
						end
						ui.addLog(yazi:format(isim,sayi),name)
					else
						mesajAt(ceviriYap("norec",name),name)
					end
				else
					mesajAt(ceviriYap("syntax",name),name)
				end
			end	
		else
			if kayitlar[name] then
				local yazi = ceviriYap("yourrec",name)
				local lsayi = 0
				for i,v in pairs(kayitlar[name]) do
					local mapkod, sure = v[1],v[2]
					yazi = yazi.." <font color='#F272A5'>"..mapkod.."</font> <font color='#9a9a9a'>- </font><font color='#F272A5'>"..sure.."</font><font color='#9a9a9a'>s</font><font color='#9a9a9a'></font>\n"
					lsayi = lsayi +1					
				end
				ui.addLog(yazi:format(lsayi),name)
			else
				mesajAt(ceviriYap("recinyok",name),name)
			end
		end
	end
end

function eventLoop(ct, tr)
    local tr = tr / 1000
    if tr <= 0 then
    	tfm.exec.newGame("#17")
    end
end

for name in pairs(tfm.get.room.playerList) do
	eventNewPlayer(name)
end

main()

