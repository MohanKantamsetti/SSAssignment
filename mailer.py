import smtplib,ssl,json
from config import smtp_mail,smtp_pass
smtp_server='smtp.gmail.com'
smtp_port=587
fro=smtp_mail

def send_smtpmail(to,message):
	try:
		context=ssl.create_default_context()
		with smtplib.SMTP(smtp_server,smtp_port) as server:
			server.starttls(context=context)
			server.login(smtp_mail,smtp_pass)
			server.sendmail(smtp_mail,to,message)
			server.quit()
	except Exception as e:
		raise Exception(str(e))