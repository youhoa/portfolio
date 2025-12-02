import discord
from discord.ext import commands

DEV_ID = 678611431339589642

prefix = "="

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"봇 {bot.user}가 실행되었습니다!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        print(f"DM 메시지 받음: {message.content} (보낸 사람: {message.author})")
        creator = await bot.fetch_user(DEV_ID)
        if creator:
            await creator.send(f"📩 새로운 DM:\n```\n{message.content}\n```\n보낸 사람: {message.author}")

    if bot.user in message.mentions:
        print(f"봇 멘션됨: {message.content} (보낸 사람: {message.author})")
        creator = await bot.fetch_user(DEV_ID)
        if creator:
            await creator.send(f"📣 봇 멘션 알림:\n```\n{message.content}\n```\n보낸 사람: {message.author}")

    await bot.process_commands(message)

    #도움말 =help
@bot.command(name='help', aliases=["h", "도움말"])
async def help_command(ctx):
    embed = discord.Embed(
        title="명령어",
        color=0xFF0000
     )
    embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name=f"{prefix}봇초대 (invite)", value="봇 초대 주소입니다.")
    embed.add_field(name=f"{prefix}help (h)", value="명령어를 보여줍니다.")
    embed.add_field(name=f"{prefix}ping", value=f"봇의 서버핑을 보여줍니다.")
    embed.add_field(name=f"{prefix}주사위", value=f"주사위를 굴려요.")
    embed.add_field(name=f"{prefix}끝말잇기 <단어> ", value=f"진짜 끝말잇기.")
    embed.add_field(name=f"{prefix}아무말", value=f"tmi")
    embed.add_field(name=f"{prefix}겜빈", value=f"써보셈")
    embed.add_field(name=f"{prefix}하령", value=f"써보셈")
    embed.add_field(name=f"{prefix}호아", value=f"써보셈")
    embed.add_field(name=f"{prefix}미적", value=f"써보셈")
    embed.add_field(name=f"{prefix}매혼", value=f"써보셈")


    # embed.timestamp = msg.created_at
    # embed.set_footer(text=f"Made By {BotOwner.name}", icon_url=BotOwner.avatar.url)
    return await ctx.reply(embed=embed)


#주사위 =주사위
@bot.command(name="주사위")
async def roll_dice(ctx):
    import random
    result = random.randint(1, 6)
    await ctx.send(f"🎲 {ctx.author.display_name}님이 주사위를 굴렸습니다! 결과: {result}")

#끝말잇기 =끝말잇기

used_words = []
last_letter = ""

@bot.command()
async def 끝말잇기(ctx, word: str):
    global last_letter

    if used_words and word[0] != last_letter:
        await ctx.send(f"❌ 단어는 '{last_letter}'(으)로 시작해야 해요!")
        return

    if word in used_words:
        await ctx.send("❌ 이미 사용된 단어예요!")
        return

    used_words.append(word)
    last_letter = word[-1]
    await ctx.send(f"✅ '{word}' 접수! 다음 단어는 '{last_letter}'로 시작해야 해요.")

@bot.command()
async def 초기화(ctx):
    global used_words, last_letter
    used_words = []
    last_letter = ""
    await ctx.send("🔄 끝말잇기 게임이 초기화되었습니다!")


#오늘의 아무말 =아무말
@bot.command(name="아무말")
async def nonsense(ctx):
    import random
    phrases = [
            "호아랑 놀아준다고?",
            "미적이랑 놀아준다고?",
            "겜빈이랑 놀아준다고?",
            "하령이랑 놀아준다고?",
            "매혼이랑 놀아준다고?",
            "모카랑 놀아준다고?",
            "이런 명령어 왜 씀",
            "메롱",
            "호아랑 마작할래?",
            "님 바보",
            "you are gay",
            "sex",
            "나랑 쓰껄할래??",
            "야스",
            "발로 개똥망겜",
            "아니 시발 젠지 왜 짐?",
            "아니 시발 젠지 왜 졌음? 내 세상 돌려줘.",
            "어제 내 세상이 무너졌어.",
            "오늘 내 세상이 무너졌어.",
            "내일 내 세상이 무너질 예정이야.",
            "매혼아 스듀 할래?",
            "조르매르매론메료나르까르보",
            "미적아 카스하자!",
            "권하령은 언니야",
            "겜빈형은 감빈셩이야",
            "님들아 마크하자",



        ]
    await ctx.send(random.choice(phrases))


