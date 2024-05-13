package environment;

public class Materials {

	public String nameMaterials;
	public float speedMultiplier;
	
	
	public Materials(String nameMaterials) {
		
		this.nameMaterials = nameMaterials;
		
		if(nameMaterials == "Beton") {
			this.speedMultiplier = new Float(1);
		} else if(nameMaterials == "Bitume") {
			this.speedMultiplier = new Float(1.5);
		} else if(nameMaterials == "Terre") {
			this.speedMultiplier = new Float(0.5);
		}else {
			System.out.println("Erreur dans le choix des materiaux: Beton est choisi par défaut");
			this.speedMultiplier = new Float(1);
		}
				
	}

	public float getSpeedMultiplier() {
		return speedMultiplier;
	}
	
}
