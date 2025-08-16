# set() 함수는 리스트나 반복 가능한 자료형 중복 제거 하고 고유한 값들 집합으로 만들어줌

import tkinter as tk #tkinter 별칭 사용해서 as 변경
import random
import os

yacht_kind = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Choice", "4 of a Kind", "Full House", "Small Straight", "Large Straight", "Yacht"
] # 요트 다이스에 있는 종류

dice_values = [0,0,0,0,0] #5개 주사위
roll_count = 0 #카운터로 2번 까지 돌릴 수 있게 0으로 초기화
max_rolls = 2 

current_player = 1 #1은 사용자  2 컴퓨터 차례 확인 

player_scores ={kind:None for kind in yacht_kind}
computer_scores = {kind:None for kind in yacht_kind}
# ㄴyacht_kind 리스트에 있는 각 점수 카테고리 키로 하고 초기값 none을 가지는 딕셔너리 
score_buttons={} #빈 딕셔너리 

#-------------------------------점수-----------------------------------------------------
def calculate_score(item,values):
    values = sorted(values) #주사위 값을 오름차순 정렬
    if item == "Ones":
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
        return sum(values)
    
    elif item =="4 of a Kind": #4개의 같은 종류
        for v in set(values): #중복 제거된 숫자 집합 
            if values.count(v) >= 4: #4개 이상 숫자 확인  똑같은 숫자 5개가 나와도 됌 
                return sum(values) 
        return 0 #숫자가 없으면 0 반환
    
    elif item =="Full House":
        counts = [values.count(v) for v in set(values)] #중복 제거 숫자 목록 만들고 몇번 나왔는지 리스트 
        if sorted(counts) == [2,3]: #오름차순 정렬하고 2개 3개 나온 경우 풀 하우스 
            return 25 
        return 0 
    
    elif item == "Small Straight":
        straights = [{1,2,3,4},{2,3,4,5},{3,4,5,6}] #스몰 스트리트 가능한 3가지 집합 정의
        vset = set(values) #중복 제거
        for s in straights: 
            if s.issubset(vset): #미리 정의한 집합에 포함
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
    global dice_values, roll_count #함수 안에 전역변수 수정
    if current_player ==1: # 플레이어 인 경우
        for i in range(5): #5개 주사위
            if not hold_vars[i].get(): #해당 주사위를 고정하지 않은 경우  
                dice_values[i] = random.randint(1,6) #1~6까지 랜덤 숫자 새로고침
    else: # 컴퓨터인 경우
        for i in range(5): #주사위를 모두 새로 굴림
            dice_values[i] = random.randint(1,6) 
    update_labels() # 라벨 업데이트
    update_score_buttons() #굴린 값을 버튼 점수에 업데이트
    roll_count += 1  #주사위 굴린 횟수 1 증가
    roll_button.config(text="굴리기 (" + str(max_rolls - roll_count) + "번 남음)") #남은 횟수
    if roll_count >= max_rolls: # 굴린 횟수가 최대 넘어가면 
        roll_button.config(state="disabled") # 버튼 비활성화

# 주사위 표시 업데이트 하기 
def update_labels():
    for i in range(5):
        if dice_values[i] != 0:
            dice_labels[i].config(image=dice_images[dice_values[i] - 1], text="") #해당 주사위 이미지 확인
        else:
            dice_labels[i].config(image="", text="-") # 아직 주사위 안 굴렸을 땐 -표시

#======================================================================================
#점수 선택 표시 업데이트
def select_score(item): #사용자가 선택한 점수 카테고리
    global current_player 
    score = calculate_score(item, dice_values) #함수 호출해서 주사위값 항목에 점수 계산
    if current_player == 1: 
        if player_scores[item] is None: #점수 아직 기록 안 하면 none 저장
            player_scores[item] = score 
        else: 
            return #이미 점수 있으면 종료
    else: #컴퓨터 인 경우
        if computer_scores[item] is None:
            computer_scores[item] = score
        else:
            return
    end_turn()

#============================================================
#======================턴 종료 ============================
def end_turn(): # 한턴이 끝날 때 호출 
    global current_player, roll_count
    roll_count = 0 #현재 누구 차례이고 몇번 굴렸는지 
    for var in hold_vars:
        var.set(False) #주사위 고정 변수 모음
    roll_button.config(state="normal", text="굴리기 (" + str(max_rolls) + "번 남음)")
    #주사위 버튼 누를 수 있게 활성화 몇번 남았는지 표시
    update_scoreboard() # 점수판 갱신
    
    if all(v is not None for v in player_scores.values()) and all(v is not None for v in computer_scores.values()):
        show_winner() #플레이어 컴퓨터 항목 딕셔너리 (all) 모든 점수 채웠는지 확인
        return

    if current_player == 1:
        current_player = 2 #턴을 끝냈으면 턴을 넘김
    else:
        current_player = 1
    turn_label.config(text="현재 턴: " + ("플레이어" if current_player == 1 else "컴퓨터"))
    #화면에 턴 표시
    if current_player == 2:
        root.after(1000, computer_turn) #만약 컴퓨터 차례라면 컴퓨터_턴 함수 자동 실행

