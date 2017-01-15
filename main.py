import binascii
import ipfsapi
from secretsharing import BitcoinToB58SecretSharer
from flask import Flask, render_template, request, Response
from Crypto.PublicKey import RSA

api = ipfsapi.connect('127.0.0.1', 5001)
app = Flask(__name__)

PRIVATES = [
    '0\x82\x02]\x02\x01\x00\x02\x81\x81\x00\x9d\xec\x13\xd8G\x84a]\x9d0\x01K\xc7\n\x1b\xfc.\xc6\xd8\x83\xcd\xc0\xe9\xc8\t\xeaK7\x01$\xc3\xc2\xd6\xd4\xde\x01\xb0k\xd2Apbh&\x1fXO\x8eU\xf6\xa4\xf7|\xa5\x8a#\xa4G\x82\x06\x1f\xa8\x02J)\xfba\x97U\x17\xec\\>\xa0\xe8\xc71\x1bYh\xb7\xbf%\xd9\x9b\xbc\x06\xac\x94\xc7\x8aw(\xd1Z\xc8\xa2\xe3%~\xd7\xb1?\x82\xdb\xe4\x9f\xb9Nt\x10"\xa9>U,\xca\xb5\xb4H\x88\xadD\x93\xa9\xcc\xacY\x02\x03\x01\x00\x01\x02\x81\x81\x00\x91\xf0\xfa\xc1\xf4\r\xb5\xc1B\xa3{\x7f!\x19\t\x95\xbbP\xce\x04\xb8_\xe0l\x9a%(\x8fS\x82;[S\x17\xf3v\xd2(BmqC\xb0\x06\x13\x0f\x94\xad\xf0ix8\xb2\xbbt\xf6\xcd9\xbcB\x96|\xb8g\x86!\xb9\xcb\xde\xa7\xff07I\x82#\xf3\xf0\x12\xad~\xd7\x06\xea.\xab\x94B\xe6\x1a6\xb8\xce\x8bc\x81\xed\xa5\xf6 \x1b1y\x12\xc6\xfa\xb8\x9e\xb1\xb4\x8b\xe3\xa5\x8c^\xa4\xe5\x0c\x8f\xf7#\x03N.\x84n\x86u\x02A\x00\xb6\xbcE\xe8!\x12MU\x1a-c\\\xa1\x9b\x1f\x8a\x9d\xb9M\xc0\x10\xabH\xb9\xb2\xea\xd2\xe3z\rZ^\x8a<\xc8&\x8aR\x99\xdfX\x1b=\x89n_\xed\xacp\xa0\x1f\xf3s&S=1\xa9\'\xc7!>j\xfb\x02A\x00\xdd=\x00\xe3E\xa3\xdc\xea\xafd\xc6\xab*\xf6\xfe|w\xa5IeO\xbf!G-U\x14\xfe\xa5\x85I\x94\x82\n\xfe\x99x}^\xf7\xff4i\xe5"p|\x1f\x08#\xd9\x0c3N\xfd\xbf\x82\x93\x85L\xea\xe6\xe5\xbb\x02@[\xbbI\x90\x8c\xc1\x86F\x99\\}\x8b\xab\xa8\x96}\xdcM\x80eQ8\xda\xca5\xb1\xc1\xe9\xe5\x84<\x80F\xfe\xda.\xd6\xb3>\x81*\xd6\x89\xde\xaa\xa4\xc7H\x10E\xa1\xa4q\x82\xa4\xb8\x8clq\x06z~\xbd\xef\x02A\x00\xdc\x84\xed\xd9\x9b\x94\x95\xa3\'h_\xceEi$\x88\x94\t\xa0z\xe7^/\xa1n\xc2\x1b\xc7&\xdd\x10V\x82\xb8\xca\xc5\xd6\x9f\xc0\x85\x99Oy-\xf7\x81\xffv>\xfa\xdca\x98\xd2\xe7\x82xx\xea\xa9\x9c\x8a\xc1\xf9\x02@S\x19\xf7d\x88\x87\x82\xcd\x9f^\x08[\x9c\xb1\xa5e:\xd8\x06r\xee5\x14\x0c|^\x9dJ\xfb\x10\xdd\xc8\x95\xb1p\xef\x8d\xba\xaa\xb0\xcb\xf3\x11\xe6\xf0W\xd1\xf8\xe7\x9d\xd7CI\xd5LO\xd1w\x9f{t\xb1e\x9b',
    '0\x82\x02[\x02\x01\x00\x02\x81\x81\x00\xdf\x00\x1e\x89\xbf[\x0f\x0f\xd4\x8d\xf8b\xff@\xec\x9bEB\x00]\xfd\x1eMR\xf3\xd6\t\xd5\r\xabQ\xae|\xfeq\xa3\xcb\x9cu\x90<\xf5l\xa7e\x88!\xf1\xd8\xea_\x18(\x95\xc5\xd5I\xdf\x9c=\xafP\x8a\x9eK\xf5\x9c\x0f\xd9sH\xfeL\\\xa7\xa5N\xd9\xe6oW\xfb\x91\x81\x1b\xa4;W\x99\xcc\xec\t+\xc1\x178\xc8\xednl\xe1`k\xc0H1\xa2\x92\x81\x87\xc1\x12\x17L\xa7f\xa8\xca\x80\xd4\x9f\xb9,\xdePc\xd4\x8b\x02\x03\x01\x00\x01\x02\x81\x80UN\x08`\x8d0\xda,&\x15A\x05-\xbb\xbaG\x13QR.\xa2\x1b+]&%\xa4\x919\xafe\x89\xa8\n\xf5\x91\xc0\xdb\xd3% \x0c\x8aI\xe6\xcf\x12\x9d\x1fkX\x817UC\xdeyi\xee\xac\xb2\x19\xcfLS\xcct\x0b\xf50\xe3Y\xe2\x02,\xd7\xee\x92\xd6\x8f\x95_\xe2\xa3Mp\xf8\x9a\xf8\x16\xdb\xdc\x10>;\xc6\xe4F:\xa4\xbdgNi\xebE\xda\x99\xb0f\x0e8?\x03\x82\xf9\xb2,\xd3P\xccK\xac\xf3\x0c@\xea\x01\x02A\x00\xe9^V\xc8\xc9\x86e\xa9\x04\xc7.\xb5o7^\x94\xf31\xf3>\xf7Z\xe3e\x01;S\xe8!c\xcb\xed\x93\x0f\xd4\xeeG+C\xf7;!\xd3\xa03(KO\xcf\xb8r(\xc1\x89B_g\xdexQK.\x8b\x81\x02A\x00\xf4\xa0az04\x86\x95\xd2\x7f\xd0\xc6B\x00\xf4F\x05\xc9:\xe3\xa5\x02;\x17?r\x00,\x84^\x07uG\xe8oJ\x86\x11\xfd;l\x07\xb8\xe5\x00-1q\x06i\x86?-\xa0f)\xe7\x1e;\x16\xc7\xc6\xd6\x0b\x02@"MD\x92T\xd4\xd5b\x87\x9aCjU\xc3\x9c\xbaf\x18\xc4yO\xe0c&8\x8d \xe30\xed;O[[k_\xee\xc4\x14De\xc3\xae\x18\x91\x0cn-x\t\xd3u\xdc$\xb1\xc5\xd6=\xa4\x0f\xc6\xee;\x81\x02@"\x86\xe8{8\x86\x91``\x1f\x8e6\rf\xd9\x13q\t\x9f\xf85x\x05#\x18\xdf\\J\xec;\xe1M\x9ab\xa2"\xa0\x9d\xb5bG\xb3\'S\x9b\x1c\xc5\xd7\xb0\x12\x00\xd2\xb5\xfb\xe7\xaf\x8eac\xf1\xa9,\xd5U\x02@S\xa3\xf6\xee\xcf-\x05\x83\xca\x1f\x90\xb7k\x9f|MW\xd3\xc0`j\x8aR\xfc\x9e\x17\xeb\xddW9\xd5I\xba\xc5\x91q#\x92D\xd4\x92\xbe\xf0f\xffqlr\xb9\x05\xf0\xf3d\x86\xb4(j\x89H\xe7dvVf',
    "0\x82\x02[\x02\x01\x00\x02\x81\x81\x00\xb6U\x8d\x05\n\xec$\x02\xe8}\xc7\xf0:\x8b\xea(\x19\x1c\xfd/\xa0\xe4\xbe\xc7\xa7\xdf\x98\x0cf\xf3\x8eB\xbf\xfc\x84\xf9\x8e\xf1~\xc1\x92\xc6\xed[\x9cQ\x7f\x86u\xa1#\x15\x90\xcc\x9a\xe0=X\xf3\xbc\x91\xb4\xc9e\x1c\xae\xd7\xf5\x0f\xdd\x16b6\xf5Xbvbn\xe1g\xea\xdf\x9c\xe7\xef\x8d\xa7\x92|\xb8\x1f\xe4\x17\xc7#\xf0\x9e()Z\xbf\xbb\xd3\xdc\x8d\x87d\xbf+cs\xe6\xa1i\xb9\xdc\x7f\xed=\x0c=\x8e\x1b^\x89\x89\x7f\x02\x03\x01\x00\x01\x02\x81\x80f\xddZ\xe2\x86g\xf4e\x03\x9e\xbaf\x87\xd1\x19x'\xba\xd8\x07\xbf\xc0l\xf5\x1c{#?\x93\xf1A\xc7\xdc\xa1\xec\xaf\x11\xfa\xa2%8\xd6+`l\x8e\xf9\xdf\xf4\x8a\xc4\xcdL\xd4qg\xa2\x94\x85eS\xdaggA\xfb>*\x05\xc6\x98\xd2\x83f\xbb]\xac\x19\x8f\xa2\xe73%K\xa3\x15)Od\x88r\x13{\xee\x8bN\xa3\x88\xb3\xd9x~\x1e\xe4\xee^z{\xa8\x999S-\x10\x8eSa#\xa0-DJ8\x1cHV\xfc)\x02A\x00\xb8\x95f\x86g\x10\x01V\x19m\x84\xaelS\x8a\x9eX1\xa5u5\xf1Ek^X\xdc%\xdf\xb1\x81U\x05]\x9bC\x96,W^\x01\xe5)2\xda\xb0:\xfa\xec\t\x1d\xccA!^\x93\xf0k(z\xa7\x15\xc83\x02A\x00\xfc\xe1Y\xda\xb3\x92\r\x1c\x97\xc5\x870\xca\xcc\x95%;\xed\x03\xda\x13/\xbc\xc4\xc9z7\xbfW\xe8\xc9\xb3\xa5\x82\xf4\x9e\x0f\x94<\x06%\xdb)\xc9Q\xb6\xe7\xd3\xdd\xfel'\x1bvz6\xff\x96\xe7HY\x8a]\x85\x02@\x0b\x9bQd\x18,\xf8x\x8a\x86\xc9v\x12W\xbaz\xb4\x7f\x02\xb1y\x1f\xdf\xc6\x9d\x9b&\xd4\xb6\xd99\x91\xb8\x11\xa7\xc6\xbb5\xb4\x94\xb3\xb7\xce<ee\xf9\x7fw\xc2&\xfe\x86\x05\xec%\x8fS\x9d\xab\x00\xc0\xac\xe3\x02@y\tC\x80\xb2BM\x94I\xf0yl\x99$\xa2\x9eW\xb8r\x07\x86\xf7jZ\xa64\xa1J,Aw\x89L\xc7\t^>\x06\xadT#\xfaj]\xb9\x86\xda\x1fF9\xe8z/b\xdd\xccE9m)\xeb\xf1\x96!\x02@5\x9c>H\x83\x15\x7f\x90\xb4\xc1 \x7f\xd1\x04~\xf2p\x88\xba\x8eU\xab\xb8o$\x10\xba\x00\xb4\xed\x10\xf6\xa1\xa0\xde_j\xd9$_\xc8\xb0\xe3\x9eI-H\x7f[\xb0\x95Y\xa5\xabL\x03\xd0\xc8\xe4C\x19\xd0J\x12"
]

