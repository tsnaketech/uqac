package stev.bowling;

public class GameDemo {
   public static void main(String[] args) {
      Game g = new Game();
      g.addFrame((new NormalFrame(1)).setPinsDown(1, 3).setPinsDown(2, 6));
      g.addFrame((new NormalFrame(2)).setPinsDown(1, 10));
      g.addFrame((new NormalFrame(3)).setPinsDown(1, 5).setPinsDown(2, 0));
      g.addFrame((new NormalFrame(4)).setPinsDown(1, 1).setPinsDown(2, 9));
      g.addFrame((new NormalFrame(5)).setPinsDown(1, 10));
      g.addFrame((new NormalFrame(6)).setPinsDown(1, 0).setPinsDown(2, 0));
      g.addFrame((new NormalFrame(7)).setPinsDown(1, 0).setPinsDown(2, 6));
      g.addFrame((new NormalFrame(8)).setPinsDown(1, 10));
      g.addFrame((new NormalFrame(9)).setPinsDown(1, 2).setPinsDown(2, 8));
      g.addFrame((new LastFrame(10)).setPinsDown(1, 1).setPinsDown(2, 9).setPinsDown(3, 3));
      System.out.println(g);
   }
}
