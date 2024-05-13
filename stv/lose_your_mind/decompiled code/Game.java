package stev.bowling;

import java.util.ArrayList;
import java.util.List;

public class Game {
   public List<Frame> m_frames = new ArrayList(10);

   public Game addFrame(Frame f) {
      if (this.m_frames.size() == 9) {
         if (!(f instanceof LastFrame)) {
            throw new BowlingException("Frame #10 must be an instance of LastFrame");
         }
      } else if (!(f instanceof NormalFrame)) {
         throw new BowlingException("Frame #" + (this.m_frames.size() + 1) + " must be an instance of NormalFrame");
      }

      this.m_frames.add(f);
      return this;
   }

   public String toString() {
      StringBuilder out = new StringBuilder();
      out.append("|");

      int i;
      for(i = 1; i <= 10; ++i) {
         out.append("#").append(i);
         if (i <= 9) {
            out.append("  |");
         } else {
            out.append(" |");
         }
      }

      out.append("\n");
      out.append("|");

      for(i = 1; i <= 10; ++i) {
         out.append("----+");
      }

      out.append("\n");
      out.append("|");

      for(i = 0; i < 10; ++i) {
         if (i >= this.m_frames.size()) {
            out.append("    |");
         } else {
            Frame f = (Frame)this.m_frames.get(i);
            if (i < 9) {
               out.append("  ");
            } else {
               out.append(" ");
            }

            out.append(f).append("|");
         }
      }

      out.append("\n");
      out.append("|");

      for(i = 1; i <= 10; ++i) {
         if (i > this.m_frames.size()) {
            out.append("    |");
         } else {
            int score = this.getCumulativeScore(i);
            out.append(padScore(score));
            out.append("|");
         }
      }

      return out.toString();
   }

   public int getCumulativeScore(int frame) {
      if (frame >= 1 && frame <= this.m_frames.size()) {
         int score = 0;

         for(int i = 0; i < Math.min(frame, this.m_frames.size() + 1); ++i) {
            Frame f = (Frame)this.m_frames.get(i);
            if (i == 9) {
               if (f.getPinsDown(1) == 10) {
                  score += 10 + f.getPinsDown(2) + f.getPinsDown(3);
               } else if (f.getPinsDown(1) + f.getPinsDown(2) == 10) {
                  score += 10 + f.getPinsDown(3);
               } else {
                  score += f.getPinsDown(1) + f.getPinsDown(2);
               }

               return score;
            }

            int pins_down = f.countPinsDown();
            if (pins_down < 10) {
               score += pins_down;
            } else {
               score += 10;
               Frame f_next;
               int next_pins_down;
               if (f.getPinsDown(1) == 10) {
                  if (i >= this.m_frames.size() - 1) {
                     return -1;
                  }

                  f_next = (Frame)this.m_frames.get(i + 1);
                  next_pins_down = f_next.getPinsDown(1);
                  score += next_pins_down;
                  if (next_pins_down != 10) {
                     int next_pins_down_2 = f_next.getPinsDown(2);
                     if (next_pins_down_2 < 0) {
                        return -1;
                     }

                     score += f_next.getPinsDown(2);
                  }
               } else {
                  if (i >= this.m_frames.size() - 1) {
                     return -1;
                  }

                  f_next = (Frame)this.m_frames.get(i + 1);
                  next_pins_down = f_next.getPinsDown(1);
                  score += next_pins_down;
               }
            }
         }

         return score;
      } else {
         throw new BowlingException("Frame #" + frame + " does not exist in this game");
      }
   }

   protected static String padScore(int score) {
      if (score < 0) {
         return "    ";
      } else if (score < 10) {
         return score + "   ";
      } else {
         return score < 100 ? score + "  " : score + " ";
      }
   }
}
