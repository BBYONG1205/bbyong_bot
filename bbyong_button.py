import discord
from bbyong_firebase import delete_member_info, save_member_info, get_member_info,save_recruitment_info, get_recruitment_info, update_match_status
from bbyong_select import RegisterView_lol, RegisterView_valorant
import asyncio
import random, pyperclip


#멤버삭제버튼 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

class deletememberButton(discord.ui.View):
    def __init__(self, 유저: discord.Member):
        super().__init__()
        self.유저 = 유저

    @discord.ui.button(label='확인', style=discord.ButtonStyle.green, custom_id='confirm')
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[1].disabled = True 
        await interaction.response.edit_message(view=self)

        delete_member_info(self.유저.id)
        await interaction.channel.send(f"{self.유저.mention}의 정보가 삭제되었다 뿅!")

    @discord.ui.button(label='취소', style=discord.ButtonStyle.red, custom_id='cancel')
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[0].disabled = True 
        await interaction.response.edit_message(view=self)

        # 여기에서 self.target_user를 활용하여 유저 정보에 대한 작업을 수행
        await interaction.channel.send("멤버 삭제를 취소하겠다 뿅!")


#정보등록버튼 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        
class registermember(discord.ui.View):
    def __init__(self, 유저: discord.Member):
        super().__init__()
        self.유저 = 유저

    @discord.ui.button(label='League of Legend', style=discord.ButtonStyle.primary, custom_id='League of Legend')
    async def LOL(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        tier_values = {"언랭": 20, "아이언": 0, "브론즈": 10, "실버": 20, "골드": 30, "플래티넘": 40, "에메랄드": 50, "다이아몬드": 60, "마스터": 70, "그랜드마스터": 80, "챌린저": 90}
        division_values = {"Ⅰ": 9, "Ⅱ": 6, "Ⅲ": 3, "Ⅳ": 0, "-" : 5}

        try:
            existing_data = get_member_info(self.유저.id)  # Initialize existing_data here
            view = RegisterView_lol()
            await interaction.user.send(content=f"{self.유저.display_name}의 롤 티어와 선호 라인을 선택해라 뿅!" ,view=view)

            await view.wait()
            tier_result = tier_values[view.answer1[0]]
            division_result = division_values[view.answer2[0]]

            sum_result = tier_result + division_result
            combined_result = f"{view.answer1[0]} {view.answer2[0]}"
            if len(view.answer3) == 2:
                lane_result = f"{view.answer3[0]}, {view.answer3[1]}"
                existing_data["선호 라인1"] = view.answer3[0]
                existing_data["선호 라인2"] = view.answer3[1]
            elif len(view.answer3) == 1:
                lane_result = f"{view.answer3[0]}"
                existing_data["선호 라인1"] = view.answer3[0]

            # Update existing_data with selected values
            existing_data["롤 티어"] = combined_result
            existing_data["LOL_value"] = sum_result
            save_member_info(self.유저.id, existing_data)

            # Get updated member info
            member_info = get_member_info(self.유저.id)
            이름 = member_info.get("이름")

            # Send confirmation message
            await interaction.user.send(content=f"{self.유저.display_name}의 정보가 다음과 같이 저장되었다 뿅!\r\n > {이름} \r\n > **League of Legend**  \r\n > {combined_result} {lane_result} ")

        except asyncio.TimeoutError:
            await interaction.user.send(content="시간이 초과되었다 뿅! 다시 시도해라 뿅!", ephemeral=True)

    @discord.ui.button(label='Valorant', style=discord.ButtonStyle.primary, custom_id='Valorant')
    async def VAL(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        val_tier_values = {"언랭": 20, "아이언": 0, "브론즈": 10, "실버": 20, "골드": 30, "플래티넘": 40, "다이아몬드": 50, "초월자": 60, "불멸": 70, "레디언트": 80}
        val_division_values = {"Ⅰ": 3, "Ⅱ": 6, "Ⅲ": 9, "-" : 5}

        try:
            view = RegisterView_valorant()
            await interaction.user.send(content=f"{self.유저.display_name}의 발로란트 티어와 주 포지션을 선택해라 뿅!", view=view)

            await view.wait()
            val_tier_result = val_tier_values[view.answer1[0]]
            val_division_result = val_division_values[view.answer2[0]]
            val_sum_result = val_tier_result + val_division_result    
            val_combined_result = f"{view.answer1[0]} {view.answer2[0]}"
            
            # Initialize existing_data
            existing_data = get_member_info(self.유저.id)
            
            if len(view.answer3) == 2:
                val_roles_result = f"{view.answer3[0]}, {view.answer3[1]}"
                existing_data["선호 포지션1"] = view.answer3[0]
                existing_data["선호 포지션2"] = view.answer3[1]
            elif len(view.answer3) == 1:
                val_roles_result = f"{view.answer3[0]}"
                existing_data["선호 포지션1"] = view.answer3[0]

            # Update existing_data with selected values
            existing_data["발로란트 티어"] = val_combined_result
            existing_data["VAL_value"] = val_sum_result
            save_member_info(self.유저.id, existing_data)

            # Get updated member info
            member_info = get_member_info(self.유저.id)
            이름 = member_info.get("이름")
            
            # Send confirmation message
            await interaction.user.send(content=f"{self.유저.display_name}의 정보가 다음과 같이 저장되었다 뿅!\r\n > {이름} \r\n > **Valorant** \r\n > {val_combined_result} {val_roles_result}")

        except asyncio.TimeoutError:
            await interaction.user.send(content="시간이 초과되었다 뿅! 다시 시도해라 뿅!", ephemeral=True)


    @discord.ui.button(label='종료', style=discord.ButtonStyle.red, custom_id='종료')
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[0].disabled = True
        self.children[1].disabled = True 
        await interaction.response.edit_message(view=self)


        await interaction.user.send("멤버 등록을 종료하겠다 뿅!")


class only_lol_in_member(discord.ui.View):
    def __init__(self, 유저: discord.Member):
        super().__init__()
        self.유저 = 유저
    
    @discord.ui.button(label='Valorant', style=discord.ButtonStyle.primary, custom_id='Valorant')
    async def VAL(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        val_tier_values = {"언랭": 20, "아이언": 0, "브론즈": 10, "실버": 20, "골드": 30, "플래티넘": 40, "다이아몬드": 50, "초월자": 60, "불멸": 70, "레디언트": 80}
        val_division_values = {"Ⅰ": 3, "Ⅱ": 6, "Ⅲ": 9, "-" : 5}

        try:
            view = RegisterView_valorant()
            await interaction.user.send(content=f"{self.유저.display_name}의 발로란트 티어와 주 포지션을 선택해라 뿅!", view=view)

            await view.wait()
            val_tier_result = val_tier_values[view.answer1[0]]
            val_division_result = val_division_values[view.answer2[0]]
            val_sum_result = val_tier_result + val_division_result    
            val_combined_result = f"{view.answer1[0]} {view.answer2[0]}"
            
            # Initialize existing_data
            existing_data = get_member_info(self.유저.id)
            
            if len(view.answer3) == 2:
                val_roles_result = f"{view.answer3[0]}, {view.answer3[1]}"
                existing_data["선호 포지션1"] = view.answer3[0]
                existing_data["선호 포지션2"] = view.answer3[1]
            elif len(view.answer3) == 1:
                val_roles_result = f"{view.answer3[0]}"
                existing_data["선호 포지션1"] = view.answer3[0]

            # Update existing_data with selected values
            existing_data["발로란트 티어"] = val_combined_result
            existing_data["VAL_value"] = val_sum_result
            save_member_info(self.유저.id, existing_data)

            # Get updated member info
            member_info = get_member_info(self.유저.id)
            이름 = member_info.get("이름")
            
            # Send confirmation message
            await interaction.user.send(content=f"{self.유저.display_name}의 정보가 다음과 같이 저장되었다 뿅!\r\n > {이름} \r\n > **Valorant** \r\n > {val_combined_result} {val_roles_result}")

        except asyncio.TimeoutError:
            await interaction.user.send(content="시간이 초과되었다 뿅! 다시 시도해라 뿅!", ephemeral=True)

    @discord.ui.button(label='종료', style=discord.ButtonStyle.red, custom_id='종료')
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[0].disabled = True
        await interaction.response.edit_message(view=self)


        await interaction.user.send("멤버 등록을 종료하겠다 뿅!")


class only_val_in_member(discord.ui.View):
    def __init__(self, 유저: discord.Member):
        super().__init__()
        self.유저 = 유저

    @discord.ui.button(label='League of Legend', style=discord.ButtonStyle.primary, custom_id='League of Legend')
    async def LOL(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.edit_message(view=self)

        tier_values = {"언랭": 20, "아이언": 0, "브론즈": 10, "실버": 20, "골드": 30, "플래티넘": 40, "에메랄드": 50, "다이아몬드": 60, "마스터": 70, "그랜드마스터": 80, "챌린저": 90}
        division_values = {"Ⅰ": 9, "Ⅱ": 6, "Ⅲ": 3, "Ⅳ": 0, "-" : 5}

        try:
            existing_data = get_member_info(self.유저.id)  # Initialize existing_data here
            view = RegisterView_lol()
            await interaction.user.send(content=f"{self.유저.display_name}의 롤 티어와 선호 라인을 선택해라 뿅!" ,view=view)

            await view.wait()
            tier_result = tier_values[view.answer1[0]]
            division_result = division_values[view.answer2[0]]

            sum_result = tier_result + division_result
            combined_result = f"{view.answer1[0]} {view.answer2[0]}"
            if len(view.answer3) == 2:
                lane_result = f"{view.answer3[0]}, {view.answer3[1]}"
                existing_data["선호 라인1"] = view.answer3[0]
                existing_data["선호 라인2"] = view.answer3[1]
            elif len(view.answer3) == 1:
                lane_result = f"{view.answer3[0]}"
                existing_data["선호 라인1"] = view.answer3[0]

            # Update existing_data with selected values
            existing_data["롤 티어"] = combined_result
            existing_data["LOL_value"] = sum_result
            save_member_info(self.유저.id, existing_data)

            # Get updated member info
            member_info = get_member_info(self.유저.id)
            이름 = member_info.get("이름")

            # Send confirmation message
            await interaction.user.send(content=f"{self.유저.display_name}의 정보가 다음과 같이 저장되었다 뿅!\r\n > {이름} \r\n > **League of Legend**  \r\n > {combined_result} {lane_result} ")

        except asyncio.TimeoutError:
            await interaction.user.send(content="시간이 초과되었다 뿅! 다시 시도해라 뿅!", ephemeral=True)

    @discord.ui.button(label='종료', style=discord.ButtonStyle.red, custom_id='종료')
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[0].disabled = True
        await interaction.response.edit_message(view=self)


        await interaction.followup.send("멤버 등록을 종료하겠다 뿅!", ephemeral=True)


#내전 시작 버튼 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

class Reroll(discord.ui.View):
    def __init__(self, 내전코드, 팀1, 팀2, 평균차, 참여자목록):
        super().__init__()
        
        self.내전코드 = 내전코드
        self.팀1 = 팀1
        self.팀2 = 팀2
        self.평균차 = 평균차
        self.참여자목록 = 참여자목록

    @discord.ui.button(label='다시 섞기', style=discord.ButtonStyle.primary, custom_id='다시섞기')
    async def re_roll(self, interaction: discord.Interaction, button: discord.ui.Button):
        내전정보 = get_recruitment_info(self.내전코드)
        게임종류 = 내전정보.get("게임")
        참여자목록 = 내전정보.get("참여자 목록")
        팀1, 팀2, 평균차 = 생성_팀_및_평균차(참여자목록, 게임종류)
        self.팀1 = 팀1
        self.팀2 = 팀2
        self.평균차 = 평균차

        embed = discord.Embed(title="**팀 결과**", color=discord.Color.blue())
        embed.add_field(name="게임", value=f"`{게임종류}`", inline=False)
        embed.add_field(name="추천도", value=추천도_계산(평균차), inline=False)
        embed.add_field(name="1팀", value=",  ".join([f"{참여자['이름']}" for 참여자 in 팀1]), inline=False)
        embed.add_field(name="2팀", value=",  ".join([f"{참여자['이름']}" for 참여자 in 팀2]), inline=False)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='확정', style=discord.ButtonStyle.danger, custom_id='확정')
    async def 확정(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        self.children[0].disabled = True
        await interaction.message.edit(view=self)
        내전정보 = get_recruitment_info(self.내전코드)
        if 내전정보:
            내전정보["1팀"] = self.팀1
            내전정보["2팀"] = self.팀2
            team1_names = ",  ".join([f"{participant['이름']}" for participant in self.팀1])
            team2_names = ",  ".join([f"{participant['이름']}" for participant in self.팀2])
            copy_message = f"1팀 - {team1_names} \n 2팀 - {team2_names}"
            save_recruitment_info(self.내전코드, 내전정보)
            update_match_status(self.내전코드, '게임 중')
            pyperclip.copy(copy_message)
            await interaction.channel.send(content="내전이 시작되었다 뿅!")
            await interaction.response.send_message(content="팀 결과가 복사되었다 뿅!", ephemeral=True)
        else:
            await interaction.response.send_message(content="내전 정보를 찾을 수 없다 뿅!")

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

#경매 계산기 버튼 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

class copy_button(discord.ui.View):
    def __init__(self, 입찰_적정가, 개이득):
        super().__init__()
        self.입찰_적정가 = 입찰_적정가
        self.개이득 = 개이득

    @discord.ui.button(label='입찰 적정가', style=discord.ButtonStyle.primary, custom_id='입찰 적정가')
    async def 입찰적정가(self, interaction: discord.Interaction, button: discord.ui.Button):
     pyperclip.copy(self.입찰_적정가)
     await interaction.response.send_message(content="입찰 적정가의 복사가 완료되었다 뿅!", ephemeral=True)

    @discord.ui.button(label='쌀먹용 입찰가', style=discord.ButtonStyle.primary, custom_id='쌀먹용 입찰가')
    async def 쌀먹(self, interaction: discord.Interaction, button: discord.ui.Button):
     pyperclip.copy(self.개이득)
     await interaction.response.send_message(content="쌀먹용 입찰가의 복사가 완료되었다 뿅!", ephemeral=True)