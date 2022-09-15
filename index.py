import discord
from discord.ext import commands, tasks
from itertools import cycle
from to2 import Token #take token from to2

intents = discord.Intents.all()
bot=commands.Bot(command_prefix='/', intents=intents)

async def level_setter(message, historic = False) :
    if message.author.id in [159985870458322944,370438600430583809] and '레벨' in message.content and '입니다!' in message.content :
        print('미육이 레벨 채팅 인식')
        member = message.mentions[0]
        x = message.content.split(' ')
        x = x[-1]
        print(x)
        level = int(x.split('**')[0])
        levellist = [0,4,7,10,13,16]
        print(level)
        if level >= 16 :
            if level %2 == 1 :
                if historic :
                    level-=1
                else :
                    return
        else :
            if level not in levellist :
                if historic :
                    for i in range(len(levellist)) :
                        if levellist[i] < level :
                            level = levellist[i]
                else :
                    return
        role_name = f'레벨 {level}'
        for i in message.guild.roles :
            if '레벨' in str(i.name) and i in member.roles:
                print('기존 레벨 삭제',member.nick,i.name)
                await member.remove_roles(i)
                print('삭제 완료')
            if role_name in str(i.name) :
                print('새 레벨 추가',member.nick,i.name)
                await member.add_roles(i)
                print('추가 완료')
                break

@bot.command()
async def test(ctx, left : int, right : int):
    await ctx.send(left+right)

@bot.command(aliases =  ['역할제공' ,'역할부여','giverole'])
async def role_give(ctx, nickname : discord.Member, *args) :
    print('---role_give_start---')
    role_name = ' '.join(args)
    is_not_done = True
    for i in ctx.guild.roles :
        if str(i.name) == str(role_name) :
            print('일치하는 역할 찾음')
            # print(i)
            print('역할 이름 :',i.name)
            reason = f'requested by {ctx.author.nick} | BOT controller)'
            await nickname.add_roles(i,reason=reason)
            await ctx.channel.send(f'{i.name} 역할 부여 완료')
            is_not_done = False
    if is_not_done :
        await ctx.channel.send('오류발생 : 멘션이 제대로 되었는지, 역할이 생성 되어있는지 확인 후 관리자에게 문의하세요')
    print('---role_give_end---')

@bot.command(aliases =  ['역할제거','역할뺏기','removerole'] )
async def user_remove_role(ctx, nickname : discord.Member, *args) :
    print('---role_remove_start---')
    role_name = ' '.join(args)
    is_not_done = True
    for i in ctx.guild.roles :
        if str(i.name) == str(role_name) :
            print('일치하는 역할 찾음')
            # print(i)
            print('역할 이름 :',i.name)
            reason = f'requested by {ctx.author.nick} | BOT controller)'
            await nickname.remove_roles(i,reason=reason)
            await ctx.channel.send(f'{i.name} 역할 제거 완료')
            is_not_done = False
    if is_not_done :
        await ctx.channel.send('오류발생 : 멘션이 제대로 되었는지, 역할이 생성 되어있는지 확인 후 관리자에게 문의하세요')
    print('---role_remove_end---')

@bot.command(aliases = ['역할생성','역할추가'])
async def role_create(ctx, *args) :
    print('---role_create_start---')
    role_name = ' '.join(args)
    reason = f'requested by {ctx.author.nick} | BOT controller)'
    x = await ctx.guild.create_role(name=str(role_name),reason = reason)
    await ctx.channel.send(f'{x.name} 역할 생성 완료')
    
    print('created_role : ', x.name)
    print('---role_create_end---')

@bot.command(aliases =  '역할삭제' )
async def server_delete_role(ctx, *args) :
    print('---role_delete_start---')
    role_name = ' '.join(args)
    reason = f'requested by {ctx.author.nick} | BOT controller)'
    for i in ctx.guild.roles :
        if str(i.name) == str(role_name) :
            print('일치하는 역할 찾음')
            print('delete_role : ', i.name)
            i.delete(reason=reason)
            await ctx.channel.send(f'{i.name} 역할 삭제 완료')
    print('---role_delete_end---')

@bot.command(aliases = ['레벨역할기록읽기','readlevelhistory'])
async def load_history(ctx,count:int) :
    print('---load_history_start---')
    contexts = await bot.get_context(ctx.message)
    print(contexts.channel.name)
    historys = contexts.history(limit = count)
    history_list = []
    async for i in historys :
        history_list.append(i)
    history_list.reverse()
    for i in history_list :
        await level_setter(i,historic=True)
    print('---load_history_end---')
    

# @bot.command(name = '역할편집' )
# async def role_edit(ctx, role_name, what, )


status = cycle(['controller','/도움 안 먹혀 걱정마'])
@tasks.loop(seconds=4)
async def change_status():
    await bot.change_presence(activity = discord.Game(next(status)))


@bot.event
async def on_ready():
    print('로그인중입니다. ')
    print(f"봇={bot.user.name}로 연결중")
    print('연결이 완료되었습니다.')
    change_status.start()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!예측 으로 내일 확진자수 예측"))


    

@bot.listen('on_message')
async def on_message2(message):
    print('---on_message_start---')
    await level_setter(message)
    
    print('---on_message_end---')
    return 0

bot.run(Token)#보안을위해 다른 코드(to.py)에서 토큰값을 가져옴.