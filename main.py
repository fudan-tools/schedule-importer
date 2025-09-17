import requests;
import re, json;
from datetime import datetime, timedelta;
import login;
def weeks_json(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d").date()
    end = datetime.strptime(end_str, "%Y-%m-%d").date()
    if start > end:
        return {}
    out, i, cur = {}, 1, start
    while cur <= end:
        week = []
        for k in range(7):
            d = cur + timedelta(days=k)
            if d > end:
                break
            week.append(d.isoformat())
        out[str(i)] = week
        i += 1
        cur += timedelta(days=7)
    return out
def to_ics(data, filename="schedule.ics"):
    ics_header = "BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n"
    ics_footer = "END:VCALENDAR"
    events = []

    for item in data:
        name, place, day, start, end = item

        # 自动补齐时间格式
        dt_start = datetime.strptime(f"{day} {start.zfill(5)}", "%Y-%m-%d %H:%M")
        dt_end = datetime.strptime(f"{day} {end.zfill(5)}", "%Y-%m-%d %H:%M")

        start_str = dt_start.strftime("%Y%m%dT%H%M%S")
        end_str = dt_end.strftime("%Y%m%dT%H%M%S")
        uid = f"{start_str}-{name}@fudan"

        event = (
            "BEGIN:VEVENT\n"
            f"UID:{uid}\n"
            f"SUMMARY:{name}\n"
            f"LOCATION:{place}\n"
            f"DTSTART;TZID=Asia/Shanghai:{start_str}\n"
            f"DTEND;TZID=Asia/Shanghai:{end_str}\n"
            "END:VEVENT\n"
        )
        events.append(event)

    ics_content = ics_header + "".join(events) + ics_footer
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ics_content)
token = login.get_session();
session = token["SESSION"];
pstsid = token["__pstsid__"]
cookies = {
    'SESSION': session,
    '__pstsid__': pstsid,
}

params = {
    'semesterId': '504',
    'hasExperiment': 'true',
}
requests.get(
    'https://fdjwgl.fudan.edu.cn/student/for-std/course-table/semester/504/print-data',
    params=params,
    cookies=cookies,
)
main_url = "https://fdjwgl.fudan.edu.cn/student/for-std/course-table";
res = requests.get(main_url,cookies=cookies);
m = re.search(r"var\s+semesters\s*=\s*JSON\.parse\(\s*'(?P<j>.*?)'\s*\)", res.text, re.S)
m = re.sub(r'\\"', '"', m.group(1))
data = json.loads(m)
sid = data[0]['id'];
start = data[0]['startDate'];
end = data[0]['endDate'];
start_on_sunday = data[0]['weekStartOnSunday'];
weekInfo = weeks_json("2025-09-07","2026-01-10")
if(start_on_sunday):
    for i in weekInfo:
        weekInfo[i] = weekInfo[i][1:]+weekInfo[i][:1];
response = requests.get(
    'https://fdjwgl.fudan.edu.cn/student/for-std/course-table/semester/504/print-data',
    params=params,
    cookies=cookies,
)
data = response.json();

courses = []
for i in data["studentTableVms"][0]["activities"]:
    start = i["startTime"]
    end = i["endTime"];
    day = int(i["weekday"])-1;
    name = i["courseName"];
    place = i["room"];
    weeks = i["weekIndexes"];
    for j in weeks:
        courses.append([name,place,weekInfo[str(j)][day],start,end]);
to_ics(courses);
