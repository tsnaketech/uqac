package environment;

public class AccessRoad {

	public int idAccessRoad;
	public int idHighway;
	public int locationAccessRoad;

	public AccessRoad(int idAccessRoad, int idHighway, int locationAccessRoad) {
		
		this.idAccessRoad = idAccessRoad;
		this.idHighway = idHighway;
		this.locationAccessRoad = locationAccessRoad;
	}

	public int getIdAccessRoad() {
		return idAccessRoad;
	}

	public void setIdAccessRoad(int idAccessRoad) {
		this.idAccessRoad = idAccessRoad;
	}

	public int getLocationAccessRoad() {
		return locationAccessRoad;
	}

	public void setLocationAccessRoad(int locationAccessRoad) {
		this.locationAccessRoad = locationAccessRoad;
	}	
	
}