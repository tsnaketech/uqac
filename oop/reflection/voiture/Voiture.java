package voiture;

public class Voiture {

	public int vitesse = 10;
	private int position = 0;
	private int id;
	
	private static int _id = 0;
	
	public Voiture(int vitesse){
		this.vitesse = vitesse;
		this.id = _id++;
	}
	
	public void deplacement() {
		position += vitesse;
	}
	
	@Override
	public String toString() {
		return ("Voiture(viesse=" + vitesse + "; position=" + position + "; id=" + id + ")");
	}
	
	public int getVitesse() {
		return vitesse;
	}
	
	public int getPosition() {
		return position;
	}

	public int getId() {
		return id;
	}
}
