import discord
import random

#채팅 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

async def 선택지_매크로(client, message):

    if message.author == client.user:
        return
    
    if '현우' in message.content and '게이' in message.content:
            await message.add_reaction('⭕') 

        
    if message.content.startswith('마법의'):
        if '뿅뿅' in message.content and '님' in message.content:

            ok_or_no = ['되나요', '되냐', '돼', '될까요', '됩니까', '될랑가', '있을까요', '잇을까']
            ok_responses = ['된다 뿅!', '안된다 뿅.']
            correct_or_not = ['맞나요', '가요', '일까요', '입니까', '맞습니까', '을까요', '마즐']
            correct_responses = ['맞다 뿅!', '아니다 뿅.']
            생긴다_responses = ['생긴다 뿅!', '안 생긴다 뿅.']

            if any(keyword in message.content for keyword in ok_or_no):
                response = random.choice(ok_responses)
                await message.channel.send(response)
                return

            if any(keyword in message.content for keyword in correct_or_not):
                response = random.choice(correct_responses)
                await message.channel.send(response)
                return
                
            if message.content.endswith('생길까요') or message.content.endswith ('생길까'):
                response = random.choice(생긴다_responses)
                await message.channel.send(response)
                return    
            
    if 'vs' in message.content:
        choices = message.content.split(' vs ')
        if len(choices) >= 2:
            selected_choice = random.choice(choices)
            await message.channel.send(f'{selected_choice}')
            return

    if '맵 랜덤' in message.content or '맵 추천' in message.content:
        maplist = ['헤이븐', '아이스박스', '로터스', '어센트', '프렉쳐', '브리즈', '선셋', '바인드', '스플릿']
        random_map = random.choice(maplist)
        await message.channel.send(f'__**{random_map}**__ 맵을 추천한다 뿅!')

    if '라인 추천' in message.content or '라인추천' in message.content:
        lane_list = ['탑', '미드', '정글', '원딜', '서폿']
        random_lane = random.choice(lane_list)
        await message.channel.send(f'추천 라인은 __**{random_lane}**__ 이다 뿅!')

    if '아메추' in message.content:
        morning = ['돌', '물', '모래', '자갈', '수건', '비누', '치약', '닭고기 사료',
                 '소고기 사료', '잡초', '민들레', '장미']
        random_morning = random.choice(morning)
        await message.channel.send(f'뿅뿅이의 아침 추천 메뉴는 __**{random_morning}**__ 이다 뿅!')

    if '점메추' in message.content:
        lunch = ['부대찌개', '햄버거', '파스타', '돈까스', '우동', '김밥', '떡볶이', '마라탕', '제육볶음', '칼국수',
                 '불고기 덮밥', '순대국밥', '돌', '쌀국수', '짜장면', '짬뽕', '함박 스테이크',
                 '초밥', '샌드위치', '핫도그']
        random_lunch = random.choice(lunch)
        await message.channel.send(f'뿅뿅이의 점심 추천 메뉴는 __**{random_lunch}**__ 이다 뿅!')
    
    if '저메추' in message.content:
        dinner = ['치킨','피자','막창','곱창','삼겹살','부대찌개','마라탕', '짜장면','짬뽕',
                 '라면', '불닭볶음면', '막창', '낙곱새', '제육볶음', '칼국수', '우동', '떡볶이',
                 '카레', '사료', '김치볶음밥', '햄버거', '보쌈', '닭발', '초밥', '닭강정']
        random_dinner = random.choice(dinner)
        await message.channel.send(f'뿅뿅이의 저녁 추천 메뉴는 __**{random_dinner}**__ 이다 뿅!')

