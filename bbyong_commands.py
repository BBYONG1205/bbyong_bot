import discord
import asyncio
import re
from bbyong_button import deletememberButton, registermember, only_val_in_member, only_lol_in_member, Reroll, copy_button
from bbyong_firebase import save_member_info, get_member_info, save_recruitment_info, add_participant, remove_participant, get_recruitment_info, update_match_status
from datetime import datetime
from typing import Literal
from bbyong_embed import 내전모집_임베드, 내전모집_업데이트임베드, 내전모집_참여임베드
import random, pyperclip


#멤버등록 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 멤버_등록(interaction: discord.Interaction, 유저: discord.Member, 이름: str):
    print(f"멤버 등록 시작 : {interaction.user.display_name} \n등록 요청 유저 : {유저} \n입력한 이름 : {이름}")
    existing_member = get_member_info(유저.id)

    if existing_member is not None and ("롤 티어" in existing_member or "발로란트 티어" in existing_member):

        if "롤 티어" in existing_member and "발로란트 티어" in existing_member:
            await interaction.response.send_message(content = "이미 등록되어 있는 멤버다 뿅!", ephemeral=True)

        elif "롤 티어" in existing_member:
            view = only_lol_in_member(유저)
            await interaction.response.send_message(content = f"{유저.display_name}의 정보는 롤 정보만 등록되어 있다 뿅! \n 다른 게임 정보를 추가로 등록할거냐 뿅? \n (게임 정보 등록은 DM으로 진행됩니다.)", view=view)

        elif "발로란트 티어" in existing_member:
            view = only_val_in_member(유저)
            await interaction.response.send_message(content = f"{유저.display_name}의 정보는 발로란트 정보만 등록되어 있다 뿅! \n 다른 게임 정보를 추가로 등록할거냐 뿅? \n (게임 정보 등록은 DM으로 진행됩니다.)", view=view)
    else:
        # 이름 한글만 입력 가능
        if not re.match("^[가-힣]+$", 이름):
            await interaction.response.send_message(content = "이름은 한글로만 입력이 가능하다 뿅!", ephemeral=True)
            return

        if len(이름) > 5:
            await interaction.response.send_message(content="이름은 5글자 이하로 입력 가능하다 뿅!", ephemeral=True)
            return

        member_info = {"이름": 이름, "디스코드 아이디": 유저.id}
        save_member_info(유저.id, member_info)

        # Initial success message
        await interaction.response.send_message(f"{유저.mention}의 정보가 성공적으로 등록되었다 뿅!", ephemeral=True)

        await asyncio.sleep(1)
       
        view = registermember(유저)
        await interaction.followup.send(content="추가로 게임 정보를 등록할 것이냐 뿅? \n (게임 정보 등록은 DM으로 진행됩니다.)", view=view, ephemeral=True)
        

   

#멤버삭제 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 멤버_삭제(interaction: discord.Interaction, 유저: discord.Member):
    print(f"멤버 삭제 요청자 : {interaction.user.display_name} \n삭제 요청 멤버 : {유저}")
    existing_member = get_member_info(유저.id)
    if existing_member is None:
        await interaction.response.send_message(content=f"등록되지 않은 멤버다 뿅!", ephemeral=True)
        return
    view = deletememberButton(유저)
    await interaction.response.send_message(content=f"정말로 {유저.display_name}의 정보를 삭제할 거냐 뿅?", view=view)


