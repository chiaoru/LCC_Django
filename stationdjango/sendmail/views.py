from django.shortcuts import render

# Create your views here.

from smtplib import SMTP,SMTPAuthenticationError,SMTPException

from email.mime.text import MIMEText

def sendmail(request):
    smtp = "smtp.gmail.com:587" # Gmail主機位置
    account = "wu0g20@gmail.com" # 請輸入 Gmail 帳號
    password = "laivdvpaiotxljwg" # 雙驗證後系統自動產生的密碼  xezmYk-hyrhot-zojky3


    content = "非常感謝您的訂購，我們將盡快安排出貨！";
    msg = MIMEText(content) # 郵件內容
    
    msg['Subject'] = "聯成快樂購物網-訂單成立" # 郵件主旨
    
    mailto = "wu0g20@gmail.com" # 寄給單獨的收件者
    # mailto = ['wu0g20@gmail.com','chiaoru.wang@gmail.com'] 寄個多個收件者
    
    server = SMTP(smtp) # 建立 SMTP 連線
    server.ehlo() # 與 SMTP 主機溝通
    server.starttls() # 要使用 TTLS 安全認證
    
    try:
        server.login(account,password) # 登入，身份確認
        server.sendmail(account,mailto,msg.as_string()) # 寄信
        sendMsg = "郵件已寄出"
        
    except SMTPAuthenticationError:
        sendMsg = "帳密認證錯誤"
    except:
        sendMsg = "郵件發生錯誤"
    
    server.quit() # 關閉 Server 連線
    
    return render(request, 'sendMail.html', locals())