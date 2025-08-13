# set() 함수는 리스트나 반복 가능한 자료형 중복 제거 하고 고유한 값들 집합으로 만들어줌

import tkinter as tk #tkinter 별칭 사용해서 as 변경
import random

yacht_kind = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Choice", "4 of a Kind", "Full House", "Small Straight", "Large Straight", "Yacht"
] # 요트 다이스에 있는 종류

dice_values = [0,0,0,0,0] #5개 주사위
rool_count = 0 #카운터로 2번 까지 돌릴 수 있게 0으로 초기화
max_rools =2 

player = 1 #1은 사용자  2 컴퓨터 차례 확인 

player_score ={kind:None for cat in yacht_kind}
computer_scores = {kind:None for cat in yacht_kind}
# ㄴyacht_kind 리스트에 있는 각 점수 카테고리 키로 하고 초기값 none을 가지는 딕셔너리 
score_button={} #빈 딕셔너리 

#-------------------------------점수-----------------------------------------------------
def total_scores(item,values):
    values = sorted(values) #주사위 값을 오름차순 정렬
    if item == "Oens":
        return values.count(1)*1 #주사위가 1인 개수를 카운트 하는데 *1은 점수 계산 하기위해 사용 1이 2개 *1 을통해 2점
    elif item =="Twos":
        return values.count(2)*2
    elif item =="Threes":
        return values.count(3)*3
    elif item =="Fours":
        return values.count(4)*4
    elif item =="Fives":
        return values.count(5)*5
    elif item =="Sixes":
        return values.count(6)*6
    elif item =="Choice":  #원래는 1~6까지 특정 합을 채우면 추가 점수를 받는데 실력 미흡으로 대체 합계를 더 받게 함
        return sum (values)
    
    elif item =="4 of a kind": #4개의 같은 종류
        for v in set(values): #중복 제거된 숫자 집합 
            if values.count(v) >= 4: #4개 이상 숫자 확인  똑같은 숫자 5개가 나와도 됌 
                return sum(values) 
        return(0) #숫자가 없으면 0 반환
    
    elif item =="Full house":
        counts = [values.count(v) for v in set(values)] #중복 제거 숫자 목록 만들고 몇번 나왔는지 리스트 
        if sorted(counts) == [2,3]: #오름차순 정렬하고 2개 3개 나온 경우 풀 하우스 
            return 25 
        return 0 
    
    elif item == "Small Straight":
        straights = [{1,2,3,4},{2,3,4,5},{3,4,5,6}] #스몰 스트리트 가능한 3가지 집합 정의
        vset = set(values) #중복 제거
        for s in straights: 
            if s.subset(vset): #미리 정의한 집합에 포함
                return 30
        return 0
    
    elif item =="Large Straight":
        if set(values) == {1,2,3,4,5} or set(values) == {2,3,4,5,6}: #미리 정의 
            return 40
        return 0
    elif item =="Yacht":
        if len(set(values)) ==1: #주사위 5개가 모두 같은 숫자 일 때 의미 set을 통해 중복 하면 1이 되니깐 
            return 50 #50점
        return 0 #없으면 0
    return 0  #아무것도 해당 안되면 0점
#-------------------------------점수-----------------------------------------------------

#주사위 굴리기
def roll_dice():
    global dice_values #함수 안에 전역변수 수정
    if current_player ==1: # 플레이어 인 경우
        for i in range(5): #5개 주사위
            if not hold_vars[i].get(): #해당 주사위를 고정하지 않은 경우  
                dice_values[i] = random.randint(1,6) #1~6까지 랜덤 숫자 새로고침
    else: # 컴퓨터인 경 우
        for i in range(5): #주사위를 모두 새로 굴림
            dice_values[i] = random.randint(1,6) 
    update_labels() # 라벨 업데이트
    update_score_button() #굴린 값을 버튼 점수에 업데이트
    rool_count+=1  #주사위 굴린 횟수 1 증가
    roll_button.config(text="굴리기 (" + str(max_rolls - roll_count) + "번 남음)") #남은 횟수
    if rool_count >= max_rools: # 굴린 횟수가 최대 넘어가면 
        roll_button.config(state="disabled") # 버튼 비활성화
# 주사위 표시 업데이트 하기 
def update_labels():
    for i in range(5):
         dice_labels[i].config(image=dice_images[dice_values[i] - 1], text="") #해당 주사위 이미지 확인
    else:
            dice_labels[i].config(image="", text="-") # 아직 주사위 안 굴렸을 땐 -표시
#======================================================================================


#윈도우 기본 설정

root = tk.Tk() 
root.title("요트 다이스") # 타이틀 이름 변경
root.geometry("500x500") #창 사이즈

dice_labels = [] #주사위 표시
for i in range(5):
    lbl = tk.Label(root, text= "-",font=("arial",20)) 
    lbl.pack(side = "left",padx = 5) #위젯을 pack으로 배치하고 왼쪽부터 붙인다 5픽셀 여백
    dice_labels.append(lbl) #라벨을 담아두는 리스트 append로 추가

roll_button = tk.Button(root,text="굴리기",command=roll_dice)
#ㄴ버튼 위젯을 만들고 root 윈도우창 command 버튼 클릭시 roll_dice 함수 실행
roll_button.pack(pady = 10) #버튼에 대한 여백 추가 

score_label = tk.Label(root, text = "합계 : 0",font=("arial",14))
score_label.pack()

root.mainloop()


