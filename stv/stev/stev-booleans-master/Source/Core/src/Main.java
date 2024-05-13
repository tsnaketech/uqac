/* 
 * Mickael LECOCQ 			- 	LECM08109608
 * Pierre Alban LAGUADEC 	- 	LAGP03059906
 * Malo MORICE 				- 	MORM02049807
 * 
 */

public class Main {

	private static int n = 9;
	public static String sudoku;

	public static void main(String[] args) throws Exception  {
		
		if(args.length != 1||args[0].length()!=81) {
			System.out.println("Sudoku required. putnumbers beetween 1 and 9, and '#' for unknown number, you need exactly 81 characters");
			return;
		}
		
		sudoku = args[0];
		
		//sudoku = "#26###81#3##7#8##64###5###7#5#1#7#9###39#51###4#3#2#5#1###3###25##2#4##9#38###46#";
		
		if(sudoku.length() != n*n) {
			System.out.println("Sudoku not valid");
			return;
		}
		
		System.out.println("Sudoku");
		SudokuSAT.display(sudoku);
		
		String sudokuSolved = SudokuSAT.solver(sudoku);
		
		SudokuSAT.display(sudokuSolved);
	}

}
