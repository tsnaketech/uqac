package simulation;

import app.Initialization;
import environment.*;


public class Car extends CarType {

	public int idCar;
	public int typeCar;
	public int damageState;
	public Highway actualHighway; // Ici la totalité de l'objet highway est passé en argument
	public int position;
	public ManageHighway managH;
	private int startCar = 0;
	private int idNextHighway;
	private int previousPosition;
	private int futurePosition;
	private ManageCar managC;
	public int idHighway;
	public int turnRoad;
	private int numberTurnOver = 0;
	private int initNumber=0;
	private int initialPosition=0;
	private int tempNumber;
	private int turnOver = 0;
	

	public Car(int idCar, int typeCar, int damageState, Highway actualHighway, int position,int maxSpeed, String name,ManageHighway managH,ManageCar managC) {
		super(maxSpeed,name);
		this.idCar = idCar;
		this.typeCar = typeCar;
		this.damageState = damageState;
		this.actualHighway = actualHighway;
		this.position = position;
		this.managH = managH;
		this.managC = managC;
		this.idHighway = actualHighway.getIdHighway();
		this.turnRoad = 0;
		this.initialPosition = position;

	}

	public int carDrive() {
		
		int highwayDistance = this.actualHighway.getDistance();
		float tempSpeed = this.actualHighway.getSpeedMultiplier();
		int realSpeed = (int)(this.maxSpeed * tempSpeed);
		int crash = 0;
		int idActualHighway = actualHighway.getIdHighway();
		int exitHighway = 0;
		int tabAccessRoad = this.actualHighway.getNextAccessRoad(this.position);
		int nextAccessRoad = tabAccessRoad;
		turnOver = 0;
		this.damageState++; // Au fils du temps la voiture se détériore
		
		Initialization init = new Initialization();
		int randomNumberChangeH = init.getRandomNumber(1, 2);
		turnOver = this.changeRoad(this.actualHighway.getRandomNumberAccessRoad(), nextAccessRoad);
		
		
		if(turnOver == 1) {
			exitHighway = 1; // La voiture va chercher à changer d'autoroute
		}

		if(startCar == 0) {
			startCar = 1;
			System.out.println();
			System.out.println("La voiture " + this.idCar + " démarre à " + this.position + " ( max: " + this.actualHighway.getDistance() + " )");	
		}
		
		System.out.println("Prochaine voie d'accès : " + nextAccessRoad + " pour la voiture " + idCar);


		if (exitHighway == 0) {

			if (this.position + realSpeed < highwayDistance) { // Condition qui gère la position lors d'une boucle d'une autoroute	

				this.previousPosition = this.position;
				this.futurePosition = this.position + realSpeed;
				crash = this.testCrash(this.previousPosition,this.futurePosition);
				this.position = this.futurePosition;

			} else if((this.position + realSpeed )== highwayDistance){	
				this.position = 0;
			} else {		
				this.position = (this.position + realSpeed) - highwayDistance;
			}

		} else if(exitHighway == 1) {

			if (this.position + realSpeed < nextAccessRoad) {

				this.position = this.position + realSpeed;
				
			} else if((this.position + realSpeed )== nextAccessRoad){

				this.changeHighway(idActualHighway,randomNumberChangeH);
				this.position = 0;

			} else {

				this.changeHighway(idActualHighway,randomNumberChangeH);
			}
		}
		
		if (this.damageState >= 50) {
			crash ++;
			System.out.println();
			System.out.println("	[*] La voiture " + this.idCar + " est en panne à la position: " + this.position); 
		} else {
			System.out.println();
			System.out.println("La voiture " + this.idCar + " roule et atteint " + this.position + " ( max: " + this.actualHighway.getDistance() + " )");	
		}
		return crash;
	}

	public void changeHighway(int idActualHighway,int randomNumberChangeH) {

		System.out.println();
		System.out.println("	--- Changement d'autoroute ---- ");

		this.idNextHighway = managH.changeHighway(idActualHighway,randomNumberChangeH,idCar);
		this.actualHighway = managH.getHighwayInformation(this.idNextHighway);
		this.position = actualHighway.getNextAccessRoad(this.position);
		this.initialPosition = position;
		numberTurnOver = 0;
		this.idHighway = this.idNextHighway;
	}

	
	public int testCrash(int previousV1, int futureV1) {

		int avantV1 = previousV1;
		int apresV1 = futureV1;
		int avantV2 =  15;
		int apresV2 = 21;
		int idHighwayV1;
		int idHighwayV2 = 0;
		int idCarV1 = this.idCar;
		int idCarV2 = 0;
		int initCar = 1;
		int crash = 0;
		idHighwayV1 = this.idHighway;
		

		for(int i=0; i<3; i++) {

			initCar = 1;
			avantV2 = managC.getAllposition(i)[0];
			apresV2 = managC.getAllposition(i)[1];

			idHighwayV2 = managC.getIdHighway(i);
			idCarV2 = i + 1;

			if (avantV2 == apresV2) {
				initCar = 0;				
			}
			
			if( (((int) Math.round(avantV1-avantV2)) < 15) && (idHighwayV1 == idHighwayV2) && (idCarV1 != idCarV2)) {
				System.out.println();
				System.out.println(" -- La voiture " + idCarV1 + " va chercher à éviter un crash avec " + idCarV2);
				System.out.println();
				this.turnOver = 1;
				
			}

			if((avantV1 <= avantV2) && (apresV1 >= apresV2) && (idHighwayV1 == idHighwayV2) && (idCarV1 != idCarV2) && (initCar == 1)) {

				System.out.println();
				System.out.println("	********* CRASH DE VOITURE ******** ");
				System.out.println();
				System.out.println("***** Entre la voiture" + idCarV1 + " et la voiture " + idCarV2 + " Positions:  " + avantV1 + "->" + apresV1 + " et " + avantV2 + "->" + apresV2 + " *******");
				crash = crash + 1;
			}
		}
		return crash;
	}
	
	

	
	public int changeRoad(int numberAccessRoad,int nextAccessRoad) {
				
		if(initNumber == 0) {
			tempNumber = initialPosition;
		}
		
		if(nextAccessRoad != tempNumber) {
			tempNumber = nextAccessRoad;
			numberTurnOver++;
			initNumber = 1;
		}
		
		if(numberTurnOver > numberAccessRoad) {
			
			initNumber = 0;
			System.out.println();
			System.out.println("	** Voiture" + idCar + " à fait un tour et cherche à sortir !**");
			System.out.println();
			
			return 1;
		}	
		return 0;
	}
	
	
	public int getIdHighway() {
		return idHighway;
	}

	public int getPreviousPosition() {
		return previousPosition;
	}

	public int getFuturePosition() {
		return futurePosition;
	}
	
}