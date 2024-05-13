package environment;

import app.Initialization;

public class Highway extends Materials{

	public int idHighway;
	public int nbExit;
	public int diameter;
	public int distance;
	public int materials;
	public float speedMultiplier;
	private int randomNumberAccessRoad;
	private AccessRoad[] tabAccessRoad; // Tableau stockant un nombre aléatoire de point d'accès

	public Highway(int idHighway, int nbExit, int diameter,String nameMaterials) {

		super(nameMaterials);
		this.idHighway = idHighway;
		this.nbExit = nbExit;
		this.diameter = diameter;
		this.distance = this.getNewDistance(diameter);
		Initialization init = new Initialization();
		Materials material = new Materials(nameMaterials);
		this.speedMultiplier = material.getSpeedMultiplier();

		
		// ------------ Création de 3 access road par autoroutes  ------------
		//this.randomNumberAccessRoad = 3;
		//tabAccessRoad = new AccessRoad[randomNumberAccessRoad];

		// ------------ Création de 2 à 6 access road par autoroutes  ------------
		this.randomNumberAccessRoad = init.getRandomNumber(2,6);
		tabAccessRoad = new AccessRoad[randomNumberAccessRoad];
		
		
		System.out.println();
		System.out.println("	- Création de l'autoroute " + this.idHighway);

		for(int i=0; i<randomNumberAccessRoad; i++) {

			tabAccessRoad[i] = new AccessRoad(init.getNewIdAccessRoad(),this.idHighway,init.getRandomNumber(0,distance));
			System.out.println("Création de la voie d'accès "+ tabAccessRoad[i].getIdAccessRoad() + "(Position = " + tabAccessRoad[i].getLocationAccessRoad() + ")" + " sur l'autoroute " + this.idHighway);
		}
	}
	
	public int getNextAccessRoad(int carPosition) { // Renvoi la sortie la plus proche

		int nextAccessRoad = 1000;
		int potentialNextAccessRoad = tabAccessRoad[0].getLocationAccessRoad();
		int i;
		int verif=0;

		for(i=0;i<this.randomNumberAccessRoad;i++) {
			potentialNextAccessRoad = tabAccessRoad[i].getLocationAccessRoad();

			if((potentialNextAccessRoad <= nextAccessRoad) && (potentialNextAccessRoad > carPosition)) {
				nextAccessRoad = potentialNextAccessRoad;
				verif = 1;
			}
		}

		if(verif == 0) { // Si il n'y a pas de solution c'est que la prochaine sortie est la premiere de l'autoroute
			nextAccessRoad = this.getSmallestAccessRoad();
		}

		
		return nextAccessRoad; 
	}

	public int getDistance() {
		return this.distance;
	}

	public int getRandomNumberAccessRoad() {
		return randomNumberAccessRoad;
	}

	public int getIdHighway() {
		return this.idHighway;
	}

	public float getSpeedMultiplier() {
		return this.speedMultiplier;
	}

	public int getNewDistance(int diameter) {
		return (int) Math.round(Math.PI*diameter);
	}
	
	public int getSmallestAccessRoad() { // Permet de retourner la voie d'accès avec la plus petite valeur

		int smallestNumber;
		smallestNumber = this.tabAccessRoad[0].getLocationAccessRoad();

		for(int i=1;i<this.randomNumberAccessRoad;i++) {

			if(smallestNumber > tabAccessRoad[i].getLocationAccessRoad()) {

				smallestNumber = tabAccessRoad[i].getLocationAccessRoad();
			}	
		}
		return smallestNumber;
	}
	
}