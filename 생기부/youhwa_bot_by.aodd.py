#외부 모듈
import discord
from discord.ext import commands

#내부 모듈
from time import time, localtime, strftime
import random
import asyncio

#사용자 정의 모듈
from helpers import logUtils as log
from helpers.config import conf

st = int(time()) #시작 시간
conf = conf("config.json") #config.json 에서 설정을 가져옴
token = conf["DISCORD_BOT_TOKEN"] #봇 토큰을 config.json 에서 가져옴
prefix = conf["PREFIX"] #prefix 를 config.json 에서 가져옴
DEV_ID = conf["DEV_ID"] #DEV_ID 를 config.json 에서 가져옴

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.dm_messages = True
intents.messages = intents.guilds = intents.guild_messages = intents.voice_states = True #한번에 True

bot = commands.Bot(command_prefix=prefix, intents=intents, help_command=None)

creator = None
async def fetchOwner(): global creator; creator = await bot.fetch_user(DEV_ID)

@bot.event
async def on_ready():
    log.info(f"봇 {bot.user}가 실행되었습니다!")

    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(
        type=discord.ActivityType.listening, #봇의 상태가 하는중 으로 지정
        name='멍 때리기' #봇의 상태 메시지
    ))
    await fetchOwner() #개발자 정보를 봇 시작과 함께 가져옴

    #슬래시 커맨드
    try:
        synced = await bot.tree.sync()  # 슬래시 커맨드 동기화
        print(f"슬래시 명령어 {len(synced)}개 동기화 완료!")
    except Exception as e:
        print(f"동기화 오류: {e}")



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        log.info(f"DM 메시지 받음: {message.content} (보낸 사람: {message.author})")

        if not creator:
            await fetchOwner()

        await creator.send(f"📩 새로운 DM:\n```\n{message.content}\n```\n보낸 사람: {message.author}")

    if bot.user in message.mentions:
        log.info(f"봇 멘션됨: {message.content} (보낸 사람: {message.author})")
        if not creator:
            await fetchOwner()

        await creator.send(f"📣 봇 멘션 알림:\n```\n{message.content}\n```\n보낸 사람: {message.author}")

    await bot.process_commands(message)

#도움말 !help
# 공통 동작을 함수로 분리
async def send_help_embed(ctx_or_interaction, is_slash=False):
    embed = discord.Embed(
        title="명령어",
        color=0xFF0000
    )
    embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)

    embed.add_field(name=f"{prefix}invite", value="봇 초대 주소입니다.")
    embed.add_field(name=f"{prefix}help (h)", value="명령어를 보여줍니다.")
    embed.add_field(name=f"{prefix}ping", value="봇의 서버핑을 보여줍니다.")
    embed.add_field(name=f"{prefix}주사위", value="주사위를 굴려요.")
    embed.add_field(name=f"{prefix}밸런스", value="밸런스 게임")
    embed.add_field(name=f"{prefix}아무말", value="tmi")
    embed.add_field(name=f"{prefix}점메추", value="ㅈㄱㄴ")
    embed.add_field(name=f"{prefix}저메추", value="ㅈㄱㄴ22 (더 다양함)")
    embed.add_field(name=f"{prefix}블랙잭", value="ㅈㄱㄴ333")

    now = discord.utils.utcnow()
    embed.timestamp = now
    embed.set_footer(text=f"Made By {creator.name}", icon_url=creator.avatar.url)

    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.reply(embed=embed)

        # 슬래시 명령어
@bot.tree.command(name="도움말", description="명령어를 보여드립니다.")
async def 도움말(interaction: discord.Interaction):
    await send_help_embed(interaction, is_slash=True)

#주사위 !주사위
@bot.command(name="주사위")
async def roll_dice(ctx):
    result = random.randint(1, 6)
    await ctx.send(f"🎲 {ctx.author.display_name}님이 주사위를 굴렸습니다! 결과: {result}")

#밸런스게임 !밸런스
@bot.command(name="밸런스")
async def balance_game(ctx):
    questions = [
        "평생 초콜릿만 먹기 vs 평생 라면만 먹기",
        "투명인간이 되기 vs 하늘을 날 수 있기",
        "공부 안 해도 전교 1등 vs 운동 안 해도 전국 1등",
        "스마트폰 없이 살기 vs 인터넷 없이 살기",
        "호아랑 마작하기 vs 호아랑 유니티 하기"
    ]
    question = random.choice(questions)
    await ctx.send(f"🔥 밸런스 게임! 무엇을 선택하시겠습니까?\n👉 {question}")

#오늘의 아무말 !아무말
@bot.command(name="아무말")
async def nonsense(ctx):
    phrases = [
        "호아랑 놀아준다고?",
        "이런 명령어 왜 씀",
        "메롱",
        "나랑 마작할래?",
        "님 바보",
        "https://www.instagram.com/reel/DLGtkpAPMrl/?igsh=MXFhYm4xc29vaG53dA%3D%3D",
        "호아랑 놀아줘",
        "호아 심심하대"
    ]
    await ctx.send(random.choice(phrases))

