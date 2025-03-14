# -在main.py运行，操控台输入爬取的贴吧名称，爬取的页数以及帖子个数。
期间产生title_url.csv保存爬取对应页数的所有帖子的标题和链接。(title_url.csv格式如下)<br>
|title|url|
|--------|------|
|xxxx|www.xxxx.com|
|xxxx|www.xxxx.com|
>>
同时产生all_contents.csv保存爬取帖子的发言人和发言`文字`。(all_contents.csv格式如下)
|0|1|2|3|4|5|6|7|
|--------|------|------|------|------|------|------|------|
|title1|user_name1|content1|user_name2|content2|
|title2|user_name3|content3|user_name1|content1|user_name4|content4|
|title4|user_name4|content4|
