# 主食
# 0 -> 1
# 1 -> 1.5
# 2 -> 2
# 副菜
# 3 -> 1
# 主菜
# 4 -> 1
# 5 -> 2 
# 6 -> 3
# else
# 7

# 主食は5~7
# 副菜は5~6
# 主菜は3~5
def step_logic(step: int):
    # ~2700歩未満で1点
    # 2700歩~4400歩未満で2点
    # 4400歩~8000歩未満で3点
    # 8000歩~11000歩未満で4点
    # 11000歩以上で5点
    step_health_level = 0
    if step < 2700:
        step_health_level = 1
    elif 2700 <= step < 4400:
        step_health_level = 2
    elif 4400 <= step < 8000:
        step_health_level = 3
    elif 8000 <= step < 11000:
        step_health_level = 4
    elif 11000 <= step:
        step_health_level = 5
    return step_health_level

def dish_logic(history_info_24):
    sum_stapleValue = 0
    sum_sideValue = 0
    sum_mainValue = 0

    status_stapleValue = 0
    status_sideValue = 0
    status_mainValue = 0

    dish_health_level_sum = 0

    for history_info in history_info_24:
        sum_stapleValue += history_info.stapleValue
        sum_sideValue += history_info.sideValue
        sum_mainValue += history_info.mainValue
    
    # 1日の目安
    # 主食は5~7
    # 副菜は5~6
    # 主菜は3~5 

    if 5 <= sum_stapleValue <=7:
        # ちょうどいい
        dish_health_level_sum += 3
        status_stapleValue = 5
    elif 8 <= sum_stapleValue <= 10:
        # 少し食べ過ぎ
        dish_health_level_sum += 4
        status_stapleValue = 4
    elif sum_stapleValue >= 11:
        # かなり食べ過ぎ
        dish_health_level_sum += 5
        status_stapleValue = 2
    elif 2 <= sum_stapleValue <= 4:
        dish_health_level_sum += 2
        status_stapleValue = 3
    elif sum_stapleValue <= 1:
        dish_health_level_sum += 1
        status_stapleValue = 1

    if 5 <= sum_sideValue <=6:
        # ちょうどいい
        dish_health_level_sum += 3
        status_sideValue = 5
    elif 7 <= sum_sideValue <= 9:
        # 少し食べ過ぎ
        dish_health_level_sum += 4
        status_sideValue = 4
    elif sum_sideValue >= 10:
        # かなり食べ過ぎ
        dish_health_level_sum += 5
        status_sideValue = 2
    elif 2<= sum_sideValue <= 4:
        dish_health_level_sum += 2
        status_sideValue = 3
    elif sum_stapleValue <= 1:
        dish_health_level_sum += 1
        status_sideValue = 1

    if 3 <= sum_mainValue <=5:
        # ちょうどいい
        dish_health_level_sum += 3
        status_mainValue = 5
    elif 6 <= sum_mainValue <= 8:
        # 少し食べ過ぎ
        dish_health_level_sum += 4
        status_mainValue = 4
    elif sum_mainValue >= 9:
        # かなり食べ過ぎ
        dish_health_level_sum += 5
        status_mainValue = 2
    elif 1 <= sum_mainValue <= 2:
        dish_health_level_sum += 2
        status_mainValue = 3
    elif sum_mainValue <= 0:
        dish_health_level_sum += 1
        status_mainValue = 1

    dish_health_level = 0
    if dish_health_level_sum == 9:
        dish_health_level = 5
    elif 10 <= dish_health_level_sum < 13:
        # 少し食べ過ぎ
        dish_health_level = 3
    elif 13 <= dish_health_level_sum:
        # かなり食べ過ぎ
        dish_health_level = 4
    elif 6 <= dish_health_level_sum < 9:
        # 少し食べてない
        dish_health_level = 2
    elif dish_health_level_sum < 6:
        dish_health_level = 2
    
    return dish_health_level,status_stapleValue, status_sideValue, status_mainValue

def decide_status(step, history_info_24):
    step_health_level = step_logic(step)
    dish_health_level, status_stapleValue, status_sideValue, status_mainValue = dish_logic(history_info_24)
    # health_level = step_health_level + dish_health_level
    print("step_health_level", step_health_level)
    print("dish_health_level", dish_health_level)
    status = 0
    if step_health_level == 5:
        if dish_health_level == 5:
            # ちょうどいい
            status = 3
        elif dish_health_level == 4:
            # かなり食べ過ぎ
            status = 5
        elif dish_health_level == 3:
            # 少し食べ過ぎ
            status = 4
        elif dish_health_level == 2 or dish_health_level == 1:
            # 少し食べてない
            status = 2
    elif step_health_level == 4:
        if dish_health_level == 5:
            # ちょうどいい
            status = 4
        elif dish_health_level == 4:
            # かなり食べ過ぎ
            status = 5
        elif dish_health_level == 3:
            # 少し食べ過ぎ
            status = 5
        elif dish_health_level == 2 or dish_health_level == 1:
            # 少し食べてない
            status = 2
    elif step_health_level == 3:
        if dish_health_level == 5:
            # ちょうどいい
            status = 4
        elif dish_health_level == 4:
            # かなり食べ過ぎ
            status = 5
        elif dish_health_level == 3:
            # 少し食べ過ぎ
            status = 5
        elif dish_health_level == 2 or dish_health_level == 1:
            # 少し食べてない
            status = 2
    elif step_health_level == 2:
        if dish_health_level == 5:
            # ちょうどいい
            status = 5
        elif dish_health_level == 4:
            # かなり食べ過ぎ
            status = 5
        elif dish_health_level == 3:
            # 少し食べ過ぎ
            status = 5
        elif dish_health_level == 2 or dish_health_level == 1:
            # 少し食べてない
            status = 2
    elif step_health_level == 1:
        if dish_health_level == 5:
            # ちょうどいい
            status = 4
        elif dish_health_level == 4:
            # かなり食べ過ぎ
            status = 5
        elif dish_health_level == 3:
            # 少し食べ過ぎ
            status = 5
        elif dish_health_level == 2 or dish_health_level == 1:
            # 少し食べてない
            status = 2
    return status, status_stapleValue, status_sideValue, status_mainValue