#내전모집 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 내전_모집(interaction: discord.Interaction, 게임: Literal["League of Legends", "Valorant"], 제목: str, 시간: str, 내전코드: str):
   
    if '오전' in 시간:
        시간 = 시간.replace("오전", "am")

    elif '오후' in 시간:
        시간 = 시간.replace("오후", "pm")

    try:
        현재_시간 = datetime.now()
        if '분' not in 시간:
            시간 += ' 00분'
        시작_시간 = datetime.strptime(시간, "%p %I시 %M분").replace(year=현재_시간.year, month=현재_시간.month, day=현재_시간.day)
        
    except ValueError as e:
        print("오류 발생: ", e)
        await interaction.response.send_message("시간 입력 형식이 잘못되었다 뿅! \r\n > ex) 오전 12시, 오후 12시 10분", ephemeral=True)
        return
    
    if 시작_시간 < 현재_시간:
        await interaction.response.send_message("과거의 시간으로는 인원을 모집할 수 없다 뿅!", ephemeral=True)
        return
    
 

    진행상태 = "모집 중"
    주최자 = interaction.user.id
    주최자_정보 = get_member_info(주최자)
    주최자_이름 = 주최자_정보.get("이름")
    recruitment_info = {"제목":제목, "게임": 게임, "시작시간": 시작_시간.strftime('%Y년 %m월 %d일 %p %I시 %M분'),"진행상태": 진행상태, "주최자": 주최자_이름, "참여자 목록":[]}
    save_recruitment_info(내전코드, recruitment_info)




    embed = 내전모집_임베드(제목, 게임, 시작_시간, 주최자_이름, 내전코드)

    
    button1 = discord.ui.Button(style=discord.ButtonStyle.primary, label="참여")
    button2 = discord.ui.Button(style=discord.ButtonStyle.danger, label="취소")

    view = discord.ui.View()
    view.add_item(button1)
    view.add_item(button2)

    await interaction.response.send_message(embed=embed,view=view) 

    async def 참여콜백(interaction: discord.Interaction):
        recruitment_id = 내전코드
        member_info = get_member_info(interaction.user.id)
        recruitment_info = get_recruitment_info(recruitment_id)
        게임종류 = recruitment_info.get('게임')
        이름 = member_info.get("이름")
        if 게임종류 == "League of Legends":
            롤_가치 = member_info.get("LOL_value", 0)
            new_participant = {"이름": 이름, "LOL_value": 롤_가치}

        elif 게임종류 == "Valorant":
            발로란트_가치 = member_info.get("VAL_value", 0)
            new_participant = {"이름": 이름, "VAL_value": 발로란트_가치}

        if member_info is None:
            await interaction.response.send_message(content="멤버 등록을 마친 뒤 다시 시도해라 뿅!", ephemeral=True)
            return
        
        recruitment_info = get_recruitment_info(recruitment_id)
        participant_list = recruitment_info.get('참여자 목록', [])
        # 등록된 멤버 수가 제한을 초과하는지 확인
        max_participants = 10  # 원하는 최대 참여자 수로 변경
        if len(participant_list) >= max_participants:
            await interaction.response.send_message(content=f"참여자가 이미 {max_participants}명을 초과하여 더 이상 참여할 수 없다 뿅!", ephemeral=True)
            return
        add_participant(recruitment_id, new_participant)

        await interaction.response.send_message(content="참가 요청이 완료되었다 뿅!", ephemeral=True)

        new_embed = 내전모집_업데이트임베드(제목, 게임, 시작_시간, 주최자_이름, 내전코드)
        
        await interaction.message.edit(embed=new_embed, view=view)
        
    async def 참여취소콜백(interaction: discord.Interaction):
        recruitment_id = 내전코드
        member_info = get_member_info(interaction.user.id)
        이름 = member_info.get("이름")
        recruitment_info = get_recruitment_info(recruitment_id)
        게임종류 = recruitment_info.get('게임')

        if 게임종류 == "League of Legends":
            롤_가치 = member_info.get("LOL_value", 0)
            participant_to_remove = {"이름": 이름, "LOL_value": 롤_가치}

        elif 게임종류 == "Valorant":
            발로란트_가치 = member_info.get("VAL_value", 0)
            participant_to_remove = {"이름": 이름, "VAL_value": 발로란트_가치}

        
        if member_info is None:
            await interaction.response.send_message(content=f"등록되지 않은 멤버다 뿅!", ephemeral=True)
            return
        
        remove_participant(recruitment_id, participant_to_remove)

        await interaction.response.send_message(content="참가 요청이 취소되었다 뿅!", ephemeral=True)

        new_embed = 내전모집_업데이트임베드(제목, 게임, 시작_시간, 주최자_이름, 내전코드)
       
        await interaction.message.edit(embed=new_embed, view=view)
        

    button1.callback = 참여콜백
    button2.callback = 참여취소콜백

    
