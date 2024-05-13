/****************
 Monitoring d'appels de méthodes: exemple de la pile
 Cours: 8INF958
 Auteur: Klaus Havelund
****************/
class Test {
	public static void main(String[] args) {
		StackInterface stack = new Stack();

		for (int i = 0; i < 1500; i++) {
			stack.push(i);
		}

		for (int i = 0; i < 1500; i++) {
			stack.pop();
		}
	} 
} 
 
