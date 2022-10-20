from rubika import Bot
from json import load , dump
import time

bot = Bot("qwwjoxvplvdoxlzbzhuehrwtdxubezlt")
target = "g0CI1L3078c7fb207625dc6360e20de5"


# Coded By : github.com/HiByeDev ~ rubika -> @Develover
# Tnx to github.com/Bahman-ahmadi
# v 1.1 (latest)


def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

def hasAds(msg):
	links = ["rubika.ir/"] # you can develop it
	for i in links:
		if i in msg.lower():
			return True


def searchUserInGroup(guid):
	user = bot.getUserInfo(guid)["data"]["user"]["username"]
	members = bot.getGroupAllMembers(user,target)["in_chat_members"]
	if members != [] and members[0]["username"] == user:
		return True
	
	

# static variable
answered, sleeped, retries = [], False, {}

# option lists
blacklist, exemption, auto_lock , no_alerts , no_stars =  [] , [] , False , [] , []
alerts, stars = {} , {}
auto_lock , locked , gif_lock = False , False , False


# alert function
def alert(guid,user,alert_text=""):
	no_alerts.append(guid)
	alert_count = int(no_alerts.count(guid))

	alerts[user] = alert_count

	max_alert = 5    # you can change it


	if alert_count == max_alert:
		blacklist.append(guid)
		bot.sendMessage(target, "\n 🚫 کاربر [ @"+user+" ] \n ("+ str(max_alert) +") اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .", msg["message_id"])
		bot.banGroupMember(target, guid)
		return

	for i in range(max_alert):
		no = i+1
		if alert_count == no:
			bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n\n"+ str(alert_text) +" شما ("+ str(no) +"/"+ str(max_alert) +") اخطار دریافت کرده اید .\n\nپس از دریافت "+ str(max_alert) +" اخطار ، از گروه اخراج خواهید شد .", msg["message_id"])
			return

# star function
def star(guid,user):
	no_stars.append(guid)
	star_count = int(no_stars.count(guid))
	stars[user] = star_count

	bot.sendMessage(target, "⭐ کاربر @"+ user +" امتیاز دریافت کرد .\n\nتعداد امتیاز های کاربر تا این لحظه = "+ str(star_count), msg["message_id"])
	return


