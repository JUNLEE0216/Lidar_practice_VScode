import roslibpy
import numpy as np


def callback(message):
    ranges = np.array(message['ranges'])

    front = np.r_[ranges[350:360], ranges[0:10]]
    left  = ranges[80:100]
    right = ranges[260:280]

    front_dist = np.mean(front)
    left_dist  = np.mean(left)
    right_dist = np.mean(right)

    safe_dist = 0.5

    if front_dist < safe_dist:
        action = "turn_left" if left_dist > right_dist else "turn_right"
    else:
        action = "go_forward"

    print(f"front={front_dist:.2f}, left={left_dist:.2f}, right={right_dist:.2f} -> action={action}")

def main():
    client = roslibpy.Ros(host='172.19.160.132', port=9090)
    client.run()

    subscriber = roslibpy.Topic(client, '/scan', 'sensor_msgs/LaserScan')
    subscriber.subscribe(callback)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        subscriber.unsubscribe()
        client.terminate()

if __name__ == '__main__':
    main()
