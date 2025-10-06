#!/usr/bin/env python3
"""
Robot's Morning Routine Behavior Tree
模拟机器人早晨起床流程的行为树
"""

import py_trees
import random
import time

class IsAlarmRinging(py_trees.behaviour.Behaviour):
    """检查闹钟是否在响（随机返回成功或失败）"""
    def __init__(self, name):
        super(IsAlarmRinging, self).__init__(name) # 初始化父类py_trees.behaviour.Behaviour
        self.blackboard = self.attach_blackboard_client(name="AlarmCheck") 
        self.blackboard.register_key("alarm_ringing", access=py_trees.common.Access.WRITE) 

    def update(self):
        # 随机决定闹钟是否在响
        if random.choice([True, False]):
            print("Alarm is ringing! ")
            self.blackboard.alarm_ringing = True
            return py_trees.common.Status.SUCCESS
        else:
            print("Alarm is not ringing.")
            self.blackboard.alarm_ringing = False
            return py_trees.common.Status.FAILURE

class HitSnoozeButton(py_trees.behaviour.Behaviour):
    """按掉闹钟小睡"""
    def update(self):
        print("Snoozing...")
        return py_trees.common.Status.SUCCESS

class GetOutOfBed(py_trees.behaviour.Behaviour):
    """起床"""
    def update(self):
        print("Getting up!")
        return py_trees.common.Status.SUCCESS

class BrewCoffee(py_trees.behaviour.Behaviour):
    """冲咖啡"""
    def update(self):
        print("Brewing coffee...")
        return py_trees.common.Status.SUCCESS

class IsWorkday(py_trees.behaviour.Behaviour):
    """检查是否是工作日"""
    def __init__(self, name):
        super(IsWorkday, self).__init__(name)
        self.blackboard = self.attach_blackboard_client(name="WorkdayCheck")
        self.blackboard.register_key("is_workday", access=py_trees.common.Access.WRITE)

    def update(self):
        # 随机决定是否是工作日
        if random.choice([True, False, True]):  # 2/3概率是工作日
            print("Workday")
            self.blackboard.is_workday = True
            return py_trees.common.Status.SUCCESS
        else:
            print("Weekend")
            self.blackboard.is_workday = False
            return py_trees.common.Status.FAILURE

def create_morning_routine_tree():
    """创建早晨起床流程的行为树"""
    
    # 创建根节点 - 序列（所有子节点必须按顺序成功）
    root = py_trees.composites.Sequence("Morning Routine", memory=True)
    
    # 闹钟处理部分 - 选择器（只要一个子节点成功即可）
    alarm_handler = py_trees.composites.Selector("Alarm Handler", memory=False)
    
    # 闹钟检查和处理序列
    alarm_sequence = py_trees.composites.Sequence("Handle Alarm", memory=True)
    alarm_sequence.add_child(IsAlarmRinging("Check Alarm"))
    alarm_sequence.add_child(HitSnoozeButton("Snooze"))
    
    # 添加到闹钟处理选择器
    alarm_handler.add_child(alarm_sequence)
    alarm_handler.add_child(GetOutOfBed("Get Up"))  # 如果闹钟没响，直接起床
    
    # 工作日咖啡检查序列
    coffee_sequence = py_trees.composites.Sequence("Workday Coffee", memory=True)
    coffee_sequence.add_child(IsWorkday("Check Workday"))
    coffee_sequence.add_child(BrewCoffee("Brew Coffee"))
    
    # 构建完整的行为树
    root.add_child(alarm_handler)    # 先处理闹钟
    root.add_child(coffee_sequence)  # 然后检查是否需要冲咖啡
    
    return root

def main():
    """主函数"""
    
    # 创建行为树
    behaviour_tree = create_morning_routine_tree()
    
    # 设置行为树
    tree = py_trees.trees.BehaviourTree(behaviour_tree)
    
    # 打印行为树结构
    # print("\n行为树结构:")
    # print(py_trees.display.ascii_tree(tree.root))
    
    # 运行行为树多次以展示不同情况
    for i in range(7):
        print(f"\n---  {i+1}  ---")
        tree.tick()
        print(f"Status: {behaviour_tree.status}")

if __name__ == "__main__":
    main()