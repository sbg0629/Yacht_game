import tkinter as tk #tkinter 별칭 사용해서 as 변경
import random

dice_values = [0,0,0,0,0] #5개 주사위

def roll_dice():
    global dice_values #함수 안에 전역변수 수정
    dice_values = [random.randint(1,6) for _ in range(5)] 
    # ㄴ리스트 컴프리헨션 문법 변수 이름을 _ 해서 값을 쓰지 않지만 5번 반복 
    update_labels() #화면 ui에 변수 갱신 없으면 안 보여짐
    score_label.config(text="합계: " + str(sum(dice_values))) #합계 계산해서 점수 라벨에 표시
    # ㄴ config은 tkinter의 위젯은 생성후 속성을 바꿀 수 있는 함수 가지고 있음

def update_labels():
    for i in range(5):
        dice_labels[i].config(text=str(dice_values[i]))

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


