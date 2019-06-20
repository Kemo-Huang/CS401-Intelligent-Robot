# IR Project

## Usage

```bash
git clone https://github.com/Airine/ROS-turtlebot-python.git
or
wget https://github.com/Airine/ROS-turtlebot-python/archive/master.zip
```
### 1. Run ROS

```bash
roslaunch turtlebot_bringup minimal.launch
```

*Do not run other movement controller (like keyborad)*

### 2. Run talker

```bash
python talker.py
```

This [talker.py](./talker.py) register a ros node "chatter", and it would set msgs to those ros nodes who subscribes it (like [main.py](./main.py)).

And if you type keys below, the `chatter` would set corresponding msg below.

```python
commands = {
    'q': 'circle',
    'w': 'dou',
    'e': 'tri',
    'r': 'rotate'
}
```

### 3. Run main.py

```bash
python main.py
```