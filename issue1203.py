import dao
import hashlib
import uuid
import logging
import sendEmailService
import const
 
def signUpUserProvisionally(username, email, password, db_file_name):
    
    # validation check
    if len(validationCheck4InsertProvisionalUser(username, email, password)) >= 1:
        return False
 
    # password to hash
    auth_key = covert2AuthKeyFromPassword(password)
    if auth_key == None:
        print("Auth_key is None")
        return False
 
    # insert user provisionally to user db
    email_confirm_pass = getEmailConfirmPass()
    if dao.insertProvisionalUser2Db(username, email, auth_key, email_confirm_pass, db_file_name) != True:
        print("InsertProvisionalUser2Db was failed")
        return False
 
    # send email for sign up user
    sendEmail4SignUpUser(username, email, email_confirm_pass)
 
    logging.info("signUpUserProvisionally is success.")
    return True
 
# send email for sign up User
def sendEmail4SignUpUser(username, email, email_confirm_pass):
    # sendEmailService.sendEmail(email, const.EMAIL_SUBJECT_SIGNUP_CONFIRM, const.EMAIL_BODY_SIGNUP_CONFIRM.format(email_confirm_pass))
    sendEmailService.sendEmailMock(email, const.EMAIL_SUBJECT_SIGNUP_CONFIRM, const.EMAIL_BODY_SIGNUP_CONFIRM.format(username, email_confirm_pass))
    return True
 
 
def validationCheck4InsertProvisionalUser(username, email, password):
    error = []
    if (username == None) or (username == ""):
        error.append("ユーザー名を入力してください。")        
    
    if (email == None) or (email == ""):
        error.append("メールアドレスを入力してください。")
    
    if (password == None) or (password == ""):
        error.append("パスワードを入力してください。")
 
    if len(password) <= 8:
        error.append("パスワードが短すぎます。パスワードは8文字以上に設定してください。")
        
    if ("@" not in email) or ("." not in email):
        error.append("メールアドレスが正しく入力されているか確認してください。")
 
    return error
 
 
def covert2AuthKeyFromPassword(password):
    if password == None:
        return False
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
 
def getEmailConfirmPass():
    return str(uuid.uuid4()).replace("-","")


'''
reviewed by okada_taku

validationかけてerrorのオブジェクト作ったのに，len()だけでログ吐かないのはもったいないかも．
あとprintするときの文言はハードコーディングじゃなくて別でtextIdみたいなんがあると多言語対応しやすい
 
convert2AuthKeyFromPasswordって
password2AuthKeyじゃね？
 
2使うならざっくり関数名でもいいイメージ
 
私この言語の仕様はよくわかってないんやけど，FalseはNONEと等価なん？
conversion2AuthKeyFromPasswordでFalse返した時にNONEに入ってくれるのか分からぬ
 
sendEmail4SignUpUserがTrueしか返してないけど，メール送信の成否で処理変えるのでは？
 
これはライブラリを使う予定かもやけど，メールアドレスのバリデーションが雑い．
あとパスワードが8文字丁度のときバグってる
 
validationCheckとconvert2*の中で2回passwordのナルチェックしてる．
メインの関数だけ公開して，残りを隠蔽する場合はナルチェックはエンドポイントでだけ行って，サブの関数ではやらんでもいいんでない？
 
ざっくり見た感じやとそれくらい
'''