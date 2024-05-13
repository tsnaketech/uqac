package oracle;

public class Listen extends Parent implements ListenInterface {

	// Vue
	
	 public void secret() {
		 Oracle.getInstance().print("Se que tu me dis restera entre nous");
	 }
	  
	 public void mort() {
		 Oracle.getInstance().getMiracle().retour();
	 }
	 
	 public void luxuria() {
		 Oracle.getInstance().getJudgement().luxure();
	 }
	 
	 public void foi() {
		 Oracle.getInstance().getCouncil().foi();
	 }
	
	// Caché
	 
	 public void penitence() {
		 Oracle.getInstance().print("Vos péchés sont pardonnés");
	 }
	 
	 
}
