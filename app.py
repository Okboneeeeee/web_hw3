from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import uuid

app = Flask(__name__)


TASK_FILE = "task.xlsx"

# 初始化 task.xlsx
if not os.path.exists(TASK_FILE):
    df = pd.DataFrame(columns=["Date", "Task", "Location", "Priority", "Subtask 1", "Subtask 2", "Subtask 3", "ID"])
    df.to_excel(TASK_FILE, index=False)
else:
    df = pd.read_excel(TASK_FILE)
    if "ID" not in df.columns:
        df["ID"] = [str(uuid.uuid4()) for _ in range(len(df))]
        df.to_excel(TASK_FILE, index=False)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/task", methods=["GET", "POST"])
def task():
    if request.method == "POST":
        date = request.form["date"]
        task = request.form["task"]
        location = request.form["location"]
        priority = request.form["priorty"]
        detail_1 = str(request.form["detail_1"])
        detail_2 = str(request.form["detail_2"])
        detail_3 = str(request.form["detail_3"])

        # 生成唯一 ID
        unique_id = str(uuid.uuid4())

        # 新增事件到 DataFrame
        new_event = pd.DataFrame([{
            "ID": unique_id,  # 新增 ID
            "Date": date,
            "Task": task,
            "Location": location,
            "Priority": priority,
            "Subtask 1": str(detail_1),
            "Subtask 2": str(detail_2),
            "Subtask 3": str(detail_3),
        }])

        


        # 使用 pd.concat 更新excel
        df = pd.read_excel(TASK_FILE)
        updated_df = pd.concat([df, new_event], ignore_index=True)
        updated_df.to_excel(TASK_FILE, index=False)

      

        # 跳轉到第三頁，傳遞所S選日期
        return redirect(url_for("tasks_on_date", date=date))
    return render_template("task.html")





@app.route("/tasks_on_date")
def tasks_on_date():
    selected_date = request.args.get("date", "")  # 獲取 URL 中的日期參數
    
    
    tasks_for_date = []
    if selected_date:
        df = pd.read_excel(TASK_FILE)  # 讀取最新的任務文件
        
        # 確保日期欄位格式一致
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        
        tasks_for_date = df[df["Date"] == selected_date][["ID", "Task"]].to_dict(orient="records")

    return render_template("tasks_on_date.html", tasks=tasks_for_date, selected_date=selected_date)
    



    


@app.route("/task_details")
def task_details():
    task_id = request.args.get('task_id', '')
    
    try:
        # 讀取任務文件
        tasks = pd.read_excel("task.xlsx")
        
        task = tasks[tasks['ID'] == task_id] 

        if task.empty:
            return f"Task '{task_id}' not found", 404

        task_name = task["Task"].iloc[0]
        subtasks = [
            task["Subtask 1"].iloc[0],
            task["Subtask 2"].iloc[0],
            task["Subtask 3"].iloc[0],
        ]
        selected_date = task['Date'].iloc[0]  # 假設這是日期字段
        
        # 顯示生成的 URL 以供檢查
        return_url = url_for('tasks_on_date', date=selected_date)
        print(f"Generated URL: {return_url}")  # 這會在後端控制台輸出 URL
        
    except Exception as e:
        return f"An error occurred while processing the task details: {e}", 500

    # 渲染模板
    return render_template(
        'task_details.html',
        task_name=task_name,
        subtask_1=subtasks[0],
        subtask_2=subtasks[1],
        subtask_3=subtasks[2],
        selected_date=selected_date  # 確保日期參數傳遞到模板
    )







if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
