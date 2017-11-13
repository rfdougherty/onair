try:
    import usocket as socket
except:
    import socket

try:
    import uselect as select
except:
    import select

from led import *

np = Led()

port = 80

timeout = 0.01

#HTML to send to browsers
html = """<!DOCTYPE html>
<html>
<head> <title>ON AIR</title> </head>
<center><h2>Control your ON AIR sign</h2></center>
<form>
ON AIR:
<button name="onair" value="on" type="submit">ON AIR</button>
<button name="onair" value="off" type="submit">OFF AIR</button><br><br>
</form>
</html>
"""

def main():
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", port)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:"+str(port))

    while True:
      ready_read,ready_write,has_err = select.select([s],[],[],timeout)
      for sock in ready_read:
        conn,addr = s.accept()
        print("Got a connection from %s" % str(addr))
        request = conn.recv(1024)
        print("Content = %s" % str(request))
        request = str(request)
        on = request.find('/?onair=on')
        off = request.find('/?onair=off')
        if on == 6:
            print('TURN ON')
            np.scanner_init(delay=1, rgbw=(255,0,0,0), back=(0,50,255,50))
        if off == 6:
            print('TURN OFF')
            np.clear()
        response = html
        conn.send(response)
        conn.close()
      np.update()

main()

