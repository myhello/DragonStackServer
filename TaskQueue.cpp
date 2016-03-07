#include "TaskQueue.h"


TaskQueue::TaskQueue(){}
TaskQueue::~TaskQueue(){}
//判断队列为空
bool TaskQueue::isEmpty()
{
	return Queue.empty();
}

//入队
void TaskQueue::enqueue(struct Task* task)
{
	Queue.push(task);
}

//出队
void TaskQueue::dequeue(struct Task* &task)
{
	task = Queue.front();
	Queue.pop();
}

//取队列长
int TaskQueue::getQsize()
{
	return Queue.size(); 
}