#내전참여(임시)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    
async def 내전_참여(interaction: discord.Interaction, 유저: discord.Member, 내전코드: str):
    print(f"내전 참여 요청자 : {interaction.user.display_name} \n요청 멤버 : {유저}")
    recruitment_id = 내전코드
    member_info = get_member_info(유저.id)
    recruitment_info = get_recruitment_info(recruitment_id)

    이름 = member_info.get("이름")
    게임종류 = recruitment_info.get('게임')

    if 게임종류 == "League of Legends":
        롤_가치 = member_info.get("LOL_value", 0)
        new_participant = {"이름": 이름, "LOL_value": 롤_가치}

    elif 게임종류 == "Valorant":
        발로란트_가치 = member_info.get("VAL_value", 0)
        new_participant = {"이름": 이름, "VAL_value": 발로란트_가치}
    
    if member_info is None:
        await interaction.response.send_message(content="멤버 등록을 마친 뒤 다시 시도해라 뿅!", ephemeral=True)
        return
        
    recruitment_info = get_recruitment_info(recruitment_id)
    participant_list = recruitment_info.get('참여자 목록', [])
     
    max_participants = 10  #최대 참여자 수 확인 코드

    if len(participant_list) >= max_participants:
            await interaction.response.send_message(content=f"참여자가 이미 {max_participants}명을 초과하여 더 이상 참여할 수 없다 뿅!", ephemeral=True)
            return
    
    add_participant(recruitment_id, new_participant)

    participation_embed = 내전모집_참여임베드(내전코드)

    await interaction.response.send_message(content="참가 요청이 완료되었다 뿅!", embed=participation_embed, ephemeral=True)

 #내전참여취소(임시)ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    
async def 내전_참여취소(interaction: discord.Interaction, 유저: discord.Member, 내전코드: str):

    print(f"내전 참여 취소 요청자 : {interaction.user.display_name} \n요청 멤버 : {유저}")
    recruitment_id = 내전코드
    member_info = get_member_info(유저.id)
    recruitment_info = get_recruitment_info(recruitment_id)

    이름 = member_info.get("이름")
    게임종류 = recruitment_info.get('게임')

    if 게임종류 == "League of Legends":
        롤_가치 = member_info.get("LOL_value", 0)
        participant_to_remove = {"이름": 이름, "LOL_value": 롤_가치}

    elif 게임종류 == "Valorant":
        발로란트_가치 = member_info.get("VAL_value", 0)
        participant_to_remove = {"이름": 이름, "VAL_value": 발로란트_가치}

    if member_info is None:
        await interaction.response.send_message(content=f"등록되지 않은 멤버다 뿅!", ephemeral=True)
        return
        
    remove_participant(recruitment_id, participant_to_remove)

    participation_embed = 내전모집_참여임베드(내전코드)

    await interaction.response.send_message(content="참가 요청이 취소되었다 뿅!", embed=participation_embed, ephemeral=True)   



#내전시작ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ   

async def 내전_시작(interaction: discord.Interaction, 내전코드: str):
    print(f"내전 시작 요청자 : {interaction.user.display_name} \n시작한 내전 코드 : {내전코드}")
        
    내전정보 = get_recruitment_info(내전코드)

    if not 내전정보:
        await interaction.response.send_message(content="존재하지 않는 검색 코드다 뿅!")
        return

    게임종류 = 내전정보.get("게임")
    참여자목록 = 내전정보.get("참여자 목록")
    진행상태=내전정보.get("진행상태")       
    if len(참여자목록) < 10:
        await interaction.response.send_message(content="내전을 시작할 인원이 부족하다 뿅!")
        return
    
    if 진행상태 == '진행 중':
        await interaction.response.send_message(content='이미 진행 중인 내전이다 뿅!', ephemeral=True)
        return
    elif 진행상태== '종료':
        await interaction.response.send_message(content='이미 종료된 내전이다 뿅!')
        return
    
    update_match_status(내전코드, '진행 중')

    팀1, 팀2, 평균차 = 생성_팀_및_평균차(참여자목록, 게임종류)

    embed = discord.Embed(title="**팀 결과**", color=discord.Color.blue())
    embed.add_field(name="게임", value=f"`{게임종류}`", inline=False)
    embed.add_field(name="추천도", value=추천도_계산(평균차), inline=False)
    embed.add_field(name="1팀", value=",  ".join([f"{참여자['이름']}" for 참여자 in 팀1]), inline=False)
    embed.add_field(name="2팀", value=",  ".join([f"{참여자['이름']}" for 참여자 in 팀2]), inline=False)

    try:
        view = Reroll(내전코드, 팀1, 팀2, 평균차, 참여자목록)
        await interaction.response.send_message(embed=embed, view=view)
    except discord.Forbidden:
        await interaction.response.send_message(content="메시지를 보낼 권한이 없다 뿅!")

