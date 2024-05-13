package stev.bowling;

public abstract class Frame {
   protected int m_frameNumber;
   protected int[] m_scores;

   public Frame(int frame_number) throws BowlingException {
      if (frame_number >= 0 && frame_number <= 10) {
         this.m_frameNumber = frame_number;
      } else {
         throw new BowlingException("There is no frame " + frame_number);
      }
   }

   public int getFrameNumber() {
      return this.m_frameNumber;
   }

   public int countPinsDown() {
      if (this.m_scores[0] < 0) {
         return 0;
      } else {
         int pins = 0;
         int[] var5;
         int var4 = (var5 = this.m_scores).length;

         for(int var3 = 0; var3 < var4; ++var3) {
            int x = var5[var3];
            pins += x;
         }

         return pins;
      }
   }

   public int getPinsDown(int roll) {
      if (roll >= 1 && roll < this.m_scores.length + 1) {
         return this.m_scores[roll - 1];
      } else {
         throw new BowlingException("No such roll in this frame");
      }
   }

   public int countRolls() {
      int rolls = 0;
      int[] var5;
      int var4 = (var5 = this.m_scores).length;

      for(int var3 = 0; var3 < var4; ++var3) {
         int x = var5[var3];
         if (x <= 0) {
            break;
         }

         ++rolls;
      }

      return rolls;
   }

   public Frame reset() {
      for(int i = 0; i < this.m_scores.length; ++i) {
         this.m_scores[i] = -1;
      }

      return this;
   }

   public Frame setPinsDown(int roll, int score) throws BowlingException {
      int r_roll = roll - 1;
      if (this.m_scores[r_roll] >= 0) {
         throw new BowlingException("Score already entered for roll " + roll);
      } else {
         this.m_scores[r_roll] = score;
         if (r_roll > 0 && this.m_scores[r_roll - 1] < 0) {
            throw new BowlingException("You must first enter the score for roll " + r_roll);
         } else {
            return this;
         }
      }
   }
}
