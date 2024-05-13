package stev.kwikemart;

public abstract class AmountException extends ItemException {
   private static final long serialVersionUID = 1L;

   public AmountException(String upc, String message) {
      super(upc, message);
   }

   public static final class AmountTooLargeException extends AmountException {
      private static final long serialVersionUID = 1L;

      public AmountTooLargeException(String upc) {
         super(upc, "the amount exceeds the maximum value allowed by the register");
      }
   }

   public static final class NegativeAmountException extends AmountException {
      private static final long serialVersionUID = 1L;

      public NegativeAmountException(String upc) {
         super(upc, "the amount is negative");
      }
   }
}
