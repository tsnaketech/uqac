package stev.bowling;

public class NormalFrame extends Frame {
   public NormalFrame(int frame_number) {
      super(frame_number);
      this.m_scores = new int[2];
      this.reset();
   }

   public NormalFrame setPinsDown(int roll, int score) {
      if (roll >= 1 && roll <= 2) {
         if (roll == 1 && score == 10) {
            this.m_scores[0] = 10;
            this.m_scores[1] = 0;
            return this;
         } else if ((roll != 2 || this.m_scores[0] + score <= 10) && (roll != 1 || this.m_scores[1] + score <= 10)) {
            super.setPinsDown(roll, score);
            return this;
         } else {
            throw new BowlingException("The total score exceeds 10");
         }
      } else {
         throw new BowlingException("There is no such roll " + roll);
      }
   }

   public String toString() {
      String out = "";
      if (this.m_scores[0] < 0) {
         return "  ";
      } else if (this.m_scores[0] == 10) {
         return "X ";
      } else {
         if (this.m_scores[0] == 0) {
            out = out + "-";
         } else {
            out = out + this.m_scores[0];
         }

         if (this.m_scores[1] == 10) {
            out = out + "X";
         } else if (this.m_scores[1] == 0) {
            out = out + "-";
         } else if (this.m_scores[1] < 0) {
            out = out + " ";
         } else if (this.m_scores[0] + this.m_scores[1] == 10) {
            out = out + "/";
         } else {
            out = out + this.m_scores[1];
         }

         return out;
      }
   }
}
