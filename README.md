# 复旦大学课表导入脚本
本脚本可根据学生学号与密码，自动抓取学生该学期课程表，并生成适用于各种日历软件的 ics 文件，方便保存到本地。
## 使用说明
1. 安装 Python 环境，建议使用 Python 3.7 及以上版本，可前往 [Python 官网](https://www.python.org) 下载。
2. 安装依赖库
```bash
  pip3 install requests
```
3. 打开 `userInfo.json`，修改里面的学号与密码。
4. 运行 `main.py` 脚本
```bash
  python3 main.py
```
5. 运行成功后，会在当前目录生成 `schedule.ics` 文件，可将该 ics 文件导入日历软件查看自己的课表。
## 注意事项
**勿干坏事**
