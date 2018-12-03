import dao
import hashlib
import uuid
import logging
import sendEmailService
import const
import re
import text1203 as err_text
 
def registerUser(username, email, password, db_file_name):    
    validation_result = validateInput(username, email, password)
    if len(validation_rs) >= 1:
        for rs in validation_result:            
            logging.info(rs)
        return False
 
    auth = password2AuthKey(password)
    if auth == None:
        logging.info("Auth_key is None")
        return False
 
    confirm_token = getEmailConfirmToken()
    if dao.insertProvisionalUser2Db(username, email, auth, confirm_token, db_file_name) != True:
        logging.info("InsertProvisionalUser2Db was failed")
        return False
 
    if not sendEmail4SignUp(username, email, confirm_token):
        logging.info("Failed to send Email")
        return False

    logging.info("signUpUserProvisionally is success.")
    return True
 

def sendEmail4SignUp(username, email, email_confirm_pass):
    if not sendEmailService.sendEmailMock(email, const.EMAIL_SUBJECT_SIGNUP_CONFIRM, const.EMAIL_BODY_SIGNUP_CONFIRM.format(username, confirm_token)):
        return False
    return True
 

def validateInput(username, email, password):
    errs = []
    pattern = "[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]"
    if (username is None) or (username == ""):
        errs.append(err_text.errText['empty_username'])        
    if (email is None) or (email == ""):
        errs.append(err_text.errText['empty_email'])    
    if (password is None) or (password == ""):
        errs.append(err_text.errText['empty_password'])
    if len(password) < 8:
        errs.append(err_text.errText['too_short_password'])
    if not re.match(pattern, email):
        errs.append(err_text.errText['invalid_password'])
    return errs
 

def password2AuthKey(password):
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