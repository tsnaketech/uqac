package stev.kwikemart;

public final class Upc {
   public static final String generateCode(String prefix) {
      return prefix + getCheckDigit(prefix);
   }

   public static final int getDigit(String c) {
      boolean var1 = false;

      try {
         int i_c = Integer.parseInt(c);
         return i_c;
      } catch (NumberFormatException var3) {
         return -1;
      }
   }

   public static final int getCheckDigit(String prefix) {
      int odd_sum = 0;
      int even_sum = 0;

      int i;
      int i_c;
      for(i = 0; i < 11; ++i) {
         i_c = getDigit(prefix.substring(i, i + 1));
         if (i_c < 0) {
            return -1;
         }

         if (i % 2 == 0) {
            odd_sum += i_c;
         } else {
            even_sum += i_c;
         }
      }

      i = 3 * odd_sum + even_sum;
      i_c = (int)Math.ceil((double)((float)i / 10.0F)) * 10 - i;
      return i_c;
   }

   private Upc() {
      throw new UnsupportedOperationException();
   }
}