#감빈셩 =겜빈
@bot.command(name="겜빈")
async def nonsense(ctx):
    import random
    phrases = [
            "버즈 최고^^",
            "너 여자야.(?)",
            "발로란트 하자!",
            "게이야..",
            "게이게이야",
            "이리하자!",
            "권용준 병신새끼",
            "앙기모띠",
            "GambinHAL이(가) 게임을 떠났습니다.",
            "게이",
            "겜꼬3",
            "로리",
            "비둘기박이",
            "권하령 씹새끼"


        ]
    await ctx.send(random.choice(phrases))

#궈나령 =하령
@bot.command(name="하령")
async def nonsense(ctx):
    import random
    phrases = [
            "언니~!",
            "너 여자야.(?)",
            "발로란트 하자!",
            "게이야..",
            "게이게이야",
            "이리하자!",
            "이재빈 병신",
            "Ha_ryeongIQ200이(가) 게임을 떠났습니다.",
            "일단 이재빈보다 나은 존재인 건 확실함",
            "유부녀 ntr 장인"



        ]
    await ctx.send(random.choice(phrases))

#유호아 =호아
@bot.command(name="호아")
async def nonsense(ctx):
    import random
    phrases = [
            "알! 빠! 노",
            "너 남자야.(?)",
            "마작 그만해!!!",
            "슈퍼 도파 밍나",
            "호아호아야 이게 무슨소리니",
            "알빠노",
            "뭘 꼬라보노",
            "보노보노 니 얼굴 혼모노",
            "꼬ㅊ"

        ]
    await ctx.send(random.choice(phrases))

#미적이 =미적
@bot.command(name="미적")
async def nonsense(ctx):
    import random
    phrases = [
            "호아랑 마작안해?",
            "너 여자야.(?)",
            "돈 그만 써!",
            "현질 작작해!",
            "발로하자!",
            "카스하자!",
            "작혼하자!",
            "커맨드 만들어줘.",
            "미적분 싫어..",
            "밥 사줘.",
            "밖에 좀 나가!!!!",
            "이새끼 뒤짐",
            "ㄹㅇ 뒤짐",
            "오늘도 뒤짐",
            "내일도 뒤짐",
            "네 부르셨나요",
            "이런 개색",
            "미연시 씹장인"


        ]
    await ctx.send(random.choice(phrases))

#매혼 =매혼
@bot.command(name="매혼")
async def nonsense(ctx):
    import random
    phrases = [
            "너 남자야.(?)",
            "발로란트 하자!",
            "스듀할래?",
            "매혼아, 보고싶어",
            "이리하자!",
            "조까시긔",
            "조르매르매론메료나르까르보야 이게 무슨소리니",
            "이새끼 남자좋아함 ㄹㅇ임",
            "얘 남자 아님 ㄹㅇ임",
            "앙기모찌"


        ]
    await ctx.send(random.choice(phrases))

#모카 =모카
@bot.command(name="모카")
async def nonsense(ctx):
    import random
    phrases = [
            "너 여자야.(?)",
            "너 사실 커피지?",
            "커피사줘.",
            "모카야 붕스할래?",
            "붕스하자!",
            "맥심 좋아하는 새끼",
            "이새끼가 제일 또라이 맞음 ㅇㅇ",
            "카페모카야 이게 무슨소리니",
            "그런사이야?",
            "맥심"


        ]
    await ctx.send(random.choice(phrases))
