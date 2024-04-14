import rospy
from clover import srv
from std_srvs.srv import Trigger
import math, socket

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(tolerance)


HOST = ("192.168.11.103", 9090)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print("Connected to", HOST)

msg = client.recv(1024)
print(msg.decode('UTF-8'))

arr = list(map(int, msg.split()))

x, y = arr[0], arr[1]

navigate(x=0, y=0, z=1, frame_id='body', auto_arm=True)
rospy.sleep(2)

navigate_wait(x=x, y=y, z=1, yaw=float('nan'), frame_id='aruco_map')
rospy.sleep(2)

navigate_wait(x=0, y=0, z=1, yaw=float('nan'), frame_id='aruco_map')
rospy.sleep(2)

land()

