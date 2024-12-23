import socket
import select

def get_html():
    with open('index.html', 'r') as file:
        html = file.read()
    return html

def parse_rgb_values(request_str):
    try:
        r = int(request_str.split('r=')[1].split('&')[0])
        g = int(request_str.split('g=')[1].split('&')[0])
        b = int(request_str.split('b=')[1].split(' ')[0])

        if all(0 <= value <= 255 for value in (r, g, b)):
            return (r, g, b)
    except (ValueError, IndexError) as e:
        print('Invalid RGB values:', e)

    return None

def handle_client(cl, rgb_callback, rainbow_callback):
    request = cl.recv(1024)
    request_str = request.decode('utf-8')
    print('Request:', request_str)

    if 'GET /?r=' in request_str:
        new_rgb = parse_rgb_values(request_str)
        if new_rgb:
            print('we got new RRRGBBBB yooo')
            rgb_callback(new_rgb)
        else:
            print('RGB values out of range or invalid')
    elif 'GET /?mode=rainbow' in request_str:
        print('fucking rainbowmode activsatedtrdtrsr1111111"!!!')
        rainbow_callback('rainbow')

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    cl.send(get_html())
    cl.close()

def serve_rgb_webpage(port, rgb_callback, rainbow_callback):
    addr = socket.getaddrinfo('0.0.0.0', port)[0][4]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    s.setblocking(False)  # Set the socket to non-blocking
    print('Listening on', addr)
    return s

def handle_web(s, rgb_callback, rainbow_callback):
    readable, _, _ = select.select([s], [], [], 0.1)
    for sock in readable:
        cl, addr = sock.accept()
        print('Client connected from', addr)
        handle_client(cl, rgb_callback, rainbow_callback)
