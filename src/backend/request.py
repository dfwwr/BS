import requests
from bs4 import BeautifulSoup

def login(user,password):
	# 创建会话对象
	session = requests.Session()
	# 登录信息
	login_url = 'https://login.taobao.com/member/login.jhtml'
	data = {
		'fm': 'login',
		'loginId': user,  # 替换成你的用户名
		'password': password     # 替换成你的密码
	}

	# 发起登录请求
	response = session.post(login_url, data=data)
	return response

def request(good):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
	}

	# 指定要爬取的商品URL
	url = 'https://s.taobao.com/search?q='+good
	print(url)
	# 发起请求
	response = requests.get(url, headers=headers)
	print(response.status_code)
	# 检查请求是否成功
	if response.status_code == 200:
		# 解析HTML内容
		soup = BeautifulSoup(response.text, 'html.parser')
		print(soup)
		# 找到商品列表
		items = soup.find_all('div', class_='item')  # 根据实际结构调整类名

		# 提取商品信息
		for item in items:
			title = item.find('a', class_='title').text.strip()  # 根据实际结构调整类名
			price = item.find('strong', class_='price').text.strip()  # 根据实际结构调整类名
			print(f'商品标题: {title}, 商品价格: {price}')
	else:
		print('请求失败，状态码:', response.status_code)
if __name__ == "__main__":
	user='13735460323'
	password='zyh20031221'
	re=login(user,password)
	if re.ok:
		request('华为手机')
