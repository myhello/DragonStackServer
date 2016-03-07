#ifndef _TASKQUEQE_H
#define _TASKQUEQE_H

#include <queue>
using namespace std;

struct Task{
	/* data */
	int t_id;
	char t_data[50];
};


class TaskQueue
{
public:
	TaskQueue();
	~TaskQueue();

	//判断队列是否为空
	bool isEmpty();

	//入队
	void enqueue(struct Task* task);

	//出队
	void dequeue(struct Task* &task);

	int getQsize();
	/* data */
private:
	queue<struct Task*> Queue;
	int q_size;

};

#endif
