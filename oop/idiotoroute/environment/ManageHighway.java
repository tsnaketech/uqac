package environment;

public class ManageHighway {

	public Highway[] hlist;
	public int randomNumberAccessRoad;

	public ManageHighway(Highway[] hlist) {
		this.hlist = hlist;
		this.randomNumberAccessRoad = 3;
	}

	public Highway getHighwayInformation(int number) {
		return hlist[number];
	}

	public int getRandomNumber(int idHighway) {

		int result = hlist[idHighway].getRandomNumberAccessRoad();
		return result;
	}

	public int changeHighway(int idActualHighway,int randomNumber,int idCar) {

		int number = 1 ;
		if(idActualHighway == 1) {
			number = 2;
		}
		if(idActualHighway == 2) {
			if(randomNumber == 1) {
				number = 1;
			}else {
				number = 3;
			}
		}
		if(idActualHighway == 3) {

			if(randomNumber == 1) {
				number = 2;
			}else {
				number = 4;
			}
		}	
		if(idActualHighway == 4) {

			if(randomNumber == 1) {
				number = 3;
			}else {
				number = 5;
			}
		}	
		if(idActualHighway == 5) {
			number = 4;
		}

		System.out.println();
		System.out.println("	--- Nouvelle autoroute: " + number + " pour la voiture " + idCar +" ----");
		number --; // Le tableau commençant à 0. Nous avons laissé les chiffres au dessus pour la compréhension

		return number;
	}
	
}