#==================컴퓨터 턴=================================
# 컴퓨터 턴
def computer_turn():
    roll_dice() 
    root.after(1000, computer_second_roll)
    #1초후 실행

def computer_second_roll():
    roll_dice()
    root.after(1000, computer_choose_score)
    #항상 두번만 굴리고 점수 선택

def computer_choose_score():
    available = [k for k, v in computer_scores.items() if v is None]
    best_choice = max(available, key=lambda c: calculate_score(c, dice_values))
    select_score(best_choice) 
    #가능한 점수가 높은 항목 선택하게 하기

#======================점수판 업데이트========================
def update_scoreboard():
    player_text = "플레이어 점수\n" + "\n".join([k + ": " + (str(v) if v is not None else "-") for k, v in player_scores.items()])
    computer_text = "컴퓨터 점수\n" + "\n".join([k + ": " + (str(v) if v is not None else "-") for k, v in computer_scores.items()])
    player_score_label.config(text=player_text)
    computer_score_label.config(text=computer_text)

#=====================버튼 활성화 승자 표시======================
def update_score_buttons():
    for category in yacht_kind: 
        if current_player == 1 and player_scores[category] is None:
            possible_score = calculate_score(category, dice_values)
            score_buttons[category].config(text=category + " (" + str(possible_score) + ")", state="normal")
        else:
            score_buttons[category].config(state="disabled")

# 승자 표시
def show_winner():
    player_total = sum(v for v in player_scores.values() if v is not None)
    computer_total = sum(v for v in computer_scores.values() if v is not None)
    if player_total > computer_total:
        result = "플레이어 승리!"
    elif player_total < computer_total:
        result = "컴퓨터 승리!"
    else:
        result = "무승부!"
    turn_label.config(text=result + " (플레이어 " + str(player_total) + " vs 컴퓨터 " + str(computer_total) + ")")
    roll_button.config(state="disabled")
    for btn in score_buttons.values():
        btn.config(state="disabled")

#============================================================

root = tk.Tk()
root.title("요트 다이스") # 타이틀 이름 변경
root.geometry("1000x1000") #창 사이즈

base_path = os.path.dirname(__file__)
dice_images = [
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice1.png")),
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice2.png")),
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice3.png")),
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice4.png")),
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice5.png")),
    tk.PhotoImage(file=os.path.join(base_path, "image", "dice6.png")),
] #이미지 불러오기

# 턴 표시
turn_label = tk.Label(root, text="현재 턴: 플레이어", font=("Arial", 14))
turn_label.pack()   #현재 턴 표시

# 주사위 UI
dice_labels = []
hold_vars = []
frame_dice = tk.Frame(root)
frame_dice.pack(pady=10)
for i in range(5):
    frame = tk.Frame(frame_dice)
    frame.pack(side="left", padx=5)
    lbl = tk.Label(frame, text="-", font=("Arial", 20))
    lbl.pack()
    dice_labels.append(lbl)
    var = tk.BooleanVar()
    chk = tk.Checkbutton(frame, text="고정", variable=var)
    chk.pack()
    hold_vars.append(var)

    #주사위 5개를 반복해서 만듦

# 굴리기 버튼
roll_button = tk.Button(root, text="굴리기 (" + str(max_rolls) + "번 남음)", command=roll_dice)
roll_button.pack(pady=10)  #굴리기 버튼

# 점수판 버튼
frame_score = tk.Frame(root)
frame_score.pack()
for category in yacht_kind:
    btn = tk.Button(frame_score, text=category, command=lambda c=category: select_score(c))
    btn.pack(side="left", padx=2)
    score_buttons[category] = btn 
    #점수판 선택 버튼 버튼 실행해서 점수 기록 

# 점수판 라벨
frame_boards = tk.Frame(root)
frame_boards.pack(pady=10)
player_score_label = tk.Label(frame_boards, text="", font=("Arial", 12), justify="left")
player_score_label.pack(side="left", padx=20)
computer_score_label = tk.Label(frame_boards, text="", font=("Arial", 12), justify="left")
computer_score_label.pack(side="left", padx=20)
#점수판 표시 구역 

update_scoreboard()
root.mainloop() #처음 점수판 갱신/ trkinter 실행 시작
