#!/usr/bin/env python 
from threading import Lock
from flask import Flask, render_template, session, request, \
    copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

sum=0
w,h = 5, 5
Matrix = [[0 for x in range(w)] for y in range(h)]
kol=1
kk=0
count = -1
x=0
y=0
stop=False
tt=1
f=True
ft=0
ff=0
def background_thread(): 
    global x,y
    global f
    global stop
    global kol,kk,count
    global sum
    global tt
    global w, h
    global ft,ff
    global Matrix
    M = 5
    N = 5
    A = [[0 for x in range(M)] for y in range(N)]
    print(A)
    steps = int((min(N, M) + 1) / 2)
    print(steps)
    print(A[0])
    print('------------------')

    for step in range(steps):
        for i in range(step, M - step):
            A[step][i] = step + 1
            socketio.sleep(0.1)
            sum+=1
            a=''
            for mat in A:
                a=a+str(mat)+'<br>'
        
            socketio.emit('my_response',
                        {'data': a, 'count': count, 'sum': sum, 'x':str(x),'y':str(y),'ft':str(ft),'ff':str(ff),'f':str(f)},
                        namespace='/test')
        for i in range(step + 1, N - step):
            A[i][M - step - 1] = step + 1
            socketio.sleep(0.1)
            sum+=1
            a=''
            for mat in A:
                a=a+str(mat)+'<br>'
        
            socketio.emit('my_response',
                        {'data': a, 'count': count, 'sum': sum, 'x':str(x),'y':str(y),'ft':str(ft),'ff':str(ff),'f':str(f)},
                        namespace='/test')
        for i in range(M - step - 2, step - 1, -1):
            A[N - step -1][i] = step + 1
            socketio.sleep(0.1)
            sum+=1
            a=''
            for mat in A:
                a=a+str(mat)+'<br>'
        
            socketio.emit('my_response',
                        {'data': a, 'count': count, 'sum': sum, 'x':str(x),'y':str(y),'ft':str(ft),'ff':str(ff),'f':str(f)},
                        namespace='/test')
        for i in range(N - step - 2, step - 1, -1):
            A[i][step] = step + 1
            socketio.sleep(0.1)
            sum+=1
            a=''
            for mat in A:
                a=a+str(mat)+'<br>'
        
            socketio.emit('my_response',
                        {'data': a, 'count': count, 'sum': sum, 'x':str(x),'y':str(y),'ft':str(ft),'ff':str(ff),'f':str(f)},
                        namespace='/test')


    '''while True:
        socketio.sleep(0.1)
        if sum<w*h:
            count+=1
            sum+=1
        else:
            print('STOP')
            stop=True

        if f:
            if count>w-1-kk: 
                y=abs(ft-(count-1))
                count=tt
                f=False
                x=count
                ft=w-1

        if f!=True:
            if count>h-1-kk:
                y=abs(ff-(count-1))
                count=tt
                f=True 
                x=count
                ff=h-1


        if f==False and ft==w-1 and ff==h-1:
            ft=0
            kk+=1
        if f and ff==h-1 and ft!=w-1:
            ff=0
            kol+=1
            tt+=1

        if f and stop!=True :
            x=count
            print('TRUE x='+str(x)+' y='+str(y))
            Matrix[abs(y)][abs(ft-x)] = kol
        if f!=True and stop!=True:
            x=count
            print('FALSE x='+str(x)+' y='+str(y))
            Matrix[abs(ff-x)][abs(y)] = kol
    


        a=''
        for mat in Matrix:
            a=a+str(mat)+'<br>'
    
        socketio.emit('my_response',
                    {'data': a, 'count': count, 'sum': sum, 'x':str(x),'y':str(y),'ft':str(ft),'ff':str(ff),'f':str(f)},
                    namespace='/test')
'''


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print('YRA!'+message['dataX'])
    global sum
    sum=0 
    global Matrix
    global w, h
    global kol,kk,count
    global x,y
    global stop
    global f,tt,ft,ff

    stop=False
    x,y=0,0
    count=-1
    kol=1
    kk=0
    tt=1
    f=True
    ft=0
    ff=0

    w=int(message['dataX'])
    h=int(message['dataY'])
    Matrix = [[0 for x in range(w)] for y in range(h)]
    emit('my_response',
         {'data': message['dataX'], 'count': session['receive_count'],'test': 'TEST!'+message['dataX']})



@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',debug=True)
