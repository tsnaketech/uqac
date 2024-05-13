package oracle;

public class Council extends Parent implements CouncilInterface {

	// Vue
	 public void critique() {
		 Oracle.getInstance().getJudgement().critique();
	 }
	 
	 public void intuition() {
		 Oracle.getInstance().print("Ecoutez votre intuition.");
	 }
	 
	 public void audace() {
		 Oracle.getInstance().print("Faites preuve d’audace.");
	 }
	 
	// Caché
	 
	 public void ira() {
		 Oracle.getInstance().print("Calmez vous avant la sentence");
	 }
	 
	 public void charity() {
		 Oracle.getInstance().print("Donne tu recevras");
	 }
	 
	 public void ecoute() {
		 Oracle.getInstance().print("Bien écouter c'est presque répondre");
	 }
	 
	 public void foi() {
		 Oracle.getInstance().print("Elle est plus grande force");
	 }
}
