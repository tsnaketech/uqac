/****************
 Monitoring d'appels de méthodes: exemple de la pile
 Cours: 8INF958
 Auteur: Klaus Havelund
****************/
class Stack implements StackInterface{
	
	private int top;
	private Object[] stack;
	private int stackSize;
	
	public Stack()
	{
		stackSize = 1000;
		stack = new Object[stackSize];
		top = 0;
	}
	
	public void push (Object t)
	{
		if(top == stackSize){
			Object[] newStack = new Object[2 * stackSize];
			for(int i = 0; i < stackSize; i++){
				newStack[i] = stack[i];
			}
			stack = newStack;
			top = stackSize - 1;
			stackSize = 2 * stackSize;
		}
		
		stack[top] = t;
		top++;
	}
	
	
	public Object pop() {
		if (top > 0) {
			top--;
			return stack[top];
		} else {
			return null;
		}
	}
	
	public Object top()
	{
		if (top > 0) {
			return stack[top - 1];
		} else {
			return null;
		}
	}
		
	public boolean isEmpty()
	{
		return top == 0;
	}
	
	public int size()
	{
		return top;
	}
}
