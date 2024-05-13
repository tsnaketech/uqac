import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import stev.booleans.And;
import stev.booleans.BooleanFormula;
import stev.booleans.Equivalence;
import stev.booleans.Implies;
import stev.booleans.Not;
import stev.booleans.Or;
import stev.booleans.PropositionalVariable;

import org.sat4j.core.VecInt;
import org.sat4j.minisat.SolverFactory;
import org.sat4j.specs.ContradictionException;
import org.sat4j.specs.IProblem;
import org.sat4j.specs.ISolver;
import org.sat4j.specs.TimeoutException;

@SuppressWarnings("unused")
public class SudokuSAT extends Constraint {
	

	/**
	 * Création d'une formule booléenne et convertion en CNF
	 * @return le sudoku complet en String.
	 * @throws Exception 
	 */
	public static String solver(String sudoku) throws Exception  {
		String SolvedSudoku;
		BooleanFormula constraints = new And(constraint1(),constraint2(),constraint3(),constraint4(),constraintSudoku(sudoku));
		
		// Convertion en formule CNF
		BooleanFormula cnf = constraints.toCnf();
		int[][] constraintsClauses=cnf.getClauses();
				
		final int MAXVAR = 1000000;
		final int NBCLAUSES = constraintsClauses.length;

		ISolver solver = SolverFactory.newDefault();

		// Prépare le solveur à accepter les variables MAXVAR. OBLIGATOIRE pour la résolution de MAXSAT
		solver.newVar(MAXVAR);
		solver.setExpectedNumberOfClauses(NBCLAUSES);
		
		// Alimenter le solveur en utilisant le format Dimacs, en utilisant des tableaux d'int
		// (Meilleure option pour éviter les dépendances à l'égard de SAT4J IVecInt)
		for (int i=0;i<NBCLAUSES;i++) {
				solver.addClause(new VecInt(constraintsClauses[i])); // Adapter Array à IVecInt
		}
		
		// Nous avons terminé. Travaillons maintenant sur l'interface IProblem
		IProblem problem = solver;
		if (problem.isSatisfiable()) {
			
			int[] model = problem.model();
			System.out.println("Sudoku solved");
			SolvedSudoku=CnfToString(cnf, model);
			
		} else {
			throw new Exception("No solutions");
		}
		
		return SolvedSudoku;
	}
	
	/*
	 * Convertit le modele obtenu en string
	 */
	public static String CnfToString(BooleanFormula cnf, int [] model) {
		String SolvedSudoku="";
		Map<String,Integer> associations = cnf.getVariablesMap();
		Map<Integer, String> reverseAssociations = associations.entrySet().stream()
				.collect(Collectors.toMap(Map.Entry::getValue, Map.Entry::getKey));
		List<String> StringListSolvedSudoku = new ArrayList<String>();
		
		for (int i = 0; i < model.length; i++) {
			if (model[i] >= 1) {
				StringListSolvedSudoku.add(reverseAssociations.get(model[i]));
			}
		}
		for (String numberOnCase : StringListSolvedSudoku) {
			SolvedSudoku += numberOnCase.substring(2);
		}
		return SolvedSudoku ;
	}
	
	/*
	 * Affiche une grille de sudoku (incomplete et complete) dans la console
	 */
	public static void display(String sudoku) {
		for (int i = 0; i < n; i++) {
			if (i % square == 0){
        		System.out.println("---------------------");
        	}
            for (int j = 0; j < n; j++) {
            	if (j % square == 0 && j != 0){
            		System.out.print("| ");
            	}
            	if (sudoku.charAt(i + j) == '#') {
            		System.out.print("."+" ");
            	} else {
            		System.out.print(sudoku.charAt(i + j)+" ");
            	}
            }
            sudoku = sudoku.substring(n-1);
            System.out.println();
        }
        System.out.println("---------------------");
        System.out.println();
    }

}