#점메추 !점메추
@bot.command(name="점메추")
async def nonsense(ctx):
    phrases = [
        "된장찌개",
        "오징어볶음",
        "제육볶음",
        "덮밥",
        "한정식",
        "김치찌개",
        "보쌈",
        "편의점도시락",
        "라면",
        "빵",
        "떡볶이",
        "김밥",
        "바나나",
        "수박",
        "사과",
        "굶어. 돈 아껴야지."
    ]
    await ctx.send(random.choice(phrases))

#저메추 !저메추
@bot.command(name="저메추")
async def nonsense(ctx):
    import random
    phrases = [
            "된장찌개",
            "치킨",
            "덮밥",
            "피자",
            "초밥",
            "빵",
            "오징어볶음",
            "불고기",
            "안먹기",
            "규동",
            "돈 아껴.",
            "먹지마",
            "호아 밥 사주기",
            "김치찌개",
            "보쌈",
            "라면",
            "편의점도시락",
            "여우",
            "순대",
            "떡볶이",
            "김밥",
            "바나나",
            "수박",
            "사과",
            "햄버거",
            "마라탕",
            "마라샹궈",
            "쭈꾸미볶음",
            "뼈해장국",
            "감자탕",
            "설렁설렁 설렁탕",
            "순댓국",
            "굶어. 돈 아껴야지."
        ]
    await ctx.send(random.choice(phrases))


#블랙잭 (!블랙잭)

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

def calculate_score(hand):
    score, aces = 0, 0
    for card in hand:
        rank = card[:-1]
        if rank in ['J','Q','K']:
            score += 10
        elif rank == 'A':
            score += 11; aces += 1
        else:
            score += int(rank)
    while score > 21 and aces:
        score -= 10; aces -= 1
    return score

# key: ctx.channel.id, value: game info
games = {}


@bot.command(aliases=["qmfforwor","블렉잭"])
async def 블랙잭(ctx):
    """새 게임 생성: !시작"""
    if ctx.channel.id in games:
        await ctx.send("이미 게임이 진행 중입니다!")
        return
    
    games[ctx.channel.id] = {
        'deck': [],
        'players': {},  # user_id: {'hand':[], 'chips':100, 'bet':0}
        'state': 'joining'
    }
    await ctx.send("블랙잭 게임을 시작합니다! 참여하려면 `!참가` 해주세요. 준비되면 `!베팅시작`")

@bot.command(aliases=["ckark"])
async def 참가(ctx):
    """게임 참여: !참가"""
    g = games.get(ctx.channel.id)
    if not g or g['state'] != 'joining':
        await ctx.send("현재 참가할 수 있는 게임이 없습니다.")
        return
    if ctx.author.id in g['players']:
        await ctx.send("이미 참여하셨습니다!")
        return
    g['players'][ctx.author.id] = {'hand': [], 'chips': 100, 'bet': 0}
    await ctx.send(f"{ctx.author.mention}님, 칩 100개로 참가 완료!")

@bot.command(aliases=["qpxldtlwkr","베팅시작"])
async def 배팅시작(ctx):
    """베팅 라운드 시작: !베팅시작"""
    g = games.get(ctx.channel.id)
    if not g or g['state'] != 'joining':
        await ctx.send("게임을 시작할 수 없습니다.")
        return
    if len(g['players']) < 1:
        await ctx.send("최소 1명 이상의 참가자가 필요합니다.")
        return
    g['state'] = 'betting'
    await ctx.send("베팅을 시작합니다! 예: `!베팅 20` (각자 칩에 따라 베팅하세요)")

@bot.command(aliases=["qpxld","배팅"])
async def 베팅(ctx, amount: int):
    """플레이어 베팅: !베팅 20"""
    g = games.get(ctx.channel.id)
    if not g or g['state'] != 'betting':
        await ctx.send("지금은 베팅할 수 없습니다.")
        return
    p = g['players'].get(ctx.author.id)
    if not p:
        await ctx.send("참가자가 아닙니다.")
        return
    if amount <= 0 or amount > p['chips']:
        await ctx.send("유효하지 않은 베팅 금액입니다.")
        return
    p['bet'] = amount
    await ctx.send(f"{ctx.author.mention}님, {amount}칩 베팅 완료!")
    if all(pl['bet'] > 0 for pl in g['players'].values()):
        await start_game(ctx)

