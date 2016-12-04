# usage
1. `getinfo.py`中变量`cnt`记录当前抓取的wechat_id序号。
每次程序由于connection error/Vcode error/etc 退出，根据当前完成的wechat_id修改第`35`行的判断，避免重复爬同一个号。
2. 使用HMA Pro VPN, 定时切换ip（经常连接不稳定，貌似沙田的ip比较好用）

# todos
1. 解析html，提取文章内容
2. 把同一个公众号的所有文章合并到一个文件里面
