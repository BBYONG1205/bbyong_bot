import discord
from bbyong_firebase import get_member_info, get_recruitment_info, get_participant_names
from datetime import datetime

#멤버정보 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 멤버_정보(interaction: discord.Interaction, 유저: discord.Member):
    member_info = get_member_info(유저.id)
    if not member_info:
        await interaction.response.send_message("해당 사용자 정보를 찾을 수 없다 뿅!", ephemeral=True)
        return
    
    
    if member_info:
        embed = discord.Embed(title=f"{유저.display_name}님의 정보", color=0xffffff)
        embed.add_field(name="이름", value=member_info.get("이름"), inline=False)
        if 유저.avatar:      
            embed.set_thumbnail(url=유저.avatar.url)
        else:  
            embed.set_thumbnail(url="https://i.ibb.co/Vm2Gx5w/image.jpg")

        # 롤 정보가 있는 경우에만 표시
        롤_티어 = member_info.get("롤 티어")
        선호라인1 = member_info.get("선호 라인1")
        선호라인2 = member_info.get("선호 라인2")
        if 롤_티어 and 선호라인1 and 선호라인2:
            embed.add_field(name="**League of Legends**", value=f"> **티어**    {롤_티어} \r\n > **선호 라인**    {선호라인1}, {선호라인2}", inline=False)
        elif 롤_티어 and 선호라인1:
            embed.add_field(name="**League of Legends**", value=f"> **티어**    {롤_티어} \r\n > **선호 라인**    {선호라인1}", inline=False)
       
        # 발로란트 정보가 있는 경우에만 표시
        발로란트_티어 = member_info.get("발로란트 티어")
        선호포지션1 = member_info.get("선호 포지션1")
        선호포지션2 = member_info.get("선호 포지션2")
        if 발로란트_티어 and 선호포지션1 and 선호포지션2:
            embed.add_field(name="**Valorant**", value=f"> **티어**    {발로란트_티어} \r\n > **선호 포지션**    {선호포지션1}, {선호포지션2}", inline=False)
        elif 발로란트_티어 and 선호포지션1:
            embed.add_field(name="**Valorant**", value=f"> **티어**    {발로란트_티어} \r\n > **선호 포지션**    {선호포지션1}", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=False)
    else:
        await interaction.response.send_message("해당 멤버의 정보를 찾을 없다 뿅!", ephemeral=True)


#내정보 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        
async def 내_정보(interaction: discord.Interaction):
    me = interaction.user
    member_info = get_member_info(me.id)
    if member_info:
        embed = discord.Embed(title="내 정보", color=0xffffff)
        embed.add_field(name="이름", value=member_info.get("이름"), inline=False)

        # 롤 정보가 있는 경우에만 표시
        롤_티어 = member_info.get("롤 티어")
        선호라인1 = member_info.get("선호 라인1")
        선호라인2 = member_info.get("선호 라인2")
        if 롤_티어 and 선호라인1 and 선호라인2:
            embed.add_field(name="**League of Legends**", value=f"> **티어**    {롤_티어} \r\n > **선호 라인**    {선호라인1}, {선호라인2}", inline=False)
        elif 롤_티어 and 선호라인1:
            embed.add_field(name="**League of Legends**", value=f"> **티어**    {롤_티어} \r\n > **선호 라인**    {선호라인1}", inline=False)

        
        # 발로란트 정보가 있는 경우에만 표시
        발로란트_티어 = member_info.get("발로란트 티어")
        선호포지션1 = member_info.get("선호 포지션1")
        선호포지션2 = member_info.get("선호 포지션2")
        if 발로란트_티어 and 선호포지션1 and 선호포지션2:
            embed.add_field(name="**Valorant**", value=f"> **티어**    {발로란트_티어} \r\n > **선호 포지션**    {선호포지션1}, {선호포지션2}", inline=False)
        elif 발로란트_티어 and 선호포지션1:
            embed.add_field(name="**Valorant**", value=f"> **티어**    {발로란트_티어} \r\n > **선호 포지션**    {선호포지션1}", inline=False)


        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message("등록된 정보가 없다 뿅!", ephemeral=True)


