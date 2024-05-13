package oracle;

public class Judgement extends Parent implements JudgementInterface {

	// Vue
	
	 public void pardon() {
		 Oracle.getInstance().getListen().penitence();
	 }
	
	 public void avarice() {
		 Oracle.getInstance().getMiracle().disparition();
	 }
	 
	 public void colere() {
		 Oracle.getInstance().getCouncil().ira();
	 }
	 
	 
	
	// Caché
	
	public void luxure() {
		 Oracle.getInstance().print("La luxure causera votre perte");
	}
	
	public void critique() {
		 Oracle.getInstance().print("Ne critiquez pas, ne jugez pas. Observez.");
	}
}
