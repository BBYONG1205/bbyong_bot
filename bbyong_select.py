import discord

#리그오브레전드 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

class UserTierSelect_lol(discord.ui.Select):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            discord.SelectOption(label="Ⅰ", value="Ⅰ"),
            discord.SelectOption(label="Ⅱ", value="Ⅱ"),
            discord.SelectOption(label="Ⅲ", value="Ⅲ"),
            discord.SelectOption(label="Ⅳ", value="Ⅳ"),
            discord.SelectOption(label="-", value="-"),
        ]
        super().__init__(options=options, placeholder="티어를 선택하세요")

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)

class LineSelect_lol(discord.ui.Select):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            discord.SelectOption(label="탑", emoji="<:LOL_TOP:1197071245389336628>", description="Top"),
            discord.SelectOption(label="미드", emoji="<:LOL_MID:1197071240846921809>", description="Mid"),
            discord.SelectOption(label="정글", emoji="<:LOL_JUNGLE:1197071238296784906>", description="Jungle"),
            discord.SelectOption(label="원딜", emoji="<:LOL_ADC:1197071235255898162>", description="ADC"),
            discord.SelectOption(label="서폿", emoji="<:LOL_SUPPORT:1197071243573215333>", description="Support"),
            discord.SelectOption(label="상관없음", emoji="<:LOL_FILL:1199916524018868265>", description="Fill"),
        ]
        super().__init__(options=options, placeholder="선호 라인을 선택하세요(최대 2개)", max_values=2)

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer3(interaction, self.values)

class RegisterView_lol(discord.ui.View):
    answer1 = None
    answer2 = None
    answer3 = None

    @discord.ui.select(
        placeholder="티어를 선택하세요",
        options=[
            discord.SelectOption(label="언랭", emoji="<:EMBLEM_UNRANKED:1197073800064401429>", description="Unranked"),
            discord.SelectOption(label="아이언", emoji="<:EMBLEM_IRON:1197073785497595996>", description="Iron"),
            discord.SelectOption(label="브론즈", emoji="<:EMBLEM_BRONZE:1197073767491452948>", description="Bronze"),
            discord.SelectOption(label="실버", emoji="<:EMBLEM_SILVER:1197073795580711054>", description="Silver"),
            discord.SelectOption(label="골드", emoji="<:EMBLEM_GOLD:1197073777851379733>", description="Gold"),
            discord.SelectOption(label="플래티넘", emoji="<:EMBLEM_PLATINUM:1197073790480437259>", description="Platinum"),
            discord.SelectOption(label="에메랄드", emoji="<:EMBLEM_EMERALD:1197073775863271485>", description="Emerald"),
            discord.SelectOption(label="다이아몬드", emoji="<:EMBLEM_DIAMOND:1197073772449116233>", description="Diamond"),
            discord.SelectOption(label="마스터", emoji="<:EMBLEM_MASTER:1197073788492333107>", description="Master"),
            discord.SelectOption(label="그랜드마스터", emoji="<:EMBLEM_GRANDMASTER:1197073781693358160>", description="Grandmaster"),
            discord.SelectOption(label="챌린저", emoji="<:EMBLEM_CHALLENGER:1197073769773146183>", description="Challenger"),
        ]
    )
    async def select_tier(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values
        self.children[0].disabled = True

        tier_select = UserTierSelect_lol()
        self.add_item(tier_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        self.answer2 = choices
        self.children[1].disabled = True
        line_select = LineSelect_lol()
        self.add_item(line_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer3(self, interaction: discord.Interaction, choices):
        self.answer3 = choices
        self.children[2].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        # View 종료
        self.stop()


#발로란트 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        

class UserTierSelect_valorant(discord.ui.Select):
    def __init__(self):
        super().__init__(timeout=None)
        options = [
            discord.SelectOption(label="Ⅰ", value="Ⅰ"),
            discord.SelectOption(label="Ⅱ", value="Ⅱ"),
            discord.SelectOption(label="Ⅲ", value="Ⅲ"),
            discord.SelectOption(label="-", value="-"),

        ]
        super().__init__(options=options, placeholder="티어를 선택하세요")

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)

class LineSelect_valorant(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="타격대", description="Duelists"),
            discord.SelectOption(label="척후대", description="Initiators"),
            discord.SelectOption(label="감시자", description="Sentinels"),
            discord.SelectOption(label="전략가",  description="Controllers"),
        ]
        super().__init__(options=options, placeholder="선호 포지션을 선택하세요(최대 2개)", max_values=2)

    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer3(interaction, self.values)

class RegisterView_valorant(discord.ui.View):
    answer1 = None
    answer2 = None
    answer3 = None

    @discord.ui.select(
        placeholder="티어를 선택하세요",
        options=[
            discord.SelectOption(label="언랭", emoji="<:EMBLEM_UNRANKED:1197073800064401429>", description="Unranked"),
            discord.SelectOption(label="아이언",  description="Iron"),
            discord.SelectOption(label="브론즈", description="Bronze"),
            discord.SelectOption(label="실버", description="Silver"),
            discord.SelectOption(label="골드", description="Gold"),
            discord.SelectOption(label="플래티넘",  description="Platinum"),
            discord.SelectOption(label="다이아몬드", description="Diamond"),
            discord.SelectOption(label="초월자", description="Ascendant"),
            discord.SelectOption(label="불멸", description="Immortal"),
            discord.SelectOption(label="레디언트", description="Radiant"),
        ]
    )
    async def select_tier(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values
        self.children[0].disabled = True

        tier_select = UserTierSelect_valorant()
        self.add_item(tier_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        self.answer2 = choices
        self.children[1].disabled = True
        line_select = LineSelect_valorant()
        self.add_item(line_select)
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    async def respond_to_answer3(self, interaction: discord.Interaction, choices):
        self.answer3 = choices
        self.children[2].disabled = True
        await interaction.message.edit(view=self)
        await interaction.response.defer()
        # View 종료
        self.stop()
