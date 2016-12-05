# 文章预处理
数据抓取完成后，运行output目录下的`extract.py`,会自动在每个wechatid文件夹目录下新建`all_article.txt`,包含该公众号所有文章及编号，每篇一行。

# 使用
0. copy到`WechatSougou`项目根目录下
1. 把`wcids.txt`需要爬的id保留，其它删除。
2. `getinfo.py`中变量`cnt`记录当前抓取的wechat_id序号。
每次程序由于connection error/Vcode error/etc 退出，根据当前完成的wechat_id修改第`35`行的判断，避免重复爬同一个号。
3. 使用HMA Pro VPN, 定时切换ip（经常连接不稳定，貌似沙田的ip比较好用）

# todos
~~1. 解析html，提取文章内容
2. 把同一个公众号的所有文章合并到一个文件里面~~