async def start_game(ctx):
    g = games[ctx.channel.id]
    g['state'] = 'playing'
    g['deck'] = [f"{r}{s}" for r in ranks for s in suits]
    random.shuffle(g['deck'])
    g['dealer'] = {'hand': []}
    # 딜 초기 분배
    for pid, pl in g['players'].items():
        pl['hand'] = [g['deck'].pop(), g['deck'].pop()]
    g['dealer']['hand'] = [g['deck'].pop(), g['deck'].pop()]
    
    # 각 플레이어 턴 시작
    for pid, pl in g['players'].items():
        user = await bot.fetch_user(pid)
        await ctx.send(f"{user.mention} 카드: {pl['hand']} (합계: {calculate_score(pl['hand'])}) – `!히트` 또는 `!스탠드` 주세요.")
    # 딜러는 자동 처리
    await ctx.send("모든 플레이어는 각자 `!히트` 또는 `!스탠드`를 입력하세요.")

@bot.command(aliases=["glxm"])
async def 히트(ctx):
    """플레이어 히트: !히트"""
    g = games.get(ctx.channel.id)
    if not g or g['state'] != 'playing':
        await ctx.send("지금은 히트할 수 없습니다.")
        return
    p = g['players'].get(ctx.author.id)
    if not p:
        await ctx.send("참가자가 아닙니다.")
        return
    p['hand'].append(g['deck'].pop())
    score = calculate_score(p['hand'])
    await ctx.send(f"{ctx.author.mention} 카드: {p['hand']} (합계: {score})")
    if score > 21:
        await ctx.send(f"{ctx.author.mention} 파산! (버스트)")
        # 자동 스탠드 처리
        await stand_player(ctx.author.id, ctx)

@bot.command(aliases=["tmxosem","스텐드"])
async def 스탠드(ctx):
    """플레이어 스탠드: !스탠드"""
    g = games.get(ctx.channel.id)
    if not g or g['state'] != 'playing':
        await ctx.send("지금은 스탠드할 수 없습니다.")
        return
    if ctx.author.id not in g['players']:
        await ctx.send("참가자가 아닙니다.")
        return
    await stand_player(ctx.author.id, ctx)

async def stand_player(player_id, ctx):
    g = games[ctx.channel.id]
    p = g['players'][player_id]
    p['finished'] = True
    if all(pl.get('finished') or calculate_score(pl['hand']) > 21 for pl in g['players'].values()):
        await dealer_play(ctx)

async def dealer_play(ctx):
    g = games[ctx.channel.id]
    dh = g['dealer']['hand']
    while calculate_score(dh) < 17:
        dh.append(g['deck'].pop())
    dealer_score = calculate_score(dh)
    # 판정
    msg = f"딜러 카드: {dh} (합계: {dealer_score})\n"
    for pid, p in g['players'].items():
        user = await bot.fetch_user(pid)
        ps = calculate_score(p['hand'])
        if ps > 21:
            result = "패 (버스트)"
        elif dealer_score > 21 or ps > dealer_score:
            result = "승"
            p['chips'] += p['bet']
        elif ps == dealer_score:
            result = "무"
        else:
            result = "패"
            p['chips'] -= p['bet']
        msg += f"{user.mention}: 패 {p['hand']} (합 {ps}) – 베팅 {p['bet']} → {result}, 남은 칩 {p['chips']}\n"
    await ctx.send(msg)
    del games[ctx.channel.id]

#봇 초대 명령어
@bot.command(name="invite")
async def inviteBot(ctx):
    embed = discord.Embed(
        title="봇 초대 링크 생성 (Bot Permissions)",
        color=0xFF0000
    )
    embed.set_author(name=bot.user, icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.add_field(name=f"1. Administrator", value="관리자 권한으로 초대링크 생성됨 (8)", inline=False)
    embed.add_field(name=f"2. 메시지 전송 및 관리, 음성채팅 연결 및 말하기", value="해당 권한으로 초대링크 생성됨 (277028562944)", inline=False)
    embed.add_field(name=f"0. 생성취소", value="링크 생성을 취소합니다. (또는 30초 경과시 자동 취소됨)", inline=False)

    embed.timestamp = ctx.message.created_at
    embed.set_footer(text=f"Made By {creator.name}", icon_url=creator.avatar.url)
    srmsg = await ctx.reply(embed=embed)

    def ucs(m): return m.author == ctx.message.author and m.content.isdigit()
    try:
        umsg = await bot.wait_for("message", timeout=30, check=ucs)
        idx = int(umsg.content)
        await srmsg.delete(); await umsg.delete()
        if idx == 0: return
        elif idx == 1: perm = 8; pt = "관리자"
        elif idx == 2: perm = 277028562944; pt = "메시지 전송 및 관리, 음성채팅 연결 및 말하기"
        return await ctx.reply(f"{pt} 권한으로 링크 생성 완료!\nhttps://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions={perm}&scope=bot+applications.commands")
    except asyncio.TimeoutError: await ctx.reply("곡 선택 시간이 초과되었습니다. 다시 시도해주세요!"); await srmsg.delete(); return

#ping 명령어
@bot.command(name="ping", aliases=["핑"])
async def ping(ctx):
    ping = f"서버 핑은 **{round(bot.latency * 1000)}ms** 입니다."; log.info(ping)
    await ctx.reply(ping)


bot.run(token)  