PUBLICS = [
    '30819f300d06092a864886f70d010101050003818d00308189028181009dec13d84784615d9d30014bc70a1bfc2ec6d883cdc0e9c809ea4b370124c3c2d6d4de01b06bd241706268261f584f8e55f6a4f77ca58a23a44782061fa8024a29fb61975517ec5c3ea0e8c7311b5968b7bf25d99bbc06ac94c78a7728d15ac8a2e3257ed7b13f82dbe49fb94e741022a93e552ccab5b44888ad4493a9ccac590203010001',
    '30819f300d06092a864886f70d010101050003818d0030818902818100df001e89bf5b0f0fd48df862ff40ec9b4542005dfd1e4d52f3d609d50dab51ae7cfe71a3cb9c75903cf56ca7658821f1d8ea5f182895c5d549df9c3daf508a9e4bf59c0fd97348fe4c5ca7a54ed9e66f57fb91811ba43b5799ccec092bc11738c8ed6e6ce1606bc04831a2928187c112174ca766a8ca80d49fb92cde5063d48b0203010001',
    '30819f300d06092a864886f70d010101050003818d0030818902818100b6558d050aec2402e87dc7f03a8bea28191cfd2fa0e4bec7a7df980c66f38e42bffc84f98ef17ec192c6ed5b9c517f8675a1231590cc9ae03d58f3bc91b4c9651caed7f50fdd166236f5586276626ee167eadf9ce7ef8da7927cb81fe417c723f09e28295abfbbd3dc8d8764bf2b6373e6a169b9dc7fed3d0c3d8e1b5e89897f0203010001'
]


