package stev.kwikemart;

public final class PaperRoll {
   public static final PaperRoll SMALL_ROLL = new PaperRoll(25);
   public static final PaperRoll LARGE_ROLL = new PaperRoll(1000);
   private int m_linesLeft;
   private StringBuilder m_strip = new StringBuilder();

   private PaperRoll(int size) {
      this.m_linesLeft = size;
      this.m_strip = new StringBuilder();
   }

   public final String tearUp() {
      String out = this.m_strip.toString();
      this.m_strip = new StringBuilder();
      return out;
   }

   public final int getLinesLeft() {
      return Math.max(0, this.m_linesLeft);
   }

   public final void println(String s) throws PaperRollException.OutOfPaperException {
      String[] lines = s.split("[\\r\\n]");
      String[] var6 = lines;
      int var5 = lines.length;

      for(int var4 = 0; var4 < var5; ++var4) {
         String line = var6[var4];
         if (this.m_linesLeft < 0) {
            throw PaperRollException.OutOfPaperException.instance;
         }

         this.m_strip.append(line).append("\n");
         --this.m_linesLeft;
      }

   }

   public final Object clone() {
      throw new UnsupportedOperationException("A paper roll cannot be cloned");
   }
}
