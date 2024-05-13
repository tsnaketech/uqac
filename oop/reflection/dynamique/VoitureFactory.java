package dynamique;

import java.lang.reflect.InvocationTargetException;

import voiture.Voiture;
import voiture.VoitureSport;

public class VoitureFactory {
	
	static int _id = 0;

	public enum ModeConstruction {
		INSTANCIATION,
		META,
		REFLEXION;
	}
	
	public static int generateVitesse() {
		int max = 120;
		int min = 40;
		int vitesse = (int)(Math.random()*(max-min));
		return vitesse;
	}
	
	public static Voiture buildVoiture(ModeConstruction construct, boolean sportive, int vitesse) {
		Voiture voiture = null;

		_id++;
        switch(construct) {
	        case INSTANCIATION:
	        	System.out.println("Création du voiture avec Instanciation");
	        	if (!sportive) {
	        		voiture = new Voiture(vitesse);
	        	} else {
	        		voiture = new VoitureSport();
	        	}
				return voiture;
	        case META:
	        	System.out.println("Création du voiture avec Meta");
	            voiture = VoitureFactoryMetaHelper.generationMetaVoiture(sportive, vitesse, _id);
	            return voiture;
	        case REFLEXION:
	        	System.out.println("Création du voiture avec Reflexion");
	        	if (!sportive) {
	        		try {
						voiture = (Voiture)(Class.forName("voiture.Voiture").getDeclaredConstructor(int.class).newInstance(vitesse));
					} catch (InstantiationException | IllegalAccessException | IllegalArgumentException
							| InvocationTargetException | NoSuchMethodException | SecurityException
							| ClassNotFoundException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
	        	} else {
	        		try {
						voiture = (Voiture)(Class.forName("voiture.VoitureSport").getDeclaredConstructor().newInstance());
					} catch (InstantiationException | IllegalAccessException | IllegalArgumentException
							| InvocationTargetException | NoSuchMethodException | SecurityException
							| ClassNotFoundException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
	        	}
	            return voiture;
        }
		return voiture;
	}
}
