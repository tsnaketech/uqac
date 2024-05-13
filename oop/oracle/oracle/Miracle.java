package oracle;

public class Miracle extends Parent implements MiracleInterface {

	// Vue
	 public void soin() {
		 Oracle.getInstance().print("Une guérison miraculeuse viens à vous !");
	 }
	 
	 public void charitable() {
		 Oracle.getInstance().getCouncil().charity();
	 }

	 
	 
	// Caché
	 
	 public void retour() {
		 Oracle.getInstance().print("Retour à la vie de votre enfant");
	 }
	 
	 public void disparition() {
		 Oracle.getInstance().print("Disparition de vos bien !!");
	 }
	 

}