def 생성_팀_및_평균차(참여자목록, 게임종류):
    while True:
        팀1 = random.sample(참여자목록, k=5)
        팀2 = [참여자 for 참여자 in 참여자목록 if 참여자 not in 팀1]

        # 각 팀의 롤 가치 평균 계산
        롤_가치_필드 = 'LOL_value' if 게임종류 == 'League of Legends' else 'VAL_value'
        팀1평균 = sum(참여자.get(롤_가치_필드, 25) for 참여자 in 팀1) / len(팀1)
        팀2평균 = sum(참여자.get(롤_가치_필드, 25) for 참여자 in 팀2) / len(팀2)

        # 팀 간 롤 가치 평균 차이가 10 미만인 경우 반복 종료
        평균차 = round(abs(팀2평균 - 팀1평균), 2)
        if 평균차 < 10:
            break

    print(평균차)
    return 팀1, 팀2, 평균차

def 추천도_계산(평균차):
    if 5 < 평균차 < 10:
        return "`보통`"
    elif 2 < 평균차 <= 5:
        return "`추천`"
    elif 0 < 평균차 <= 2:
        return "`강추`"
    elif 평균차 == 0:
        return "`★황금밸런스★`"


#경매계산기 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
async def 경매계산기(interaction: discord.Interaction, 아이템가격: int, 인원 : Literal["4","8","16"]):
    숫자열_인원=int(인원)
    수수료 = int(round(아이템가격 * 0.05, 1))
    분배금 = int(round(아이템가격 / (숫자열_인원 - 1), 1))
    손익분기점_인원 = (숫자열_인원 - 1) / 숫자열_인원
    수수료_제외 = 아이템가격 - 수수료
    손익분기점 = int(수수료_제외 * 손익분기점_인원)
    입찰_적정가 = int(round(손익분기점 / 1.1, 1))
    개이득 = int(round(입찰_적정가 / 1.1, 1))


    embed = discord.Embed(title="**경매 계산기**", color=0xffffff)
    embed.add_field(name="수수료", value=f"`-{수수료}`<:Gold:1204324099908702228>", inline=False)
    embed.add_field(name="분배금", value=f"`-{분배금}`<:Gold:1204324099908702228>", inline=False)
    embed.add_field(name="손익분기점", value=f"`{손익분기점}`<:Gold:1204324099908702228>", inline=False)
    embed.add_field(name="입찰 적정가", value=f"`{입찰_적정가}`<:Gold:1204324099908702228>", inline=False)
    embed.add_field(name="쌀먹용 입찰가", value=f"`{개이득}`<:Gold:1204324099908702228>", inline=False)
    embed.set_footer(text="아래의 버튼 클릭 시 각 입찰 금액이 복사됩니다.")

    view = copy_button(입찰_적정가, 개이득)
    await interaction.response.send_message(embed=embed, view=view)



async def 닉네임등록(interaction:discord.Interaction, 유저:discord.Member, 닉네임:str, 태그:str):
    print(f"닉네임 등록 요청자 : {interaction.user.display_name} \n등록 요청 유저 : {유저}")
    existing_data = get_member_info(유저.id)
    라이엇_태그 = f"{닉네임}#{태그}"

    existing_data['라이엇 태그'] = 라이엇_태그

    save_member_info(유저.id, existing_data)
    await interaction.response.send_message(f"라이엇 태그가 정상적으로 등록되었다 뿅! \n >  {라이엇_태그}")

