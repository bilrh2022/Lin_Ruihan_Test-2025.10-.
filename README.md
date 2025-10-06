# Robot's Morning Routine BT
>注意：提交Github后发现该README文件显示异常，行为树结构无法正常显示，部分加粗出现问题，建议下载查看

## 如何运行

在终端中执行以下命令：
给 `test.sh` 添加执行权限
```bash
chmod +x test.sh
```
运行`test.sh` 
```bash
./test.sh
```

## 行为树结构

Morning Routine [Sequence]
├── Alarm Handler [Selector]
│   ├── Handle Alarm [Sequence]
│   │   ├── Check Alarm [IsAlarmRinging]
│   │   └── Snooze [HitSnoozeButton]
│   └── Get Up [GetOutOfBed]
└── Workday Coffee [Sequence]
    ├── Check Workday [IsWorkday]
    └── Brew Coffee [BrewCoffee]

>注释：该行为树结构通过AI生成，自己能够理解但是没办法画得这么清晰

## 控制节点使用说明

### Sequence
- **主流程（Morning Routine）**是顺序执行，因为要先处理闹钟，再处理咖啡
- **处理闹钟（Handle Alarm）**是顺序执行，因为检查闹钟和按掉闹钟有严格的先后顺序依赖
- **工作日咖啡（Workday Coffee）**是顺序执行，因为只有工作日才冲咖啡
### Selector
- **是否处理闹钟（Alarm Handler）**是顺序执行，因为该流程是在"处理闹钟"和"直接起床"之间选择执行路径，只需要其中一个路径成功即可继续。

## 工作日咖啡实现

新增 `IsWorkday` 行为节点
```python
class IsWorkday(py_trees.behaviour.Behaviour):

    """检查是否是工作日"""

    def __init__(self, name):

        super(IsWorkday, self).__init__(name)

        self.blackboard = self.attach_blackboard_client(name="WorkdayCheck")

        self.blackboard.register_key("is_workday", access=py_trees.common.Access.WRITE)

  

    def update(self):

        # 随机决定是否是工作日

        if random.choice([True, False, True]):  # 2/3概率是工作日

            print("Workday")

            self.blackboard.is_workday = True

            return py_trees.common.Status.SUCCESS

        else:

            print("Weekend")

            self.blackboard.is_workday = False

            return py_trees.common.Status.FAILURE
```
使用Sequence组合: 将工作日检查和冲咖啡组合成一个序列
```python
	coffee_sequence = py_trees.composites.Sequence("Workday Coffee", memory=True)

    coffee_sequence.add_child(IsWorkday("Check Workday"))

    coffee_sequence.add_child(BrewCoffee("Brew Coffee"))
```
然后将其集成到行为树
```python
	root.add_child(coffee_sequence)
```


