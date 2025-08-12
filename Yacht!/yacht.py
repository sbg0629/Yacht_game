import tkinter as tk
import random

# 요트 다이스 카테고리
categories = [
    "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",
    "Choice", "4 of a Kind", "Full House", "Small Straight", "Large Straight", "Yacht"
]

# 초기값 설정
dice_values = [0] * 5
roll_count = 0
max_rolls = 2
current_player = 1  # 1: 플레이어, 2: 컴퓨터
player_scores = {cat: None for cat in categories}
computer_scores = {cat: None for cat in categories}
score_buttons = {}

# 점수 계산 함수
def calculate_score(category, values):
    values = sorted(values)
    if category == "Ones":
        return values.count(1) * 1
    elif category == "Twos":
        return values.count(2) * 2
    elif category == "Threes":
        return values.count(3) * 3
    elif category == "Fours":
        return values.count(4) * 4
    elif category == "Fives":
        return values.count(5) * 5
    elif category == "Sixes":
        return values.count(6) * 6
    elif category == "Choice":
        return sum(values)
    elif category == "4 of a Kind":
        for v in set(values):
            if values.count(v) >= 4:
                return sum(values)
        return 0
    elif category == "Full House":
        counts = [values.count(v) for v in set(values)]
        if sorted(counts) == [2, 3]:
            return 25
        return 0
    elif category == "Small Straight":
        straights = [{1,2,3,4}, {2,3,4,5}, {3,4,5,6}]
        valset = set(values)
        for s in straights:
            if s.issubset(valset):
                return 30
        return 0
    elif category == "Large Straight":
        if set(values) == {1,2,3,4,5} or set(values) == {2,3,4,5,6}:
            return 40
        return 0
    elif category == "Yacht":
        if len(set(values)) == 1:
            return 50
        return 0
    return 0

# 주사위 굴리기
def roll_dice():
    global roll_count
    if current_player == 1:
        for i in range(5):
            if not hold_vars[i].get():
                dice_values[i] = random.randint(1, 6)
    else:
        for i in range(5):
            dice_values[i] = random.randint(1, 6)
    update_labels()
    update_score_buttons()
    roll_count += 1
    roll_button.config(text="굴리기 (" + str(max_rolls - roll_count) + "번 남음)")
    if roll_count >= max_rolls:
        roll_button.config(state="disabled")

# 주사위 표시 업데이트
def update_labels():
    for i in range(5):
        dice_labels[i].config(text=str(dice_values[i]))

# 점수 선택
def select_score(category):
    global current_player
    score = calculate_score(category, dice_values)
    if current_player == 1:
        if player_scores[category] is None:
            player_scores[category] = score
        else:
            return
    else:
        if computer_scores[category] is None:
            computer_scores[category] = score
        else:
            return
    end_turn()

# 턴 종료
def end_turn():
    global current_player, roll_count
    roll_count = 0
    for var in hold_vars:
        var.set(False)
    roll_button.config(state="normal", text="굴리기 (" + str(max_rolls) + "번 남음)")
    update_scoreboard()

    # 게임 종료 체크
    if all(v is not None for v in player_scores.values()) and all(v is not None for v in computer_scores.values()):
        show_winner()
        return

    # 턴 변경
    if current_player == 1:
        current_player = 2
    else:
        current_player = 1
    turn_label.config(text="현재 턴: " + ("플레이어" if current_player == 1 else "컴퓨터"))

    if current_player == 2:
        root.after(1000, computer_turn)

# 컴퓨터 턴
def computer_turn():
    roll_dice()
    root.after(1000, computer_second_roll)

def computer_second_roll():
    roll_dice()
    root.after(1000, computer_choose_score)

def computer_choose_score():
    available = [k for k, v in computer_scores.items() if v is None]
    best_choice = max(available, key=lambda c: calculate_score(c, dice_values))
    select_score(best_choice)

# 점수판 업데이트
def update_scoreboard():
    player_text = "플레이어 점수\n" + "\n".join([k + ": " + (str(v) if v is not None else "-") for k, v in player_scores.items()])
    computer_text = "컴퓨터 점수\n" + "\n".join([k + ": " + (str(v) if v is not None else "-") for k, v in computer_scores.items()])
    player_score_label.config(text=player_text)
    computer_score_label.config(text=computer_text)

# 버튼 활성화/비활성화 및 예상 점수 표시
def update_score_buttons():
    for category in categories:
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

# ---------------------------
# Tkinter UI
# ---------------------------
root = tk.Tk()
root.title("요트 다이스")
root.geometry("800x500")

# 턴 표시
turn_label = tk.Label(root, text="현재 턴: 플레이어", font=("Arial", 14))
turn_label.pack()

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

# 굴리기 버튼
roll_button = tk.Button(root, text="굴리기 (" + str(max_rolls) + "번 남음)", command=roll_dice)
roll_button.pack(pady=10)

# 점수판 버튼
frame_score = tk.Frame(root)
frame_score.pack()
for category in categories:
    btn = tk.Button(frame_score, text=category, command=lambda c=category: select_score(c))
    btn.pack(side="left", padx=2)
    score_buttons[category] = btn

# 점수판 라벨
frame_boards = tk.Frame(root)
frame_boards.pack(pady=10)
player_score_label = tk.Label(frame_boards, text="", font=("Arial", 12), justify="left")
player_score_label.pack(side="left", padx=20)
computer_score_label = tk.Label(frame_boards, text="", font=("Arial", 12), justify="left")
computer_score_label.pack(side="left", padx=20)

update_scoreboard()
root.mainloop()
