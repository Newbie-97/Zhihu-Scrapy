# Zhihu-Scrapy
---
##### 利用Scrapy框架爬取知乎网用户基本信息

在知乎网上随意找一用户，例如一用户url为：
[https://www.zhihu.com/people/chai-sheng-mang/following](知乎用户)
![用户界面](https://i.imgur.com/zRaihfX.png)

## 可以获得的信息：

1. 用户列表：
	
	1.1 请求的Request URL:
		![Request URL](https://i.imgur.com/Hfmv654.png) 
	1.2 URL中的相关参数（query）:
		![Query](https://i.imgur.com/BNzdoy7.png)
	1.3 被他关注的用户列表（一页的20个）：
		![被关注列表](https://i.imgur.com/BaMZXM7.png)
	1.4 用户列表中提供了url_token
		![url_token](https://i.imgur.com/SzKejWE.png)

2. 用户相关信息：
	
	![基本信息](https://i.imgur.com/LdG5RUo.png) 

## 请求的链接结构

	https://www.zhihu.com/api/v4/members/***url_token*** ?include=**Query**
	

