import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./bbyongbot-firebase-adminsdk-kz1p9-8b90051ca7.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# 멤버 정보를 Firebase에 저장
def save_member_info(member_id, member_info):
    doc_ref = db.collection('members').document(str(member_id))
    doc_ref.set(member_info)

# 멤버 정보를 Firebase에서 불러옴
def get_member_info(member_id):
    doc_ref = db.collection('members').document(str(member_id))
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

# 멤버 정보를 Firebase에서 삭제
def delete_member_info(member_id):
    doc_ref = db.collection('members').document(str(member_id))
    doc_ref.delete()


# 내전 모집 정보를 Firebase에 저장
def save_recruitment_info(recruitment_id, recruitment_info):
    doc_ref = db.collection('내전인원모집').document(str(recruitment_id))
    doc_ref.set(recruitment_info)


# 내전 모집 정보를 Firebase에서 불러옴
def get_recruitment_info(recruitment_id):
    doc_ref = db.collection('내전인원모집').document(str(recruitment_id))
    doc = doc_ref.get()
    if doc.exists:
        recruitment_info = doc.to_dict()
        participants = recruitment_info.get("참여자 목록", [])
        recruitment_info["참여자 목록"] = participants
        return recruitment_info
    else:
        return {"참여자 목록": []}


# 내전 모집 정보를 Firebase에서 삭제
def delete_recruitment_info(recruitment_id, user_id):
    doc_ref = db.collection('내전인원모집').document(str(recruitment_id))
    doc_ref.update({str(user_id): firestore.DELETE_FIELD})


# 참여자 추가 함수
def add_participant(recruitment_id, new_participant):
    doc_ref = db.collection("내전인원모집").document(recruitment_id)
    doc_ref.update({
            "참여자 목록": firestore.ArrayUnion([new_participant])
        })


# 참여자 제거 함수
def remove_participant(recruitment_id, participant_to_remove):
    doc_ref = db.collection('내전인원모집').document(str(recruitment_id))
    doc_ref.update({
        "참여자 목록": firestore.ArrayRemove([participant_to_remove])
    })


# 참여자 목록 불러오기
def get_participant_info(참여자목록):
    멤버정보 = []
    for 참여자ID in 참여자목록:
        # Firestore에서 멤버 정보를 가져오는 적절한 쿼리 작성
        member_doc = db.collection('members').document(참여자ID)
        member_info = member_doc.get().to_dict()
        
        if member_info:
            멤버정보.append(member_info)

    return 멤버정보


# 참여자 이름 불러오기
def get_participant_names(recruitment_id):
    db = firestore.client()
    doc_ref = db.collection('내전인원모집').document(str(recruitment_id))
    doc = doc_ref.get()

    if doc.exists:
        # 참여자 목록 가져오기
        participants = doc.to_dict().get('참여자 목록', [])
        
        # 모든 참여자의 이름 목록 가져오기
        names = [participant.get('이름', '이름 없음') for participant in participants]
        return names

    else:
        print('해당 문서가 존재하지 않습니다.')


#진행 상태 업데이트
def update_match_status(내전코드, new_status):

    user_ref = db.collection('내전인원모집').document(내전코드)
    update_data = {'진행상태': new_status}

    user_ref.update(update_data)

