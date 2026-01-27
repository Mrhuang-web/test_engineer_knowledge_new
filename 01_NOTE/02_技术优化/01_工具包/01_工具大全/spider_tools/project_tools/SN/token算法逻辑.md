# Token生成具体流程
## 核心公式
`token = Base16(HMAC-SHA-256(appkey, SignBytes))`
其中，`SignBytes = Content-MD5-Str`

## 关键参数说明
| 名称 | 详细说明 |
|------|----------|
| appkey | 动环平台生成的密钥（不重复随机数），外部平台需保密存储，交互时不明文传递 |
| Content-MD5-Str | 消息体所有内容的MD5值；若为GET请求（无消息体），可不参与TOKEN计算 |
| token | 最终生成的鉴权加密字符串，用于接口请求头Authorization字段 |

## 分步生成流程
1. **计算请求报文MD5散列值**
    - 对请求报文源文进行MD5散列运算
    - 得到结果为带不可见字符的byte[]数组
2. **HMAC-SHA-256加密**
    - 以appkey作为密钥
    - 对第一步得到的MD5散列值（byte[]数组）进行单向加密
    - 得到结果为带不可见字符的byte[]数组
3. **Base16编码转换**
    - 对第二步的加密结果（byte[]数组）进行Base16编码
    - 转换为可见字符，最终得到token值

## 应用场景
生成的token需填入HTTP(S)请求头的Authorization字段，格式如下：
`Authorization: appid="分配的appid",token="生成的token值"`