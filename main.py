import discord
from discord import app_commands
from collections import defaultdict
import asyncio
from typing import Any, Literal
from bbyong_event import 채팅_매크로, 이미지_매크로, 선택지_매크로
from bbyong_commands import 멤버_등록, 멤버_삭제, 내전_모집, 내전_참여, 내전_참여취소, 내전_시작, 경매계산기, 닉네임등록, 친구추가, 돌깍기게임
from bbyong_embed import 멤버_정보, 내_정보, 도움말


f = open('token.txt', 'r')
token = f.readline().strip()

registered_members = {}
member_info = {}

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False  # 여기에 synced 초기화 추가
        self.user_pattern_counts = defaultdict(int)

    async def on_ready(self):
        await super().wait_until_ready()
        if not self.synced: 
            await tree.sync() 
            self.synced = True
        print(f'{self.user}이 시작되었습니다')  # 봇이 시작하였을 때 터미널에 뜨는 말
        game = discord.Game('산책 갈 준비')  # ~~ 하는 중
        await client.change_presence(status=discord.Status.online, activity=game)
        self.loop.create_task(self.reset_user_counts())  # loop 속성 사용

    async def reset_user_counts(self):  # 클래스 메소드로 변경
        while True:
            await asyncio.sleep(1800)  # 30분(1800초)마다 초기화
            self.user_pattern_counts.clear()

    
client = aclient()
client.intents.messages = True
client.intents.message_content = True
client.intents.members = True
tree = app_commands.CommandTree(client)

#이벤트 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@client.event
async def on_message(message):
    await 선택지_매크로(client, message)
    await 이미지_매크로(client, message)
    await 채팅_매크로(client, message)

    #await 단어_매크로(client, message)



#커맨드 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ



#정보 커맨드
@tree.command(name='멤버등록', description='신규 멤버를 등록합니다.')
async def register_member(interaction: discord.Interaction, 유저: discord.Member, 이름: str):
    await 멤버_등록(interaction, 유저, 이름)

@tree.command(name='멤버삭제', description='등록된 멤버의 정보를 삭제합니다.')
async def delete_member(interaction: discord.Interaction, 유저: discord.Member):
    await 멤버_삭제(interaction, 유저)

@tree.command(name='멤버정보', description='멤버의 정보를 확인합니다.') 
async def get_member_info(interaction: discord.Interaction, 유저: discord.Member):
    await 멤버_정보(interaction, 유저)

@tree.command(name='닉네임등록', description='라이엇 게임의 닉네임과 태그를 추가합니다. ')
async def nickname(interaction:discord.Interaction, 유저:discord.Member, 닉네임:str, 태그:str):
    await 닉네임등록(interaction, 유저, 닉네임, 태그)
    
@tree.command(name='친추', description='유저의 라이엇 게임 닉네임과 태그를 복사합니다.')
async def add_friend(interaction:discord.Interaction, 유저:discord.Member):
    await 친구추가(interaction, 유저)

@tree.command(name='내정보', description='내 정보를 확인합니다.')
async def my_info(interaction: discord.Integration):
    await 내_정보(interaction)

@tree.command(name='도움말', description='뿅뿅봇의 명령어 모음')
async def help(interaction: discord.Interaction):
    await 도움말(interaction)



#내전 커맨드
@tree.command(name='내전모집', description='내전에 참여할 멤버를 모집합니다.')
async def recruitment_member(interaction: discord.Interaction,게임: Literal["League of Legends","Valorant"], 제목: str, 시간: str, 내전코드:str):
    await 내전_모집(interaction, 게임, 제목, 시간, 내전코드)

@tree.command(name='내전참여', description='내전 참여 확인')
async def recruitment_add(interaction: discord.Interaction, 유저: discord.Member, 내전코드:str):
    await 내전_참여(interaction, 유저, 내전코드)

@tree.command(name='참여취소', description='내전 참여 취소')
async def recruitment_cancel(interaction: discord.Interaction, 유저: discord.Member, 내전코드:str):
    await 내전_참여취소(interaction, 유저, 내전코드)

@tree.command(name='내전시작', description='내전 시작')
async def recruitment_start(interaction: discord.Interaction,내전코드:str):
    await 내전_시작(interaction, 내전코드)



#로아 커맨드
@tree.command(name='경매', description='경매에 올라온 아이템의 입찰 적정가를 계산합니다.')
async def calculate(interaction: discord.Interaction, 아이템가격: int, 인원 : Literal["4","8","16"]):
    await 경매계산기(interaction, 아이템가격, 인원)

@tree.command(name='돌깎기게임', description='돌깎기 시뮬레이션 게임을 진행합니다.')
async def stone_game(interaction: discord.Interaction, 증가능력: str, 감소능력: Literal["공격력 감소","공격속도 감소","방어력 감소", "이동속도 감소"]):
    await 돌깍기게임(interaction, 증가능력, 감소능력)



client.run(token)