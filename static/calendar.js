// 初始化變數
const calendarTable = document.getElementById("calendar-table");
const monthYearDisplay = document.getElementById("month-year");

let currentDate = new Date();
let currentMonth = currentDate.getMonth();
let currentYear = currentDate.getFullYear();

// 生成日曆
function generateCalendar(month, year) {
    // 清空日曆
    while (calendarTable.rows.length > 1) {
        calendarTable.deleteRow(1);
    }

    // 設置顯示的月份與年份
    monthYearDisplay.textContent = `${year}年 ${month + 1}月`;

    // 計算當月的第一天和總天數
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    let row = calendarTable.insertRow();
    let cellCount = 0;

    // 在第一行填充前幾天的空格
    for (let i = 0; i < firstDay; i++) {
        row.insertCell();
        cellCount++;
    }

    // 填充當月日期
    for (let day = 1; day <= daysInMonth; day++) {
        const cell = row.insertCell();
        cell.textContent = day;
        cell.classList.add("calendar-cell");

        // 點擊事件：選擇日期
        cell.onclick = () => {
            const selectedDate = new Date(year, month, day).toISOString().split("T")[0];
            const dateInput = document.getElementById("date");
            if (dateInput) {
                dateInput.value = selectedDate; // 將日期填入表單
            }
        };

        cellCount++;
        if (cellCount % 7 === 0 && day < daysInMonth) {
            row = calendarTable.insertRow();
        }
    }
}

// 更改月份
function changeMonth(offset) {
    currentMonth += offset;

    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    } else if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }

    generateCalendar(currentMonth, currentYear);
}

// 初始化日曆
generateCalendar(currentMonth, currentYear);