#도움말 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 도움말(interaction: discord.Interaction):
    embed = discord.Embed(title="**도움말**", color=0xffffff)
    embed.add_field(name="명령어 목록", value="", inline=False)
    embed.add_field(name="멤버등록", value="`신규 멤버를 등록합니다.`", inline=False)
    embed.add_field(name="멤버정보", value="`멤버의 정보를 확인합니다.`", inline=False)
    embed.add_field(name="멤버삭제", value="`등록되어있는 멤버의 정보를 삭제합니다.`", inline=False)
    embed.add_field(name="내정보", value="`나의 정보를 확인합니다.`", inline=False)
    embed.add_field(name="내전모집", value="`내전에 참여할 멤버를 모집합니다.`", inline=False)
    embed.add_field(name="내전참여", value="`내전코드를 입력하여 내전에 참여합니다.`", inline=False)
    embed.add_field(name="내전참여", value="`내전코드를 입력하여 참여를 취소합니다.`", inline=False)
    embed.add_field(name="내전시작", value="`내전코드를 입력하여 내전을 시작합니다.`", inline=False)
    embed.add_field(name="경매계산기", value="`로스트아크 경매 입찰 시 적정 가격을 계산합니다.`", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


#내전모집 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

def 내전모집_임베드(제목, 게임, 시작_시간, 주최자_이름, 내전코드):

    제목_메세지 = f":loudspeaker: {제목} "
    주최자_메세지 = f"\n{주최자_이름}님이 내전 모집을 시작하였습니다.\n내전코드 - {내전코드}"
    게임_메세지 = f"`{게임}`"
    ampm = 시작_시간.strftime("%p")
    오전오후 = "오전" if ampm == "AM" else "오후"
    시간 = 시작_시간.strftime("%I시 %M분")
    시작시간_메세지 = f"`{오전오후} {시간}`"



    embed = discord.Embed(title=제목_메세지, color=discord.Color.blue())
    embed.add_field(name=f":video_game: 게임", value=게임_메세지, inline=False)
    embed.add_field(name=":alarm_clock: 시작 시간", value=시작시간_메세지, inline=False)
    embed.add_field(name=":busts_in_silhouette: 참여자 목록 (0)", value=">>> - ", inline=False)
    embed.add_field(name="", value="", inline=False)
    embed.set_footer(text=주최자_메세지)
    return embed


def 내전모집_업데이트임베드(제목, 게임, 시작_시간, 주최자_이름,내전코드):


    제목_메세지 = f":loudspeaker: {제목} "
    주최자_메세지 = f"\n{주최자_이름}님이 내전 모집을 시작하였습니다.\n내전코드 - {내전코드}"
    게임_메세지 = f"`{게임}`"
    ampm = 시작_시간.strftime("%p")
    오전오후 = "오전" if ampm == "AM" else "오후"
    시간 = 시작_시간.strftime("%I시 %M분")
    시작시간_메세지 = f"`{오전오후} {시간}`"


    recruitment_id = 내전코드
    participant_list = get_participant_names(recruitment_id)
    참여자_수 = len(participant_list)

    new_embed = discord.Embed(title=제목_메세지, color=discord.Color.blue())
    new_embed.add_field(name=":video_game: 게임", value=게임_메세지, inline=False)
    new_embed.add_field(name=":alarm_clock: 시작 시간", value=시작시간_메세지, inline=False)
        
    if participant_list:
        participants_field = "\n".join([f"{participant}" for participant in participant_list])
        new_embed.add_field(name=f":busts_in_silhouette: 참여자 목록 ({참여자_수})", value=f">>> {participants_field}", inline=False)
        new_embed.add_field(name="", value="", inline=False)
        new_embed.set_footer(text=주최자_메세지)
    else:
        new_embed.add_field(name=":busts_in_silhouette: 참여자 목록", value=">>> - ", inline=False)
        new_embed.add_field(name="", value="", inline=False)
        new_embed.set_footer(text=주최자_메세지)

    return new_embed


#내전참여 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

def 내전모집_참여임베드(내전코드):

    recruitment_id = 내전코드
    recruitment_info = get_recruitment_info(recruitment_id)
    제목 = recruitment_info.get("제목")
    게임 = recruitment_info.get("게임")
    시작_시간 = recruitment_info.get("시작시간")
    주최자_이름 = recruitment_info.get("주최자")
    participant_list = get_participant_names(recruitment_id)

    if "AM" in 시작_시간 or "PM" in 시작_시간:
        시작시간변형 = datetime.strptime(시작_시간, "%Y년 %m월 %d일 %p %I시 %M분")
        ampm = 시작시간변형.strftime("%p")
        오전오후 = "오전" if ampm == "AM" else "오후"
        시간 = 시작시간변형.strftime("%I시 %M분")
    else:
        # AM/PM 정보가 없는 경우에는 그냥 변환
        시작시간변형 = datetime.strptime(시작_시간, "%Y년 %m월 %d일 %I시 %M분")
        오전오후 = ""  # AM/PM 정보가 없는 경우에는 빈 문자열로 설정
        시간 = 시작시간변형.strftime("%I시 %M분")

    참여자_수 = len(participant_list)
    제목_메세지 = f":loudspeaker: {제목} "
    주최자_메세지 = f"\n{주최자_이름}님이 내전 모집을 시작하였습니다.\n내전코드 - {내전코드}"
    게임_메세지 = f"`{게임}`"
    시작시간_메세지 = f"`{오전오후} {시간}`"


    participation_embed = discord.Embed(title=제목_메세지, color=discord.Color.blue())
    participation_embed.add_field(name=":video_game: 게임", value=게임_메세지, inline=False)
    participation_embed.add_field(name=":alarm_clock: 시작 시간", value=시작시간_메세지, inline=False)

    participants_field = "\n".join([f"{participant}" for participant in participant_list])
    if participants_field:
        participation_embed.add_field(name=f":busts_in_silhouette: 참여자 목록 ({참여자_수})", value=f">>> {participants_field}", inline=False)
        participation_embed.add_field(name="", value="", inline=False)
        participation_embed.set_footer(text=주최자_메세지)
   
    else:
        participation_embed.add_field(name=":busts_in_silhouette: 참여자 목록", value=">>> -", inline=False)
        participation_embed.add_field(name="", value="", inline=False)
        participation_embed.set_footer(text=주최자_메세지)
   
    return participation_embed


#돌깎기 게임 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