async def 이미지_매크로(client, message):
    # 봇이 자신의 메시지에 반응하지 않도록 처리
    if message.author == client.user:
        return
    
    if message.content.startswith('우마이'):
        embed = discord.Embed(title="혼자 먹으니 맛있냐 뿅", color=discord.Color.blue())
        embed.set_image(url="https://i.ibb.co/1G26c5d/Kakao-Talk-20240208-190649265.jpg") #한심뿅2
        await message.channel.send(embed=embed)
        return

    if message.content.startswith("뿅"):
                
        if "앉아" in message.content:
            embed = discord.Embed(title="앉았다 뿅!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/4KR4LzB/image.jpg") #앉아뿅
            await message.channel.send(embed=embed)
            return

        if "산책" in message.content:
            embed = discord.Embed(title="산책은 늘 즐겁다 뿅!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/JxwGRzb/2.jpg") #해맑뿅2
            await message.channel.send(embed=embed)
            return
        
        if "굴러" in message.content:
            
            embed = discord.Embed(title="그런걸 내가 어떻게 하냐 뿅..", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/3svmrSZ/image.jpg") #한심좌뿅
            await message.channel.send(embed=embed)
            return
        
        if "손" in message.content:
            embed = discord.Embed(title="됐냐 뿅!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/YX0gNT3/image.jpg") #손뿅
            await message.channel.send(embed=embed)
            return

        if "엎드려" in message.content:
            embed = discord.Embed(title=".oO(간식은 언제 주는거냐 뿅)", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/ZXGM91W/image.jpg") #엎드려뿅
            await message.channel.send(embed=embed)
            return
        
        if "간식" in message.content:
            embed = discord.Embed(title="나는 고기 간식이 좋다 뿅!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/6bc0MRV/1.jpgg") #해맑뿅 1
            await message.channel.send(embed=embed)
            return
        
        if "목욕" in message.content:
            embed = discord.Embed(title="싫다!! 목욕 싫다 뿅!!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/jvvgLBC/image.jpg") #절망뿅
            await message.channel.send(embed=embed)
            return
        
        if "빵" in message.content:
            embed = discord.Embed(title="꾸엑 x_x", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/zGxWbhX/image.jpg") #빵뿅
            await message.channel.send(embed=embed)
            return
        
        if "혼날래" in message.content:
            embed = discord.Embed(title="내가 뭘 잘못했다고 그러냐 뿅..", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/L8xTm13/2.jpg") #엎드려뿅2
            await message.channel.send(embed=embed)
            return
        
        if "물어" in message.content:
            embed = discord.Embed(title="아르르... 뿅뿅!!!", color=discord.Color.blue())
            embed.set_image(url="https://i.ibb.co/jVCGRcB/image.jpg") #짐승뿅
            await message.channel.send(embed=embed)
            return
    

async def 채팅_매크로(client, message):
    # 봇이 자신의 메시지에 반응하지 않도록 처리
    if message.author == client.user:
        return
    
    
    # 사용자가 해당 조건을 입력했을 
    hello_patterns = ['안녕', 'ㅎㅇ', 'hello', '하잉', '반가', '하이','하위', '하윙', '하이루']
    bye_patterns = ['ㅂㅂ', 'ㅃㅃ', 'bye', 'ㅃㅇ', '빠빠', '빠이', 'ㅂㅇ', '잘가', '빠잉']
    curse_patterns = ['시발','쉬발','씨발','시1발','ㅅㅂ','ㅆㅂ','ㅅ1ㅂ','tlqkf','시불',
                      '병신','븅신','비융신','뵹신','병1신','ㅂㅅ','ㅄ','병1신','등신', '비웅신'
                      '존나','존1나','ㅈㄴ','줜내','줜나','쥰내','쥰나','죤내','죤나','줘언나',
                      '지랄','지1랄','쥐랄','ㅈㄹ',
                      '이새끼','저새끼','개새','씹새','개가튼',
                      '빠큐','뻐큐','fuck','ㅗ','엿쳐','엿처',
                      '좆','조까','줮같','ㅈ같','ㅈ가','ㅈ까',
                      '옘병', '썅', 
                      '닥쳐','ㄷㅊ','닥1쳐',
                      '꺼져','ㄲㅈ','껒여',
                      ]

    # 각 패턴에 맞게 상응하여 설정한 답변값 중 하나를 랜덤하게 출력
    for pattern in hello_patterns:
        if message.content.startswith (pattern) or message.content.endswith (pattern) :
                 # 사용자가 해당 패턴을 입력한 횟수 증가
            client.user_pattern_counts[message.author.id] += 1

            # 5번 입력할 때마다 유저를 언급하며 새로운 문장 출력
            if client.user_pattern_counts[message.author.id] % 5 == 0:
                user = await client.fetch_user(message.author.id)
                mention = user.mention
                await message.channel.send(f'{mention} 인사를 대체 몇 번이나 하는 거냐 뿅!')
                return
            
            responses = ['반갑다 뿅!', '안녕 뿅!', '만나서 반갑다 뿅!', 'Hi.', '반갑개!']
            response = random.choice(responses)
            await message.channel.send(response)
            return

    for pattern in bye_patterns:
        if message.content.startswith (pattern) or message.content.endswith (pattern) :
            responses = ['잘가 뿅!', '재밌었다 뿅!', '잘가개!', '즐거웠다 뿅!', 'Bye, Honey~♡']
            response = random.choice(responses)
            await message.channel.send(response)
            return
    
    for pattern in curse_patterns:
        if pattern in message.content:
            client.user_pattern_counts[message.author.id] += 1

            if client.user_pattern_counts[message.author.id] % 5 == 0:
                user = await client.fetch_user(message.author.id)
                mention = user.mention
                await message.reply(f'{mention} 욕을 너무 많이 한다 뿅!')
                return
                
            responses = ['욕은 나쁜거다 뿅!', '왜 욕을 하고 그러냐 뿅!', '착한 말을 쓰자 뿅!', '어디서 욕질이야 이새끼가']
            response = random.choice(responses)
            await message.reply(response)
            return


    # 사용자가 ㅇㅅㅇ를 입력하면
    if 'ㅇㅅㅇ' in message.content:
        await message.channel.send('우리 서버는 ㅇㅅㅇ 하는 사람 없어서 좋다 뿅...')
        return

    if '♡' in message.content:
        love = message.content.split(' ♡ ')
        if len(love) == 2:
            await message.channel.send('두 사람의 사랑을 응원한다 뿅!')
            return




