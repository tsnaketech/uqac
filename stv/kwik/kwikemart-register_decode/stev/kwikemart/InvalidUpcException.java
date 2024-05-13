package stev.kwikemart;

public abstract class InvalidUpcException extends ItemException {
   private static final long serialVersionUID = 1L;

   public InvalidUpcException(String upc, String explanation) {
      super(upc, explanation);
   }

   public static final class InvalidCheckDigitException extends InvalidUpcException {
      private static final long serialVersionUID = 1L;

      public InvalidCheckDigitException(String upc) {
         super(upc, "invalid UPC check digit");
      }
   }

   public static final class InvalidDigitException extends InvalidUpcException {
      private static final long serialVersionUID = 1L;

      public InvalidDigitException(String upc, int position) {
         super(upc, "invalid UPC digit at position " + position);
      }
   }

   public static final class NoUpcException extends InvalidUpcException {
      private static final long serialVersionUID = 1L;

      public NoUpcException(String upc) {
         super(upc, "the UPC is the empty string");
      }
   }

   public static final class UpcTooLongException extends InvalidUpcException {
      private static final long serialVersionUID = 1L;

      public UpcTooLongException(String upc) {
         super(upc, "the UPC is too long");
      }
   }

   public static final class UpcTooShortException extends InvalidUpcException {
      private static final long serialVersionUID = 1L;

      public UpcTooShortException(String upc) {
         super(upc, "the UPC is too short");
      }
   }
}
