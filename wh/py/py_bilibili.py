#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
from requests import session, utils
import os
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "B站视频"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
		
			"演唱会":"演唱会4K",
      "MV":"MV4K",
      "窗白噪音":"窗白噪音4K",
      "风景":"风景4K",
      "说案":"说案",
      "戏曲":"戏曲4K",
      "演讲":"演讲4K",
      "解说":"解说",
      "相声小品":"相声小品",
      "河卫国风":"河南卫视国风4K",
      "儿童":"儿童",
      "苏教版":"苏教版课程",
      "人教版":"人教版课程",
      "沪教版":"沪教版课程",
      "北师大版":"北师大版课程",
      "球星":"球星",
      "动物世界":"动物世界4K"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	cookies = ''
	def getCookie(self):
		cookies_str ="buvid3=418CAE55-A89A-0098-4B2B-C7F6E828462038635infoc; rpdid=|(u)~kmY)kml0J'uYkukRYRRJ; video_page_version=v_old_home_6; buvid_fp=418CAE55-A89A-0098-4B2B-C7F6E828462038635infoc; buvid_fp_plain=6463AA03-B557-A6CF-6E13-6309086EB29041849infoc; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; CURRENT_QUALITY=80; blackside_state=0; nostalgia_conf=-1; fingerprint=63b8c1cbf6ab858bf9a04a9ff112f9bb; SESSDATA=2472ade8,1677739051,a03fc*91; bili_jct=b0d218df4c5be5b7f26d3b0ae390e826; DedeUserID=667298592; DedeUserID__ckMd5=aa18ade6353974c9; sid=5o3z9v5c; bp_video_offset_667298592=undefined; b_ut=5; CURRENT_FNVAL=16; innersign=0" #填入大会员Cookies
		cookies_dic = dict([co.strip().split('=') for co in cookies_str.split(';')])
		rsp = session()
		cookies_jar = utils.cookiejar_from_dict(cookies_dic)
		rsp.cookies = cookies_jar
		self.cookies = rsp.cookies
		return rsp.cookies
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(tid,pg)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:			
			rspRetry = self.fetch(url,cookies=self.getCookie())
			content = rspRetry.text		
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id":aid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def cleanSpace(self,str):
		return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
	def detailContent(self,array):
		aid = array[0]
		url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

		rsp = self.fetch(url,headers=self.header)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
		pic = jo['pic']
		desc = jo['desc']
		timeStamp = jo['pubdate']
		timeArray = time.localtime(timeStamp)
		year = str(time.strftime("%Y-%m-%d %H:%M", timeArray)).replace(" ","/")
		dire = jo['owner']['name']
		typeName = jo['tname']
		remark = str(jo['duration']).strip()
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":year,
			"vod_area":"",
			"vod_remarks":remark,
			"vod_actor":"",
			"vod_director":dire,
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站视频'
		vod['vod_play_url'] = playUrl

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}'.format(key)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:
			rspRetry = self.fetch(url, cookies=self.getCookie())
			content = rspRetry.text
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id": aid,
				"vod_name": title,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result = {
			'list': videos
		}
		return result


	def playerContent(self,flag,id,vipFlags):
		result = {}

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid={1}&qn=116'.format(ids[0],ids[1])
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		ja = jo['durl']
		
		maxSize = -1
		position = -1
		for i in range(len(ja)):
			tmpJo = ja[i]
			if maxSize < int(tmpJo['size']):
				maxSize = int(tmpJo['size'])
				position = i

		url = ''
		if len(ja) > 0:
			if position == -1:
				position = 0
			url = ja[position]['url']

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"Referer":"https://www.bilibili.com",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {
		"相声小品": [
      {
        "key": "tid",
        "name": "分类",
        "value": [
          {
            "n": "全部",
            "v": "相声小品"
          },
          {
            "n": "单口相声",
            "v": "单口相声"
          },
          {
            "n": "群口相声",
            "v": "群口相声"
          },
          {
            "n": "德云社",
            "v": "德云社"
          },
          {
            "n": "青曲社",
            "v": "青曲社"
          },
          {
            "n": "郭德纲",
            "v": "郭德纲"
          },
          {
            "n": "岳云鹏",
            "v": "岳云鹏"
          },
          {
            "n": "曹云金",
            "v": "曹云金"
          },
          {
            "n": "评书",
            "v": "评书"
          },
          {
            "n": "小曲",
            "v": "小曲"
          },
          {
            "n": "二人转",
            "v": "二人转"
          },
          {
            "n": "春晚小品",
            "v": "春晚小品"
          },
          {
            "n": "赵本山",
            "v": "赵本山"
          },
          {
            "n": "陈佩斯",
            "v": "陈佩斯"
          },
          {
            "n": "冯巩",
            "v": "冯巩"
          },
          {
            "n": "宋小宝",
            "v": "宋小宝"
          },
          {
            "n": "赵丽蓉",
            "v": "赵丽蓉"
          },
          {
            "n": "郭达",
            "v": "郭达"
          },
          {
            "n": "潘长江",
            "v": "潘长江"
          },
          {
            "n": "郭冬临",
            "v": "郭冬临"
          },
          {
            "n": "严顺开",
            "v": "严顺开"
          },
          {
            "n": "文松",
            "v": "文松"
          },
          {
            "n": "开心麻花",
            "v": "开心麻花"
          },
          {
            "n": "屌丝男士",
            "v": "屌丝男士"
          },
          {
            "n": "喜剧综艺",
            "v": "喜剧综艺"
          }
        ]
      },
      {
        "key": "duration",
        "name": "时长",
        "value": [
          {
            "n": "全部",
            "v": "0"
          },
          {
            "n": "60分钟以上",
            "v": "4"
          },
          {
            "n": "30~60分钟",
            "v": "3"
          },
          {
            "n": "10~30分钟",
            "v": "2"
          },
          {
            "n": "10分钟以下",
            "v": "1"
          }
        ]
      }
    ]}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]