/****************
 Monitoring d'appels de méthodes: exemple de la pile
 Cours: 8INF958
 Auteur: Klaus Havelund
****************/
interface StackInterface {
	public void push (Object t);
	public Object pop();
	public Object top();
	public boolean isEmpty();
	public int size();	
}
