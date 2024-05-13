package app;

import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import environment.*; 
import simulation.*;
import app.Initialization;

public class App {

	public static void main(String[] args) {

		System.out.println();
		System.out.println();
		System.out.println("	----- Démarage de la simulation ----");
		System.out.println();
		System.out.println();

		Scanner sc = new Scanner(System.in);

		int exit=1;
		int crash=0;

		Highway[] tabHighway;
		Car[] tabCar;
		tabHighway = new Highway[5];
		tabCar = new Car[3];
		Initialization init = new Initialization();

		Highway a1 = new Highway(init.getNewIdHighway(),3,30,"Beton");
		Highway a2 = new Highway(init.getNewIdHighway(),2,25,"Beton");
		Highway a3 = new Highway(init.getNewIdHighway(),3,20,"Bitume");
		Highway a4 = new Highway(init.getNewIdHighway(),3,15,"Beton");
		Highway a5 = new Highway(init.getNewIdHighway(),3,10,"Terre");
		tabHighway[0] = a1;
		tabHighway[1] = a2;
		tabHighway[2] = a3;
		tabHighway[3] = a4;
		tabHighway[4] = a5;

		ManageHighway managH = new ManageHighway(tabHighway);
		ManageCar managC = new ManageCar(tabCar);
		Car c1 = new Car(1,1,3,a1,0,10,"sportCar",managH,managC);
		Car c2 = new Car(2,2,5,a3,0,8,"cityCar",managH,managC);
		Car c3 = new Car(3,3,10,a5,0,5,"van",managH,managC);
		tabCar[0] = c1;
		tabCar[1] = c2;
		tabCar[2] = c3;

		System.out.println("	----------------------------------------- ");
		
		// Boucle de jeu
		do{
			// Permet d'effectuer une gestion tour par tour en remplacant le sleep()
			//System.out.println(" -- 1 pour continuer -- ");
			//exit = sc.nextInt();

			crash = 0;

			try {
				TimeUnit.SECONDS.sleep(1);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}

			crash = c1.carDrive() + crash;
			crash = c2.carDrive() + crash;
			crash = c3.carDrive() + crash;

		}while(exit == 1 && crash == 0);


		if(crash>0) {
			System.out.println();
			System.out.println();
			System.out.println("	---- Accident ! Tout le monde se stoppe -----");
		}

		System.out.println();
		System.out.println();
		System.out.println("	---- Fin de la simulation d'autoroute -----");
	}

}