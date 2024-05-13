package simulation;


public class ManageCar {

	public Car[] carList;

	
	public ManageCar(Car[] carList) {
		//super();
		this.carList = carList;
	}
	
	public int[] getAllposition(int idCar) {
		
		int previousPosition = carList[idCar].getPreviousPosition();
		int futurePosition = carList[idCar].getFuturePosition();

		
		
		int[] mytab = {previousPosition, futurePosition};
		
		return mytab;
	}
	
	public int getIdHighway(int number) {
		
		int idHighway = carList[number].getIdHighway();
		
		return idHighway;
	}
	
}