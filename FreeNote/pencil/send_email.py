# -*- coding: utf-8 -*-

from django.template import loader
from django.core.mail import EmailMessage
from django.conf import settings
import threading

# 继承 Thread 对象， 定义 run 方法
class SendEmail(threading.Thread):
	def __init__(self, subject, html_content, send_from, to_list, fail_silenty=True):
		threading.Thread.__init__(self)
		self.subject = subject
		self.html_content = html_content
		self.send_from  = send_from
		self.to_list = to_list
		self.fail_silenty = fail_silenty # 默认发送异常不报错

	def run(self):
		message = EmailMessage(self.subject, self.html_content, self.send_from, self.to_list)
		message.content_subtype = "html"
		message.send(self.fail_silenty)


def send_html_email(subject, html_content, to_list):
	"""发送 html 邮件"""
	send_from = settings.DEFAULT_FROM_EMAIL
	send_email = SendEmail(subject, html_content, send_from, to_list)
	send_email.start()
