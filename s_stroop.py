from psychopy import visual, core, event, gui
import random
import csv

# ==== 添加对话框，收集参与者信息（编号 + 年龄）====
participant_info = {
    '参与者编号 (如001)': '',
    '年龄': ''
}
dlg = gui.DlgFromDict(participant_info, title='实验信息')
if not dlg.OK or participant_info['参与者编号 (如001)'] == '' or participant_info['年龄'] == '':
    core.quit()

participant_id = participant_info['参与者编号 (如001)']
participant_age = participant_info['年龄']
filename = f"data_{participant_id}.csv"


# 创建窗口
win = visual.Window(fullscr=True, color='white', units='height')

# 设置字体
FONT_NAME = 'Microsoft YaHei'  # 确保支持中文

# 显示欢迎界面
# 显示欢迎界面
def show_instruction():
    # 主文本内容（将分成多个部分绘制）
    text_lines = [
        "欢迎参加实验！",
        "在这个实验中，你会看到用不同颜色印刷的符号和颜色词，",
        "你的任务是尽可能快速地按键报告字的印刷颜色：",
        "红（1），黑（2），蓝（3），绿（4）",
        "",
        "按任意键开始实验……"
    ]
    
    # 先绘制黑色文本部分
    for i, line in enumerate(text_lines):
        if line not in ["红（1），黑（2），蓝（3），绿（4）", ""]:
            text_stim = visual.TextStim(
                win,
                text=line,
                color='black',
                height=0.04,
                font=FONT_NAME,
                pos=(0, 0.2 - i*0.08),
                alignText='center',
                bold=False
            )
            text_stim.draw()
    
    # 单独绘制彩色文字部分（保持在同一行）
    color_words = [
        ("红", 'red', -0.3),
        ("黑", 'black', -0.1),
        ("蓝", 'blue', 0.1),
        ("绿", 'green', 0.3)
    ]
    
    # 绘制彩色字
    for word, color, x_pos in color_words:
        word_stim = visual.TextStim(
            win,
            text=word,
            color=color,
            height=0.04,
            font=FONT_NAME,
            pos=(x_pos, -0.1),
            alignText='center',
            bold=False
        )
        word_stim.draw()
    
    # 绘制数字部分（黑色）
    for i, (_, _, x_pos) in enumerate(color_words):
        num_stim = visual.TextStim(
            win,
            text=f"（{i+1}）",
            color='black',
            height=0.04,
            font=FONT_NAME,
            pos=(x_pos+0.05, -0.1),  # 数字稍微右移
            alignText='center',
            bold=False
        )
        num_stim.draw()
        # 绘制逗号（除了最后一个）
        if i < len(color_words)-1:
            comma_stim = visual.TextStim(
                win,
                text="，",
                color='black',
                height=0.04,
                font=FONT_NAME,
                pos=(x_pos+0.12, -0.1),
                alignText='center',
                bold=False
            )
            comma_stim.draw()
    
    win.flip()
    event.waitKeys()

# 定义颜色和对应按键
colors = ['red', 'black', 'blue', 'green']
color_keys = {'red': '1', 'black': '2', 'blue': '3', 'green': '4'}
color_words = {'red': '红', 'black': '黑', 'blue': '蓝', 'green': '绿'}

# 构建 trial 列表
def build_trials():
    trials = []
    for condition in ['Congruent', 'Incongruent', 'Neutral']:
        for _ in range(20):
            ink_color = random.choice(colors)
            if condition == 'Congruent':
                text = color_words[ink_color]
            elif condition == 'Incongruent':
                wrong_colors = [c for c in colors if c != ink_color]
                text = color_words[random.choice(wrong_colors)]
            else:  # Neutral
                text = 'XXXX'
            trials.append({'condition': condition, 'text': text, 'color': ink_color})
    return balance_trials(trials)

# 不允许连续相同条件或颜色超过两次
def balance_trials(trials):
    max_attempts = 10000
    for _ in range(max_attempts):
        random.shuffle(trials)
        valid = True
        for i in range(2, len(trials)):
            # 检查条件是否连续3次相同
            condition_check = (trials[i]['condition'] == trials[i-1]['condition'] == trials[i-2]['condition'])
            
            # 检查颜色是否连续3次相同
            color_check = (trials[i]['color'] == trials[i-1]['color'] == trials[i-2]['color'])
            
            # 检查"条件+颜色"组合是否连续3次相同（新增）
            combo_check = ((trials[i]['condition'], trials[i]['color']) == 
                          (trials[i-1]['condition'], trials[i-1]['color']) == 
                          (trials[i-2]['condition'], trials[i-2]['color']))
            
            if condition_check or color_check or combo_check:
                valid = False
                break
                
        if valid:
            return trials
            
    raise Exception("无法平衡试次。请重试。建议减少每种条件的试次数或增加最大尝试次数。")

# 显示 trial 并记录反应
def run_trial(text, color):
    stim = visual.TextStim(
        win,
        text=text,
        color=color,
        height=0.1,
        font=FONT_NAME
    )
    stim.draw()
    win.flip()
    clock = core.Clock()
    keys = event.waitKeys(maxWait=2.0, keyList=['1', '2', '3', '4', 'escape'], timeStamped=clock)
    win.flip()
    if keys:
        key, rt = keys[0]
        if key == 'escape':
            win.close()
            core.quit()
        return key, rt
    else:
        return None, None

# ==== 修改后的实验主函数 ====
def run_experiment():
    show_instruction()
    trials = build_trials()
    results = []

    for trial in trials:
        key, rt = run_trial(trial['text'], trial['color'])
        correct = key == color_keys[trial['color']] if key else False
        results.append({
        'participant_id': participant_id,
        'age': participant_age,
        'condition': trial['condition'],
        'stimulus': trial['text'],
        'ink_color': trial['color'],
        'key_pressed': key,
        'correct': correct,
        'reaction_time': rt
    })

        core.wait(0.5)

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    end = visual.TextStim(win, text='实验结束，感谢参与！', font=FONT_NAME, color='black', height=0.05)
    end.draw()
    win.flip()
    event.waitKeys()
    win.close()
    core.quit()

# ==== 启动实验 ====
run_experiment()
