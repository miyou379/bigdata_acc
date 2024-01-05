import pandas as pd
import os
import time
import warnings

## Disable the FutureWarning of concat
warnings.filterwarnings("ignore", message="The behavior of DataFrame concatenation with empty or all-NA entries is deprecated")

df_col = ["平台", "题号", "标题", "难度", "日期"]

## Initialize time
day = time.strftime(r"%y/%m/%d/%H", time.localtime())

## Initialize platforms
plat_name = []
plat_name.append(["uva", "uvaoj", "uvaonlinejudge"]) ## No. 1 UVa OJ
plat_name.append(["atcoder", "ac"]) ## No. 2 AtCoder
plat_name.append(["codeforce", "cf", "codeforces"]) ## No. 3 CodeForces
plat_name.append(["洛谷", "luogu", "lg"]) ## No. 4 洛谷
plat_name.append(["力扣", "leetcode", "lc"]) ## No. 5 力扣
plat_name.append(["pta", "ptaoj", "ptaonlinejudge"]) ## No. 6 PTA OJ
plat_name.append(["libre", "libreoj", "libreonlinejudge"]) ## No. 7 Libre OJ
plat_name.append(["usaco", "usacooj", "usacoj"]) ## No. 8 USACO
plat_name.append(["uoj", "universal", "universaloj"]) ## No. 9 Universal OJ
plat_name.append(["项目", "pro", "pros", "project", "projects"])
dict_name = ["UVaOJ", "AtCoder", "CodeForces", "洛谷", "力扣", "PTA", "LibreOJ", "USACO", "UniversalOJ", "项目"]
dict_plat = dict(enumerate(dict_name, start = 1))
oj_type = pd.api.types.CategoricalDtype(
    dict_name,
    ordered = True
)

def sort_df(df):
    #  Also can be implemented by a subline but more memory usage
    ## Also can be solved by .isin()
    ## The .copy() method enables df_enable to copy the origin data therefore modify the dtype
    df_enable = df[[True if elem in dict_name else False for elem in df["平台"]]].copy()
    df_enable["平台"] = df_enable["平台"].astype(oj_type)
    df_disable = df[[True if elem not in dict_name else False for elem in df["平台"]]]
    df_enable = df_enable.sort_values(by = ["平台", "难度", "题号"], ascending = [True, False, True])
    df_enable["平台"] = df_enable["平台"].astype(str)
    df_disable = df_disable.sort_values(by = ["难度", "题号"], ascending = [False, True])
    df = pd.concat([df_enable, df_disable], ignore_index = True)
    return df

def update(source, new_df):
    new_df = sort_df(new_df) ## Conduct first to avoid modify the old_file
    source.to_csv(r"./.MySolvedProblems.csv.bak", index = False)
    new_df.to_csv(r"./MySolvedProblems.csv", index = False)

def sign():
    print("\n每行一题")
    print("请依次输入平台, 题号, 标题, 难度。以空格隔开")
    print("其中, 平台可以以数字代称:")
    print(dict_plat)
    print("也可以输入其他平台")
    print("难度可以是任意正实数")
    print("完成题目的时间为: 20", day, sep = '')
    print("按平台分类, 平台相同时先按难度, 再按题号(字典序)排序")

def parse_plat(plat):
    if plat.isdigit() == True:
        return dict_plat[int(plat)]
    i = 0
    for alias in plat_name:
        i += 1
        if plat.lower() in alias:
            return dict_plat[i]
    return plat

def single(df):
    print("\n请输入平台: ", end = '')
    plat = parse_plat(input())
    print("请输入题号: ", end = '')
    name = input()
    print("请输入标题: ", end = '')
    title = input()
    print("请输入难度: ", end = '')
    level = float(input())
    print("完成题目的时间为: 20", day, sep = '')
    df_new = pd.concat([df, pd.DataFrame([[plat, name, title, level, day]], columns = df_col)], ignore_index = True)
    return df_new

def multi(df, n):
    sign()
    tmp = pd.DataFrame(columns = df_col)
    while n > 0:
        n -= 1
        sentence = input()
        plat, name, title, level = sentence.split(' ')
        plat = parse_plat(plat)
        level = float(level)
        tmp = pd.concat([tmp, pd.DataFrame([[plat, name, title, level, day]], columns = df_col)], ignore_index = True)
    df_new = pd.concat([df, tmp], ignore_index = True)
    return df_new

def file_input(df):
    sign()
    print("\n请注意文件不要有空行!")
    print("请输入想要导入的文件的绝对路径")
    while True:
        fpath = input()
        ifexist = os.path.isfile(fpath)
        if ifexist:
            break
        else:
            print("文件不存在, 请重试!")
    fin = open(file = fpath, mode = "r", encoding = "utf-8")
    tmp = pd.DataFrame(columns = df_col)
    for line in fin:
        plat, name, title, level = line.split(' ')
        plat = parse_plat(plat)
        level = float(level)
        tmp = pd.concat([tmp, pd.DataFrame([[plat, name, title, level, day]], columns = df_col)], ignore_index = True)
    df_new = pd.concat([df, tmp], ignore_index = True)
    fin.close()
    return df_new

def df_show(df):
    print("\n1. all          打印全部") # Accomplished
    print("2. a,b          打印[a, b)这个区间") # Accomplished
    print("3. OJ名         打印该OJ的所有题目") # Accomplished
    print("4. diff=a,b     打印该难度所有题目") # Accomplished
    opt = input()
    f_diff = False
    if (opt in ["all", "All", "ALL", "1", "1."]):
        opt = "all" # Do Nothing
    elif (opt.find(',') != -1):
        opt = opt.replace(' ', '')
        if (opt[0:4].lower() == "diff"):
            f_diff = True
            opt = opt[5:]
        if f_diff:
            a, b = [float(i) for i in opt.split(',')] ## Mode 4
            df = df[(df["难度"] >= a) & (df["难度"] <= b)]
        else:
            a, b = [int(i) for i in opt.split(',')] ## Mode 2
            df = df[a:b]
    else:
        opt = parse_plat(opt)
        df = df[df["平台"] == opt]
    print(df.to_string(index = True, justify = "left"))

def main():
    IFFILE1 = os.path.isfile(r"./MySolvedProblems.csv")
    IFFILE2 = os.path.isfile(r"./.MySolvedProblems.csv.bak")
    IFFIRST = IFFILE1 + IFFILE2
    if IFFIRST == 0:
        ept = pd.DataFrame(columns = df_col)
        ept.to_csv(r"./MySolvedProblems.csv", encoding = "utf-8", index = False)
    print("请输入你想选择的数据输入方式")
    print("0: 以文件形式输入") # Accomplished
    print("1: 仅输入1题") # Accomplished
    print("2及以上: 采用和文件式一样的多行输入n题") # Accomplished
    print("-1: 仅对csv排序") # Accomplished
    print("-2: 展示题目")
    if IFFIRST == 1 and IFFILE2:
        df_old = pd.read_csv(r"./.MySolvedProblems.csv.bak", encoding = "utf-8")
    else:
        df_old = pd.read_csv(r"./MySolvedProblems.csv", encoding = "utf-8")
    options = int(eval(input())) ## Options for input
    if options == 1:
        df_now = single(df_old)
    elif options >= 2:
        df_now = multi(df_old, options)
    elif options == 0:
        df_now = file_input(df_old)
    elif options == -1:
        options = -1 ## Do Nothing
    elif options == -2:
        df_show(df_old)
        return
    else:
        print("参数错误, 退出程序")
        return
    update(df_old, df_now)
    print("完成!")
        
main()
