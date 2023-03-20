import time
import subprocess as sp

proc = sp.Popen(['python', 'mqtt_sub.py'], stdout=sp.PIPE, stderr=sp.PIPE)
while True:
    error_code = proc.poll()
    # オブジェクト番号がない=サブプロセスが実行中
    if error_code is None:
        time.sleep(5)
    # サブプロセス終了
    else:
        for line in proc.stdout.readlines():
            print(line.decode(encoding='cp932'), end='')
        # 正常終了
        if error_code == 0:
            e = ''
        # 異常終了
        else:
            e = proc.stderr.readlines()[-1].decode()
            proc = sp.Popen(['python', 'mqtt_sub.py'], stdout=sp.PIPE, stderr=sp.PIPE)
