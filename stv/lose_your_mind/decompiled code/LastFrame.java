package stev.bowling;

public class LastFrame extends Frame {
   public LastFrame(int frame_number) {
      super(frame_number);
      this.m_scores = new int[3];
      this.reset();
   }

   public int countRolls() {
      return this.m_scores[0] + this.m_scores[1] < 10 ? 2 : 3;
   }

   public LastFrame setPinsDown(int roll, int score) {
      if (roll >= 1 && roll <= 3) {
         if (roll == 3 && this.m_scores[0] + this.m_scores[1] != 10) {
            throw new BowlingException("No third roll is allowed");
         } else {
            super.setPinsDown(roll, score);
            return this;
         }
      } else {
         throw new BowlingException("There is no such roll " + roll);
      }
   }

   public String toString() {
      String out = "";
      if (this.m_scores[0] < 0) {
         return "   ";
      } else {
         if (this.m_scores[0] == 10) {
            out = out + "X";
         } else if (this.m_scores[0] == 0) {
            out = out + "-";
         } else {
            out = out + this.m_scores[0];
         }

         if (this.m_scores[1] == 10) {
            out = out + "X";
         } else if (this.m_scores[1] == 0) {
            out = out + "-";
         } else {
            if (this.m_scores[1] < 0) {
               return out + "  ";
            }

            if (this.m_scores[0] + this.m_scores[1] == 10) {
               out = out + "/";
            } else {
               out = out + this.m_scores[1];
            }
         }

         if (this.m_scores[0] + this.m_scores[1] == 10) {
            if (this.m_scores[2] == 0) {
               out = out + "-";
            } else if (this.m_scores[2] == 10) {
               out = out + "X";
            } else if (this.m_scores[2] < 0) {
               out = out + " ";
            } else {
               out = out + this.m_scores[2];
            }
         }

         return out;
      }
   }
}