async def 친구추가(interaction:discord.Interaction, 유저:discord.Member):
    member_info=get_member_info(유저.id)
    라이엇태그 = member_info.get('라이엇 태그')
    pyperclip.copy(라이엇태그)

    await interaction.response.send_message(f"{유저.display_name}의 태그가 복사되었다 뿅! \n >  {라이엇태그}", ephemeral=True)




async def 돌깎기게임(interaction: discord.Interaction, 증가능력: str, 감소능력: Literal["공격력 감소", "공격속도 감소", "방어력 감소", "이동속도 감소"]):
    명령어사용자=interaction.user.id

    증가능력_입력값 = 증가능력.split(maxsplit=1)

    축약어_모음 = {
        '결대': '결투의 대가', '구동': '구슬동자',
        '급타': '급소 타격', '기습': '기습의 대가',
        '달저': '달인의 저력', '돌대': '돌격대장',
        '마효증': '마나 효율 증가', '바리': '바리케이드',
        '번분': '번개의 분노', '부뼈': '부러진 뼈',
        '선필': '선수필승', '속속': '속전속결', 
        '슈차': '슈퍼 차지', '실관': '실드 관통',
        '안상': '안정된 상태', '약무': '약자 무시',
        '에포': '에테르 포식자', '예둔': '예리한 둔기',
        '위모': '위기 모면', '정흡': '정기 흡수',
        '정단': '정밀 단도','중착': '중갑 착용', '중갑': '중갑 착용',
        '질증': '질량 증가', '최마증': '최대 마나 증가',
        '타대': '타격의 대가', '아드': '아드레날린',
        '저받': '저주받은 인형'
    }

    증가능력_목록 = [
        "각성", "강령술", "강화 방패", "결투의 대가", "구슬동자", "굳은 의지", "급소 타격", "기습의 대가",
        "긴급 구조", "달인의 저력", "돌격대장", "마나 효율 증가", "마나의 흐름", "바리케이드", "번개의 분노", "부러진 뼈",
        "분쇄의 주먹", "불굴", "선수필승", "속전속결", "슈퍼 차지", "승부사", "시선 집중", "실드 관통", "아드레날린",
        "안정된 상태", "약자 무시", "에테르 포식자", "여신의 가호", "예리한 둔기", "원한", "위기 모면", "저주받은 인형",
        "전문의", "정기 흡수", "정밀 단도", "중갑 착용", "질량 증가", "최대 마나 증가", "추진력", "타격의 대가",
        "탈출의 명수", "폭발물 전문가"
    ]

    if len(증가능력_입력값) == 2:
        증가능력1, 증가능력2 = 증가능력_입력값
        
        # 각각의 증가능력 값에 대해 축약어 여부 확인
        for 축약어, 전체단어 in 축약어_모음.items():
            if 축약어 in 증가능력1:
                증가능력1 = 전체단어
                break
        else:
            증가능력1 = 증가능력1

        for 축약어, 전체단어 in 축약어_모음.items():
            if 축약어 in 증가능력2:
                증가능력2 = 전체단어
                break
        else:
            증가능력2 = 증가능력2
            
        # 각 증가능력이 목록에 없으면 메시지 출력 후 종료
        if 증가능력1 not in 증가능력_목록 or 증가능력2 not in 증가능력_목록:
            await interaction.response.send_message("올바르지 않은 각인 명이다 뿅!",ephemeral=True)
            return
        

        증가능력_남은기회="[1;34m◇ [0m"
        감소능력_남은기회="[1;31m◇ [0m"
        #증가능력_성공="[1;34m◆ [0m"
        #증가능력_실패="[1;30m◆ [0m"


        증가능력1_출력값 = 증가능력_남은기회 * 10
        증가능력2_출력값 = 증가능력_남은기회 * 10
        감소능력_출력값 = 감소능력_남은기회 * 10

        embed = discord.Embed(title="**돌깎기 게임**", color=0xffffff)
        embed.add_field(name="**성공확률** ```75%```", value="", inline=False)
        embed.add_field(name=증가능력1, value=f"```ansi\n{증가능력1_출력값}\n```", inline=False)
        embed.add_field(name=증가능력2, value=f"```ansi\n{증가능력2_출력값}\n```", inline=False)
        embed.add_field(name=감소능력, value=f"```ansi\n{감소능력_출력값}\n```", inline=False)

        button1 = discord.ui.Button(style=discord.ButtonStyle.primary, label=증가능력1)
        button2 = discord.ui.Button(style=discord.ButtonStyle.primary, label=증가능력2)
        button3 = discord.ui.Button(style=discord.ButtonStyle.danger, label=감소능력)

        view = discord.ui.View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
                            
        await interaction.response.send_message(embed=embed, view=view)

        success_rate = 75
        max_success_rate = 75
        min_success_rate = 25
        증가능력1_시도횟수 = 0
        증가능력2_시도횟수 = 0
        감소능력_시도횟수 = 0
    
        증가능력1_결과 = ""
        증가능력2_결과 = ""
        감소능력_결과 = ""

        async def 증가능력1_콜백(interaction: discord.Interaction):
            nonlocal success_rate, 증가능력1_시도횟수, 증가능력1_결과, 증가능력2_결과, 감소능력_결과
            버튼사용자=interaction.user.id

            if 명령어사용자 != 버튼사용자:
                await interaction.response.send_message("다른 사람이 이용 중인 게임이다 뿅!", ephemeral=True)
                return

            if 증가능력1_시도횟수 < 10:
                if random.randint(1, 100) <= success_rate:
                    증가능력1_결과 += "[1;34m◆ [0m"
                    success_rate = max(min_success_rate, success_rate - 10)
                else:
                    증가능력1_결과 += "[1;30m◆ [0m"
                    success_rate = min(max_success_rate, success_rate + 10)

                증가능력1_시도횟수 += 1
                증가능력_남은기회표시 = "[1;34m◇ [0m"
                감소능력_남은기회표시 = "[1;31m◇ [0m"
                증1_남은기회 = 10 - 증가능력1_시도횟수
                증가능력1_남은기회 = 증가능력_남은기회표시 * 증1_남은기회
                증2_남은기회 = 10 - 증가능력2_시도횟수
                증가능력2_남은기회 = 증가능력_남은기회표시 * 증2_남은기회
                감능_남은기회 = 10 - 감소능력_시도횟수
                감소능력__남은기회 = 감소능력_남은기회표시 * 감능_남은기회

                edit_embed = discord.Embed(title=f"**돌깎기 게임**", color=0xffffff)
                edit_embed.add_field(name=f"**성공확률** ```{success_rate}%```", value="", inline=False)
                edit_embed.add_field(name=증가능력1, value=f"```ansi\n{증가능력1_결과}{증가능력1_남은기회}\n```", inline=False)
                edit_embed.add_field(name=증가능력2, value=f"```ansi\n{증가능력2_결과}{증가능력2_남은기회}\n```", inline=False)
                edit_embed.add_field(name=감소능력, value=f"```ansi\n{감소능력_결과}{감소능력__남은기회}\n```", inline=False)
                
                await interaction.response.edit_message(embed=edit_embed, view=view)
            else:
                await interaction.response.send_message(f"{증가능력1}의 남은 기회가 없다 뿅!", ephemeral=True)

        async def 증가능력2_콜백(interaction: discord.Interaction):
            nonlocal success_rate, 증가능력2_시도횟수, 증가능력1_결과, 증가능력2_결과, 감소능력_결과
            버튼사용자=interaction.user.id

            if 명령어사용자 != 버튼사용자:
                await interaction.response.send_message("다른 사람이 이용 중인 게임이다 뿅!", ephemeral=True)
                return

            if 증가능력2_시도횟수 < 10:
                if random.randint(1, 100) <= success_rate:
                    증가능력2_결과 += "[1;34m◆ [0m"
                    success_rate = max(min_success_rate, success_rate - 10)
                else:
                    증가능력2_결과 += "[1;30m◆ [0m"
                    success_rate = min(max_success_rate, success_rate + 10)

                증가능력2_시도횟수 += 1
                증가능력_남은기회표시 = "[1;34m◇ [0m"
                감소능력_남은기회표시 = "[1;31m◇ [0m"
                증1_남은기회 = 10 - 증가능력1_시도횟수
                증가능력1_남은기회 = 증가능력_남은기회표시 * 증1_남은기회
                증2_남은기회 = 10 - 증가능력2_시도횟수
                증가능력2_남은기회 = 증가능력_남은기회표시 * 증2_남은기회
                감능_남은기회 = 10 - 감소능력_시도횟수
                감소능력__남은기회 = 감소능력_남은기회표시 * 감능_남은기회

                edit_embed = discord.Embed(title=f"**돌깎기 게임**", color=0xffffff)
                edit_embed.add_field(name=f"**성공확률** ```{success_rate}%```", value="", inline=False)
                edit_embed.add_field(name=증가능력1, value=f"```ansi\n{증가능력1_결과}{증가능력1_남은기회}\n```", inline=False)
                edit_embed.add_field(name=증가능력2, value=f"```ansi\n{증가능력2_결과}{증가능력2_남은기회}\n```", inline=False)
                edit_embed.add_field(name=감소능력, value=f"```ansi\n{감소능력_결과}{감소능력__남은기회}\n```", inline=False)
                
                await interaction.response.edit_message(embed=edit_embed, view=view)
            else:
                await interaction.response.send_message(f"{증가능력2}의 남은 기회가 없다 뿅!", ephemeral=True)

        async def 감소능력_콜백(interaction: discord.Interaction):
            nonlocal success_rate, 감소능력_시도횟수, 증가능력1_결과, 증가능력2_결과, 감소능력_결과
            버튼사용자=interaction.user.id

            if 명령어사용자 != 버튼사용자:
                await interaction.response.send_message("다른 사람이 이용 중인 게임이다 뿅!", ephemeral=True)
                return

            if 감소능력_시도횟수 < 10:
                if random.randint(1, 100) <= success_rate:
                    감소능력_결과 += "[1;31m◆ [0m"
                    success_rate = max(min_success_rate, success_rate - 10)
                else:
                    감소능력_결과 += "[1;30m◆ [0m"
                    success_rate = min(max_success_rate, success_rate + 10)

                감소능력_시도횟수 += 1
                증가능력_남은기회표시 = "[1;34m◇ [0m"
                감소능력_남은기회표시 = "[1;31m◇ [0m"
                증1_남은기회 = 10 - 증가능력1_시도횟수
                증가능력1_남은기회 = 증가능력_남은기회표시 * 증1_남은기회
                증2_남은기회 = 10 - 증가능력2_시도횟수
                증가능력2_남은기회 = 증가능력_남은기회표시 * 증2_남은기회
                감능_남은기회 = 10 - 감소능력_시도횟수
                감소능력__남은기회 = 감소능력_남은기회표시 * 감능_남은기회

                edit_embed = discord.Embed(title=f"**돌깎기 게임**", color=0xffffff)
                edit_embed.add_field(name=f"**성공확률** ```{success_rate}%```", value="", inline=False)
                edit_embed.add_field(name=증가능력1, value=f"```ansi\n{증가능력1_결과}{증가능력1_남은기회}\n```", inline=False)
                edit_embed.add_field(name=증가능력2, value=f"```ansi\n{증가능력2_결과}{증가능력2_남은기회}\n```", inline=False)
                edit_embed.add_field(name=감소능력, value=f"```ansi\n{감소능력_결과}{감소능력__남은기회}\n```", inline=False)
                
                await interaction.response.edit_message(embed=edit_embed, view=view)
            else:
                await interaction.response.send_message(f"{감소능력}의 남은 기회가 없다 뿅!", ephemeral=True)

        button1.callback = 증가능력1_콜백
        button2.callback = 증가능력2_콜백
        button3.callback = 감소능력_콜백
        
    else:
        await interaction.response.send_message("두개의 각인을 입력해야한다 뿅!", ephemeral=True)
        return


    

  
