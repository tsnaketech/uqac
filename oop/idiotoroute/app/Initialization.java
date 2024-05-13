package app;

public class Initialization {

	public int generateIdHighway = 0;
	public int generateIdAccessRoad = 0;
	
	public int getNewIdHighway() {
		this.generateIdHighway++;
		return generateIdHighway;
	}
	
	public int getNewIdAccessRoad() {
		this.generateIdAccessRoad++;
		return generateIdAccessRoad;
	}

	public int getRandomNumber(int min,int max) {
		int n;
		max++;
		n = (int)((Math.random() * (max - min)) + min);
        return n;	
	}
	
}