while True:
	if auto_lock:
		if not locked and time.localtime().tm_hour == 00:
			bot.setMembersAccess(target, ["AddMember"])
			bot.sendMessage(target, "⏰ زمان قفل خودکار گروه فرا رسیده است .\n - گروه تا ساعت [ 08:00 ] تعطیل می باشد .")
			locked , sleeped = True , True

		if locked and time.localtime().tm_hour == 8:
			bot.setMembersAccess(target, ["SendMessages","AddMember"])
			bot.sendMessage(target, "⏰ زمان قفل خودکار گروه به پایان رسیده است .\n - اکنون اعضا می توانند در گروه چت کنند .")
			locked , sleeped = False , False		


	# time.sleep(15)
	try:

		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		with open("learn.json","r",encoding="utf-8") as learn:
			data = load(learn)

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				# Check Bot is Sleeped or Not
				if not sleeped:

					# Get Text Messages
					if msg["type"]=="Text" and not msg["message_id"] in answered:


						# Admin Commands
						if msg["author_object_guid"] in admins:

							if msg["text"] == "ربات خاموش" or msg["text"] == "/sleep" :
								sleeped = True
								bot.sendMessage(target, "💤 𝕿𝖍𝖊 𝖇𝖔𝖙 𝖎𝖘 𝖓𝖔𝖜 𝖔𝖋𝖋 .", msg["message_id"])


							elif msg["text"] == "!start" or msg["text"] == "/start" :
								bot.sendMessage(target, "✨ 𝓦𝓮𝓵𝓬𝓸𝓶𝓮 𝓽𝓸 𝓖𝓲𝓰𝓪𝓫𝔂𝓽𝓮.\n\n𝑻𝒐 𝒔𝒆𝒆 𝒕𝒉𝒆 𝒍𝒊𝒔𝒕 𝒐𝒇 𝒃𝒐𝒕 𝒄𝒐𝒎𝒎𝒂𝒏𝒅𝒔, 𝒔𝒆𝒏𝒅 𝒕𝒉𝒆 𝒘𝒐𝒓𝒅 (/panel)..", msg["message_id"])
							
							elif msg["text"].startswith("یادبگیر") or msg["text"].startswith("/learn"):
								try:
									text = msg["text"].replace("یادبگیر ","").replace("/learn ","").split(":")
									word = text[0]
									answer = text[1]

									data[word] = answer
									with open("learn.json","w",encoding="utf-8") as learn:
										dump(data, learn)

									bot.sendMessage(target, "✅ 𝙨𝙖𝙫𝙚𝙙", msg["message_id"])
								except:
									bot.sendMessage(target, "❌ 𝑬𝒓𝒓𝒐𝒓 𝒆𝒙𝒆𝒄𝒖𝒕𝒊𝒏𝒈 𝒕𝒉𝒆 𝒄𝒐𝒎𝒎𝒂𝒏𝒅", msg["message_id"])


							elif msg["text"].startswith("افزودن ادمین") or msg["text"].startswith("/add_admin") :

								try:
									user = msg["text"].replace("افزودن ادمین ","").replace("/add_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										bot.setGroupAdmin(target, guid)
										bot.sendMessage(target, "✅ 𝑼𝒔𝒆𝒓 @"+ str(user) +" 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘢𝘥𝘮𝘪𝘯.", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ɴᴏᴡ ᴀɴ ᴀᴅᴍɪɴ", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										
										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "✅ 𝑼𝒔𝒆𝒓 @"+ str(user) +" 𝘚𝘶𝘤𝘤𝘦𝘴𝘴𝘧𝘶𝘭𝘭𝘺 𝘢𝘥𝘮𝘪𝘯.", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ɴᴏᴡ ᴀɴ ᴀᴅᴍɪɴ", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ ᴇʀʀᴏʀ ᴇxᴇᴄᴜᴛɪɴɢ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ", msg["message_id"])

							elif msg["text"].startswith("حذف ادمین") or msg["text"].startswith("/del_admin") :
								try:
									user = msg["text"].replace("حذف ادمین ","").replace("/del_admin ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]

									if guid in admins :
										bot.deleteGroupAdmin(target, guid)
										bot.sendMessage(target, "✅ 𝑼𝒔𝒆𝒓 @"+ str(user) +" ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴅᴍɪɴ.", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ", msg["message_id"])

								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if not guid in admins :
											bot.setGroupAdmin(target, guid)
											bot.sendMessage(target, "✅ 𝑼𝒔𝒆𝒓 @"+ str(user) +" ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ᴀᴅᴍɪɴ.", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ ᴇʀʀᴏʀ ᴇxᴇᴄᴜᴛɪɴɢ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ", msg["message_id"])
							

							
							elif msg["text"].startswith("/top") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("/top ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if not guid in exemption:
											exemption.append(guid)
											bot.sendMessage(target, "✅ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝘄𝗮𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗲𝘅𝗲𝗺𝗽𝘁𝗲𝗱.", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙣𝙤𝙬 𝙚𝙭𝙚𝙢𝙥𝙩.", msg["message_id"])
								
									else :
										bot.sendMessage(target, "❌ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙖𝙙𝙢𝙞𝙣.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins:
											if not guid in exemption:
												exemption.append(guid)
												bot.sendMessage(target, "✅ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝘄𝗮𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗲𝘅𝗲𝗺𝗽𝘁𝗲𝗱.", msg["message_id"])
											else:
												bot.sendMessage(target, "❌ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙣𝙤𝙬 𝙚𝙭𝙚𝙢𝙥𝙩.", msg["message_id"])

										else :
											bot.sendMessage(target, "❌ ᴛʜᴇ ᴜꜱᴇʀ ɪꜱ ɴᴏᴛ ᴛʜᴇ ᴀᴅᴍɪɴ ᴏꜰ ᴛʜᴇ ɢʀᴏᴜᴘ", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ ᴇʀʀᴏʀ ᴇxᴇᴄᴜᴛɪɴɢ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ", msg["message_id"])


							elif msg["text"].startswith("/untop") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("/untop ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										if guid in exemption:
											exemption.remove(guid)
											bot.sendMessage(target, "✅ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙬𝙖𝙨 𝙧𝙚𝙢𝙤𝙫𝙚𝙙 𝙛𝙧𝙤𝙢 𝙩𝙝𝙚 𝙚𝙭𝙚𝙢𝙥𝙩𝙞𝙤𝙣", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙣𝙤𝙩 𝙚𝙭𝙚𝙢𝙥𝙩.", msg["message_id"])
									else :
										bot.sendMessage(target, "❌ 𝑻𝒉𝒆 𝒖𝒔𝒆𝒓 𝒊𝒔 𝒂𝒅𝒎𝒊𝒏", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins and guid in exemption:
											if guid in exemption:
												exemption.remove(guid)
												bot.sendMessage(target, "✅ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝘄𝗮𝘀 𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗲𝘅𝗲𝗺𝗽𝘁𝗶𝗼𝗻", msg["message_id"])
											else:
												bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗻𝗼𝘁 𝗲𝘅𝗲𝗺𝗽𝘁.", msg["message_id"])

										else :
											bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗮𝗱𝗺𝗶𝗻", msg["message_id"])
									
									except:
										bot.sendMessage(target, "❌ 𝗘𝗿𝗿𝗼𝗿 𝗲𝘅𝗲𝗰𝘂𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱", msg["message_id"])
							

							
							elif msg["text"] == "لیست امتیاز" or msg["text"] == "/star_list":
								try:
									text = "💎 𝘭𝘪𝘴𝘵 𝘰𝘧 𝘱𝘳𝘪𝘷𝘪𝘭𝘦𝘨𝘦𝘴 𝘰𝘧 𝘨𝘳𝘰𝘶𝘱 𝘶𝘴𝘦𝘳𝘴 :\n\n"
									stars_list = ""
									for i in stars:
										stars_list += (" - @"+i+" \t= "+str(stars[i])+"\n")
									bot.sendMessage(target, text + str(stars_list), msg["message_id"])
								except:
									bot.sendMessage(target, "❌ 𝙀𝙧𝙧𝙤𝙧 𝙚𝙭𝙚𝙘𝙪𝙩𝙞𝙣𝙜 𝙩𝙝𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙", msg["message_id"])
							
							
							elif msg["text"] == "لیست اخطار" or msg["text"] == "/alert_list":
								try:
									text = "⚠ 𝗟𝗶𝘀𝘁 𝗼𝗳 𝗴𝗿𝗼𝘂𝗽 𝘂𝘀𝗲𝗿 𝘄𝗮𝗿𝗻𝗶𝗻𝗴𝘀 :\n\n"
									alert_list = ""
									for i in alerts:
										alert_list += (" - @"+i+" \t= "+str(alerts[i])+"\n")
									bot.sendMessage(target, text + str(alert_list), msg["message_id"])
								except:
									bot.sendMessage(target, "❌ 𝗘𝗿𝗿𝗼𝗿 𝗲𝘅𝗲𝗰𝘂𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱", msg["message_id"])

							
							elif msg["text"].startswith("حذف اخطار") or msg["text"].startswith("/del_alert"):
								try:
									user = msg["text"].replace("حذف اخطار ","").replace("/del_alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if guid in no_alerts:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										alerts[user] = 0
										bot.sendMessage(target, "✅ ᵁˢᵉʳ ʷᵃʳⁿⁱⁿᵍˢ ʷᵉʳᵉ ʳᵉᵐᵒᵛᵉᵈ.", msg["message_id"])
									else:
										bot.sendMessage(target, "❌ ᵀʰᵉ ᵘˢᵉʳ ʰᵃˢ ⁿᵒ ʷᵃʳⁿⁱⁿᵍ.", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]

										if guid in no_alerts:
											for i in range(no_alerts.count(guid)):
												no_alerts.remove(guid)
											alerts[user] = 0
											bot.sendMessage(target, "✅ 𝗨𝘀𝗲𝗿 𝘄𝗮𝗿𝗻𝗶𝗻𝗴𝘀 𝘄𝗲𝗿𝗲 𝗿𝗲𝗺𝗼𝘃𝗲𝗱.", msg["message_id"])
										else:
											bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗵𝗮𝘀 𝗻𝗼 𝘄𝗮𝗿𝗻𝗶𝗻𝗴.", msg["message_id"])

									except:
										bot.sendMessage(target, "❌ 𝗣𝗹𝗲𝗮𝘀𝗲 𝗲𝗻𝘁𝗲𝗿 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗰𝗼𝗿𝗿𝗲𝗰𝘁𝗹𝘆", msg["message_id"])
								


							elif msg["text"].startswith("اخطار")  or msg["text"].startswith("/alert"):
								try:
									user = msg["text"].replace("اخطار ","").replace("/alert ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									
									if not guid in admins :
										alert(guid,user)
									else :
										bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗮𝗱𝗺𝗶𝗻", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										if not guid in admins:
											alert(guid,user)
										else:
											bot.sendMessage(target, "❌ 𝐓𝐡𝐞 𝐮𝐬𝐞𝐫 𝐢𝐬 𝐚𝐝𝐦𝐢𝐧", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ 𝐄𝐫𝐫𝐨𝐫 𝐞𝐱𝐞𝐜𝐮𝐭𝐢𝐧𝐠 𝐭𝐡𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝", msg["message_id"])
							
							
							
							elif msg["text"].startswith("حالت آرام") or msg["text"].startswith("/slow"):
								try:
									number = int(msg["text"].replace("حالت آرام ","").replace("/slow ",""))

									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "⏰ 𝘾𝙖𝙡𝙢 𝙢𝙤𝙙𝙚 𝙛𝙤𝙧 "+str(number)+"𝘀𝗲𝗰𝗼𝗻𝗱𝘀 𝗮𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱", msg["message_id"])

								except:
									bot.sendMessage(target, "❌ 𝘌𝘳𝘳𝘰𝘳 𝘦𝘹𝘦𝘤𝘶𝘵𝘪𝘯𝘨 𝘵𝘩𝘦 𝘤𝘰𝘮𝘮𝘢𝘯𝘥", msg["message_id"])
								
							elif msg["text"] == "حذف حالت آرام" or msg["text"] == "/off_slow":
								try:
									number = 0
									bot.setGroupTimer(target,number)

									bot.sendMessage(target, "⏰ 𝗤𝘂𝗶𝗲𝘁 𝗺𝗼𝗱𝗲 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱", msg["message_id"])
								except:
									bot.sendMessage(target, "❌ ᴱʳʳᵒʳ ᵉˣᵉᶜᵘᵗⁱⁿᵍ ᵗʰᵉ ᶜᵒᵐᵐᵃⁿᵈ", msg["message_id"])
								
							# elif msg["text"] == "قفل گیف" or msg["text"] == "/gif_lock":
							# 	gif_lock = True
							# 	bot.sendMessage(target, "✅ قفل گیف و استیکر فعال شد .", msg["message_id"])

							
							# elif msg["text"] == "حذف قفل گیف" or msg["text"] == "/del_gif_lock":
							# 	gif_lock = False
							# 	bot.sendMessage(target, "✅ قفل گیف و استیکر غیرفعال شد .", msg["message_id"])


							elif msg["text"] == "قفل خودکار" or msg["text"] == "/auto_lock":
								try:
									auto_lock = True
									# time = msg["text"].split(" ")[2].split(":") start=time[0] , end=time[1]
									start = "00:00"
									end = "08:00"
									# open("time.txt","w").write(start +"-"+ end)
									bot.sendMessage(target, "�̲�̲ ̲ق̲ف̲ل̲ ̲خ̲و̲د̲ک̲ا̲ر̲ ̲ب̲ر̲ا̲ی̲ ̲گ̲ر̲و̲ه̲ ̲ف̲ع̲ا̲ل̲ ̲ش̲د̲ . \n\n گ̲ر̲و̲ه̲ ̲س̲ا̲ع̲ت̲ [ "+ start +" ] ق̲ف̲ل̲ ̲خ̲و̲ا̲ه̲د̲ ̲ش̲د̲ \n و̲ ̲د̲ر̲ ̲س̲ا̲ع̲ت̲ [ "+ end +" ] ب̲ا̲ز̲ ̲خ̲و̲ا̲ه̲د̲ ̲ش̲د̲ .", msg["message_id"])
										
								except:
									bot.sendMessage(target, "❌ 𝙀𝙧𝙧𝙤𝙧 𝙚𝙭𝙚𝙘𝙪𝙩𝙞𝙣𝙜 𝙩𝙝𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙", msg["message_id"])

							
							elif msg["text"] == "حذف قفل خودکار" or msg["text"] == "/del_auto_lock":
								auto_lock = False
								bot.sendMessage(target, "🔓 ق̲ف̲ل̲ ̲خ̲و̲د̲ک̲ا̲ر̲ ̲ب̲ر̲د̲ا̲ش̲ت̲ه̲ ̲ش̲د̲ .", msg["message_id"])


							elif msg["text"].startswith("اخراج") or msg["text"].startswith("/ban") :
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("اخراج ","").replace("/ban ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
									if not guid in admins :
										bot.banGroupMember(target, guid)
										bot.sendMessage(target, "✅ 𝐓𝐡𝐞 𝐮𝐬𝐞𝐫 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐤𝐢𝐜𝐤𝐞𝐝 𝐨𝐮𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐩", msg["message_id"])
									else :
										bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗮𝗱𝗺𝗶𝗻", msg["message_id"])
										
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										if not guid in admins :
											bot.banGroupMember(target, guid)
											bot.sendMessage(target, "𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙝𝙖𝙨 𝙗𝙚𝙚𝙣 𝙨𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙠𝙞𝙘𝙠𝙚𝙙 𝙤𝙪𝙩 𝙤𝙛 𝙩𝙝𝙚 𝙜𝙧𝙤𝙪𝙥", msg["message_id"])
										else :
											bot.sendMessage(target, "❌ 𝗧𝗵𝗲 𝘂𝘀𝗲𝗿 𝗶𝘀 𝗮𝗱𝗺𝗶𝗻", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ 𝗘𝗿𝗿𝗼𝗿 𝗲𝘅𝗲𝗰𝘂𝘁𝗶𝗻𝗴 𝘁𝗵𝗲 𝗰𝗼𝗺𝗺𝗮𝗻𝗱", msg["message_id"])

							
							elif msg["text"].startswith("حذف") or msg["text"].startswith("/del"):
								try:
									number = int(msg["text"].replace("حذف ","/del").replace("/del ",""))
									if number > 50:
										bot.sendMessage(target, "❌ 𝐓𝐡𝐞 𝐫𝐨𝐛𝐨𝐭 𝐨𝐧𝐥𝐲 𝐝𝐞𝐥𝐞𝐭𝐞𝐬 𝐮𝐩 𝐭𝐨 𝟓𝟎 𝐫𝐞𝐜𝐞𝐧𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞𝐬 .", msg["message_id"])
									else:
										answered.reverse()
										bot.deleteMessages(target, answered[0:number])

										bot.sendMessage(target, "✅ "+ str(number) +" 𝗧𝗵𝗲 𝗹𝗮𝘀𝘁 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘄𝗮𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗱𝗲𝗹𝗲𝘁𝗲𝗱", msg["message_id"])
										answered.reverse()

								except:
									try:
										bot.deleteMessages(target, [msg["reply_to_message_id"]])
										bot.sendMessage(target, "✅ 𝗧𝗵𝗲 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘄𝗮𝘀 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗱𝗲𝗹𝗲𝘁𝗲𝗱", msg["message_id"])
									except:
										bot.sendMessage(target, "❌ 𝙀𝙧𝙧𝙤𝙧 𝙚𝙭𝙚𝙘𝙪𝙩𝙞𝙣𝙜 𝙩𝙝𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙", msg["message_id"])

							
							elif msg["text"].startswith("آپدیت قوانین") or msg["text"].startswith("/update_rules"):
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg["text"].replace("آپدیت قوانین","").replace("/update_rules","")))
								bot.sendMessage(target, "✅𝐓𝐡𝐞 𝐫𝐮𝐥𝐞𝐬 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐮𝐩𝐝𝐚𝐭𝐞𝐝", msg["message_id"])
								# rules.close()							                           
                            
							elif msg["text"].startswith("امتیاز") or msg["text"].startswith("/star"):
								try:
									user = msg["text"].replace("امتیاز ","").replace("/star ","")[1:]
									guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
									star(guid,user)
									
								except:
									try:
										guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
										user = bot.getUserInfo(guid)["data"]["user"]["username"]
										star(guid,user)
									except:
										bot.sendMessage(target, "❌ 𝑬𝒓𝒓𝒐𝒓 𝒆𝒙𝒆𝒄𝒖𝒕𝒊𝒏𝒈 𝒕𝒉𝒆 𝒄𝒐𝒎𝒎𝒂𝒏𝒅", msg["message_id"])

							
							
							elif msg["text"] == "lock/" or msg["text"] == "/lock":
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐰𝐚𝐬 𝐥𝐨𝐜𝐤𝐞𝐝", msg["message_id"])

                            elif msg["text"] == "قوانین":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()
                            
							elif msg["text"] == "unlock/" or msg["text"] == "/unlock" :
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 𝐓𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐢𝐬 𝐧𝐨𝐰 𝐨𝐩𝐞𝐧", msg["message_id"])
							

							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										for i in range(no_alerts.count(guid)):
											no_alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.invite(target, [guid])
									
								except:
									bot.sendMessage(target, "❌ 𝙀𝙧𝙧𝙤𝙧 𝙚𝙭𝙚𝙘𝙪𝙩𝙞𝙣𝙜 𝙩𝙝𝙚 𝙘𝙤𝙢𝙢𝙖𝙣𝙙", msg["message_id"])
							
							elif msg["text"] == "/ruls":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
                                # rules.close() 	
					
						# User Commands
						else:

							if hasAds(msg["text"]) and not msg["author_object_guid"] in exemption:
								guid = msg["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								bot.deleteMessages(target, [msg["message_id"]])
								alert(guid,user,"𝐏𝐨𝐬𝐭𝐢𝐧𝐠 𝐥𝐢𝐧𝐤𝐬 𝐢𝐧 𝐭𝐡𝐞 𝐠𝐫𝐨𝐮𝐩 𝐢𝐬 𝐩𝐫𝐨𝐡𝐢𝐛𝐢𝐭𝐞𝐝! .\n\n")
							
							elif msg["text"] == "/panel":
								commands = open("commands.txt","r",encoding='utf-8').read()
								bot.sendMessage(target,str(commands),msg["message_id"])
                            
							elif msg["text"] == "/ruls":
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), msg["message_id"])
								# rules.close()

							elif msg["text"].startswith("افزودن") or msg["text"].startswith("/add"):
								try:
									guid = bot.getInfoByUsername(msg["text"].replace("افزودن ","").replace("/add ","")[1:])["data"]["chat"]["object_guid"]
									if guid in blacklist:
										bot.sendMessage(target, "❌ 𝘛𝘩𝘦 𝘶𝘴𝘦𝘳 𝘪𝘴 𝘪𝘯 𝘵𝘩𝘦 𝘣𝘭𝘢𝘤𝘬 𝘭𝘪𝘴𝘵 𝘢𝘯𝘥 𝘰𝘯𝘭𝘺 𝘵𝘩𝘦 𝘢𝘥𝘮𝘪𝘯 𝘤𝘢𝘯 𝘢𝘥𝘥 𝘵𝘩𝘦 𝘱𝘦𝘳𝘴𝘰𝘯 𝘵𝘰 𝘵𝘩𝘦 𝘨𝘳𝘰𝘶𝘱.", msg["message_id"])
									else:
										bot.invite(target, [guid])
										bot.sendMessage(target, "✅ 𝙏𝙝𝙚 𝙪𝙨𝙚𝙧 𝙞𝙨 𝙣𝙤𝙬 𝙖 𝙢𝙚𝙢𝙗𝙚𝙧 𝙤𝙛 𝙩𝙝𝙚 𝙜𝙧𝙤𝙪𝙥", msg["message_id"])
									
								except:
									bot.sendMessage(target, "❌ 𝘌𝘳𝘳𝘰𝘳 𝘦𝘹𝘦𝘤𝘶𝘵𝘪𝘯𝘨 𝘤𝘰𝘮𝘮𝘢𝘯𝘥", msg["message_id"])

							elif msg["text"] == "/link":
								group = bot.getGroupLink(target)["data"]["join_link"]
								bot.sendMessage(target, "🔗 𝐆𝐫𝐨𝐮𝐩 𝐥𝐢𝐧𝐤 :\n"+str(group), msg["message_id"])
                            
							for i in data.keys():
								if i == msg["text"]:
									bot.sendMessage(target, str(data[i]), msg["message_id"])



					elif msg["type"]=="Event" and not msg["message_id"] in answered:
						answered.append(msg["message_id"])

						name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
						data = msg['event_data']
						if data["type"]=="RemoveGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"🚨 𝘂𝘀𝗲𝗿 {user} 𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗿𝗲𝗺𝗼𝘃𝗲𝗱 𝗳𝗿𝗼𝗺 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽 .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="AddedGroupMembers":
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n • به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						
						elif data["type"]=="LeaveGroup":
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"خدانگهدار {user} 👋 ", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							
						elif data["type"]=="JoinedGroupByLink":
							guid = data['performer_object']['object_guid']
							user = bot.getUserInfo(guid)["data"]["user"]["first_name"]
							bot.sendMessage(target, f"سلام {user} عزیز 🌹 \n• به گروه {name} خوش اومدی 😍 \n 📿 لطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی .", msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
							if guid in blacklist:
								for i in range(no_alerts.count(guid)):
									no_alerts.remove(guid)
								blacklist.remove(guid)
					
					# elif msg["type"]=="Gif" or msg["type"]=="Sticker" and not msg["message_id"] in answered:
					# 	if gif_lock and not msg["author_object_guid"] in admins:
					# 		guid = msg["author_object_guid"]
					# 		user = bot.getUserInfo(guid)["data"]["user"]["username"]
					# 		bot.deleteMessages(target, [msg["message_id"]])
					# 		alert(guid,user,"ارسال گیف و استیکر در گروه ممنوع میباشد .")

					else:
						if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg["message_id"]])[0]["forwarded_from"]["type_from"] == "Channel" and not msg["author_object_guid"] in exemption:
							bot.deleteMessages(target, [msg["message_id"]])
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg["message_id"]])
							alert(guid,user,"𝗙𝗼𝗿𝘄𝗮𝗿𝗱𝗶𝗻𝗴 𝗺𝗲𝘀𝘀𝗮𝗴𝗲𝘀 𝗶𝗻 𝘁𝗵𝗲 𝗴𝗿𝗼𝘂𝗽 𝗶𝘀 𝗽𝗿𝗼𝗵𝗶𝗯𝗶𝘁𝗲𝗱 .\n\n")
						
						answered.append(msg["message_id"])
						continue
				
				else:
					if msg["text"] == "ربات روشن" or msg["text"] == "/wakeup":
						sleeped = False
						bot.sendMessage(target, "✅ 𝐓𝐡𝐞 𝐫𝐨𝐛𝐨𝐭 𝐢𝐬 𝐧𝐨𝐰 𝐨𝐧 .", msg["message_id"])
					
			except:
				continue

			answered.append(msg["message_id"])
			print("[" + msg["message_id"]+ "] >>> " + msg["text"] + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