@app.route("/")
def root():
    return render_template('index2.html')


@app.route("/upload", methods=['POST'])
def upload():
    payload = request.files
    file_ptr = payload['file']

    # Send file to IPFS, and return hash
    file_stream = file_ptr.read()
    response = api.add_bytes(file_stream)

    # Generate using shamir secret
    encrypted_keys = BitcoinToB58SecretSharer.split_secret(str(response), 2, 3)

    # Encrypt with Public keys
    key1 = RSA.importKey(binascii.unhexlify(request.form['key1']))
    key2 = RSA.importKey(binascii.unhexlify(request.form['key2']))
    key3 = RSA.importKey(binascii.unhexlify(request.form['key3']))

    pubs = [key1, key2, key3]
    encrypted = [k.encrypt(e, 1024)[0].encode('hex') for k, e in zip(pubs, encrypted_keys)]
    return render_template('res.html', enc1=encrypted[0], enc2=encrypted[1], enc3=encrypted[2])


@app.route("/decrypt")
def decrypt():
    return render_template('decrypt.html')


@app.route("/decrypt/execute", methods=['POST'])
def submit():
    data1 = request.form['data1']
    data2 = request.form['data2']

    ipfs_path = BitcoinToB58SecretSharer.recover_secret(map(str, [data1, data2]))
    data = api.cat(ipfs_path)

    resp = Response(data)
    resp.headers['Content-Type'] = 'application/pdf'
    return resp


if __name__ == "__main__":
    app.run()
