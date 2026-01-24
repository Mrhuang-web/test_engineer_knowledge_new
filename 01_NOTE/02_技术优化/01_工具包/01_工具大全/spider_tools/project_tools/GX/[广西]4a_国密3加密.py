from gmssl import sm3
# body='wcc13S8@r*6p'
body='wcc13S8@rsffref#@aa*6p'
body2='wcc13P4sOKkh20@r*6p'
msg_list = [i for i in bytes(body.encode('utf-8'))]
digest = sm3.sm3_hash(msg_list)
print(digest)


msg_list = [i for i in bytes(body2.encode('utf-8'))]
digest = sm3.sm3_hash(msg_list)
print(digest)