import java.util.ArrayList;

import stev.booleans.And;
import stev.booleans.Or;
import stev.booleans.PropositionalVariable;
import stev.booleans.BooleanFormula;
import stev.booleans.Implies;
import stev.booleans.Not;

public abstract class Constraint {


	public static int n = 9;
	public static int square = (int) Math.sqrt(n);

	/*
	 * Premiere contrainte :
	 * 	Chaque case ne peut contenir qu’un chiffre entre 1 et 9.
	 * 	par exemple pour la premiere case cela donne : 
	 * 	(111 | 112 | 113 | 114 | 115 | 116 | 117 | 118 | 119)
	 * 	Un "ou exclusif" aurait été plus précis mais il n'est pas disponible dans la bibliotheque.
	 * 	Neanmoins, grace aux contraintes 2,3, et 4, il ne peut y avoir qu'un seul chiffre par case.
	 */
	public static BooleanFormula constraint1() {
		ArrayList<BooleanFormula> conditions  = new ArrayList<>();
	    for (int r = 1; r <= n ; r++) {
	        for(int c = 1; c <= n; c++) {
	        	ArrayList<BooleanFormula> values = new ArrayList<>();
	            for(int v = 1; v <= n; v++) {
	            	values.add(getPropositionalVariable(r, c, v));
				}
	            conditions.add(new Or(values));
	        }
	    }
	    return new And(conditions);
	}

	/*
	 * Deuxieme contrainte :
	 * 	Chaque chiffre doit apparaître exactement une fois dans chaque ligne de la grille
	 * 	par exemple pour le chiffre 1 sur la premiere case cela donne : 
	 * 	(111 -> (!211 & !311 & !411 & !511 & !611 & !711 & !811 & !911 )
	 */
	public static BooleanFormula constraint2() {
		ArrayList<BooleanFormula> conditions  = new ArrayList<>();
		for(int r = 1; r <= n; r++) {
			for(int c = 1; c <= n; c++) {
				for(int v = 1; v <= n; v++) {
					ArrayList<BooleanFormula> not = new ArrayList<>();
					for(int i = 1; i < n; i++) {
						if(r != i) {
							not.add(new Not(getPropositionalVariable(i, c, v)));
						}
					}
					conditions.add(new Implies(getPropositionalVariable(r, c, v), new And(not)));
				}
			}
		}
		return new And(conditions);
	}
	
	/*
	 * Troisieme contrainte :
	 * 	Chaque chiffre doit apparaître exactement une fois dans chaque colonne de la grille
	 * 	par exemple pour le chiffre 1 sur la premiere case cela donne : 
	 * 	((111 -> (!121 & !131 & !141 & !151 & !161 & !171 & !181 & !191))
	 */
	public static BooleanFormula constraint3() {
		ArrayList<BooleanFormula> conditions  = new ArrayList<>();
		for(int r = 1; r <= n; r++) {
			for(int c = 1; c <= n; c++) {
				for(int v = 1; v <= n; v++) {
					ArrayList<BooleanFormula> not = new ArrayList<>();
					for(int i = 1; i < n; i++) {
						if(c != i) {
							not.add(new Not(getPropositionalVariable(r, i, v)));
						}
					}
					conditions.add(new Implies(getPropositionalVariable(r, c, v), new And(not)));
				}
			}
		}
		return new And(conditions);
	}
	
	/*
	 * Quatrieme contrainte :
	 *  chaque chiffre doit apparaître exactement une fois dans chacune des neuf sous-grilles de taille 3×3
	 *  par exemple pour le chiffre 1 sur la premiere case cela donne : 
	 *  (111 -> (!121 & !131 & !211 & !221 & !231 & !311 & !321 & !331))
	 */
	public static BooleanFormula constraint4() {
        ArrayList<BooleanFormula> conditions = new ArrayList<>();
        for(int v = 1; v <= n; v++) {
            for(int i = 0; i<square; i++) {
                for(int j = 0; j < square; j++) {
                    for(int r = 1; r <= square; r++) {
                        for(int c = 1; c <= square; c++) {
                            ArrayList<BooleanFormula> values = new ArrayList<>();
                            for(int x = 1; x <= square; x++) {
                                for(int y = 1; y <= square; y++) {
                                    if(x != r || y != c) {
                                        int row_i = square*i+x;
                                        int colm_j= square*j+y;
                                        values.add(new Not(getPropositionalVariable(row_i, colm_j, v)));
                                    }
                                    
                                }
                            }
                            int row_i = square*i+r;
                            int colm_j= square*j+c;
                            conditions.add(new Implies(getPropositionalVariable(row_i, colm_j, v),new And(values)));
                        }
                        
                    }
                   
                }
            }
        }
        return new And(conditions);
	}
	
	/**
	
	#26###81#
	3##7#8##6
	4###5###7
	#5#1#7#9#
	##39#51##
	#4#3#2#5#
	1###3###2
	5##2#4##9
	#38###46#
	
	*/
	
	/* 
	 * Cinquième contrainte : contrainte du sudoku incomplet
	 *  exemple avec la grille ci dessus : on devrait avoir ((122 & 000) & (136 & 000) & (178 & 000) 191 & 000) & ...)
	 *  si on ajoute pas le deuxieme terme '000', la clause est considéré comme vide lorsqu on la transforme en cnf.
	 *  grace à la premire contrainte, le '000' ne pose pas de probleme.
	 */
	public static BooleanFormula constraintSudoku(String sudoku) {
			
			char[] sudokuToCharList=sudoku.toCharArray();
			
			ArrayList<BooleanFormula> conditions = new ArrayList<>();
			for(int i=0;i<sudokuToCharList.length;i++) {
				//search for constraints
				if(sudokuToCharList[i]!='#') {
					int r=((int)(i/9))+1;
					int c=i%9+1;
					int v=Character.getNumericValue(sudokuToCharList[i]);
					conditions.add(new Or(getPropositionalVariable(r,c,v),getPropositionalVariable(0,0,0)));
				}
			}
			return new And(conditions);
		}
	
	/*
	 * Retourne une variables de ligne + colonne + valeur
	 */
	private static PropositionalVariable getPropositionalVariable(int x, int y, int z) {
		return new PropositionalVariable(String.valueOf(x * 100 + y * 10 + z));
	}
	
}
