package simulation;

public class CarType {

	public int maxSpeed;
	public String name;
	
	public CarType(int maxSpeed, String name) {

		this.maxSpeed = maxSpeed;
		this.name = name;
		System.out.println();
		System.out.println("	* Création du type de voiture " + this.name);
	}
	
}